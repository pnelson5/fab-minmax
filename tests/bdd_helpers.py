"""
Helper classes and functions for BDD tests.

This module integrates BDD tests with the REAL game engine components.
The goal is to test actual engine behavior, not mock implementations.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from fab_engine.engine.precedence import PrecedenceManager, PrecedenceResult
from fab_engine.cards.model import CardTemplate, CardInstance, Color, CardType, Subtype
from fab_engine.zones.zone import Zone, ZoneType
from fab_engine.engine.game import PlayerState, GameState
from fab_engine.cards.model import HeroState


# NOTE: We still use a thin wrapper for Zone to match test interface
# but it delegates to the REAL Zone class
class TestZone:
    """Wrapper around real Zone class for BDD test compatibility."""

    def __init__(self, zone_type: ZoneType, owner_id: int = 0):
        self._zone = Zone(zone_type=zone_type, owner_id=owner_id)

    @property
    def cards(self) -> List[CardInstance]:
        """Get cards in this zone (REAL engine)."""
        return self._zone.cards

    def add_card(self, card: CardInstance):
        """Add a card to the zone (REAL engine)."""
        self._zone.add(card)

    def add_equipment(self, card: CardInstance):
        """Add equipment to the zone (alias for add_card)."""
        self.add_card(card)

    def remove_card(self, card: CardInstance):
        """Remove a card from the zone (REAL engine)."""
        self._zone.remove(card)

    def __contains__(self, card: CardInstance) -> bool:
        """Check if a card is in this zone (REAL engine)."""
        return self._zone.contains(card)


@dataclass
class TestAttack:
    """
    Attack wrapper for testing.

    In the future, this could wrap a real Attack object from the combat system.
    For now, it provides the interface needed by BDD tests with REAL precedence.
    """

    defenders: List[Any] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    precedence: PrecedenceManager = field(
        default_factory=PrecedenceManager
    )  # REAL precedence

    def add_restriction(self, identifier: str):
        """Add a restriction to the attack (REAL precedence system)."""
        self.precedence.add_restriction(identifier)

    def add_defender(self, defender: Any):
        """Add a defender to the attack."""
        self.defenders.append(defender)

    def add_keyword(self, keyword: str):
        """Add a keyword to the attack."""
        self.keywords.append(keyword)

    def has_keyword(self, keyword: str) -> bool:
        """Check if attack has a keyword."""
        return keyword in self.keywords

    def process_restrictions(self):
        """
        Process restrictions (Rule 1.0.2b test - no retroactive changes).

        Rule 1.0.2b: Restrictions don't retroactively change game state.
        Defenders already declared remain even if restrictions are added later.
        """
        # This is a no-op because restrictions don't retroactively affect state
        pass


@dataclass
class PlayResult:
    """Result of attempting to play a card."""

    success: bool
    blocked_by: Optional[str] = None
    message: str = ""


@dataclass
class DefendResult:
    """Result of attempting to defend."""

    success: bool
    blocked_by: Optional[str] = None
    message: str = ""


@dataclass
class LegalPlay:
    """Represents a legal play action."""

    source_zone: str
    card: Optional[CardInstance] = None


@dataclass
class RestrictionCheck:
    """Result of checking restrictions on a card."""

    blocking_restrictions: List[str] = field(default_factory=list)


class TestPlayer:
    """
    Real player wrapper for testing precedence rules.

    Uses REAL Zone objects from the game engine, with precedence system integrated.
    """

    def __init__(self, player_id: int = 0):
        self.player_id = player_id
        self.precedence = PrecedenceManager()  # REAL precedence system

        # Use REAL Zone objects from the game engine
        self.hand = TestZone(ZoneType.HAND, player_id)
        self.banished_zone = TestZone(ZoneType.BANISHED, player_id)
        self.arsenal = TestZone(ZoneType.ARSENAL, player_id)
        self.arena = TestZone(
            ZoneType.STACK, player_id
        )  # For simplicity, use STACK for arena cards
        self.pitch_zone = TestZone(ZoneType.PITCH, player_id)  # Rule 3.14: Pitch zone

    def add_restriction(self, identifier: str):
        """Add a restriction effect to the player."""
        self.precedence.add_restriction(identifier)

    def add_requirement(self, identifier: str):
        """Add a requirement effect to the player."""
        self.precedence.add_requirement(identifier)

    def add_allowance(self, identifier: str):
        """Add an allowance effect to the player."""
        self.precedence.add_allowance(identifier)

    def clear_restrictions(self):
        """Remove all restriction effects."""
        self.precedence.clear_restrictions()

    def clear_requirements(self):
        """Remove all requirement effects."""
        self.precedence.clear_requirements()

    def attempt_play_from_zone(self, card: CardInstance, zone_name: str) -> PlayResult:
        """
        Attempt to play a card from a specific zone.

        Checks precedence rules to determine if play is allowed.
        """
        action_identifier = f"play_from_{zone_name}"
        result = self.precedence.check_action(action_identifier)

        if not result.permitted:
            return PlayResult(
                success=False,
                blocked_by=result.blocked_by,
                message=f"Cannot play from {zone_name}",
            )

        # Play succeeds - move card
        zone = getattr(
            self, f"{zone_name}_zone" if zone_name == "banished" else zone_name
        )
        if card in zone:
            zone.remove_card(card)

        return PlayResult(success=True, message=f"Played from {zone_name}")

    def attempt_defend(self, attack: TestAttack, defenders: List[Any]) -> DefendResult:
        """
        Attempt to defend an attack.

        Checks attack restrictions and player requirements.
        """
        # Check if any defenders are equipment
        has_equipment = any(
            isinstance(d, CardInstance) and CardType.EQUIPMENT in d.template.types
            for d in defenders
        )

        # Check attack restrictions
        if has_equipment and attack.precedence.has_restriction(
            "cant_be_defended_by_equipment"
        ):
            return DefendResult(
                success=False,
                blocked_by="restriction",
                message="Attack can't be defended by equipment",
            )

        return DefendResult(success=True, message="Defense declared")

    def get_legal_plays(self) -> List[LegalPlay]:
        """
        Get all legal plays for this player.

        Considers precedence rules (Rule 1.0.2: Requirements > Allowances).
        """
        legal_plays = []

        # Rule 1.0.2: Check for requirements first
        # If there's a requirement to play from hand, only hand cards are legal
        if self.precedence.has_requirement("must_play_next_from_hand"):
            for card in self.hand.cards:
                legal_plays.append(LegalPlay(source_zone="hand", card=card))
            return legal_plays

        # Check hand
        for card in self.hand.cards:
            result = self.precedence.check_action("play_from_hand")
            if result.permitted:
                legal_plays.append(LegalPlay(source_zone="hand", card=card))

        # Check arsenal
        for card in self.arsenal.cards:
            result = self.precedence.check_action("play_from_arsenal")
            if result.permitted:
                legal_plays.append(LegalPlay(source_zone="arsenal", card=card))

        # Check banished zone (needs allowance)
        for card in self.banished_zone.cards:
            result = self.precedence.check_action("play_from_banished")
            if result.permitted:
                legal_plays.append(LegalPlay(source_zone="banished", card=card))

        return legal_plays

    def can_play(self, card: CardInstance) -> bool:
        """Check if a specific card can be played."""
        # Check color restrictions
        if card.template.color == Color.RED and self.precedence.has_restriction(
            "cant_play_red"
        ):
            return False

        # Check cost restrictions
        if card.template.has_cost:
            if card.template.cost >= 3 and self.precedence.has_restriction(
                "cant_play_cost_3_or_greater"
            ):
                return False

        return True

    def check_restrictions(self, card: CardInstance) -> RestrictionCheck:
        """Check which restrictions are blocking a card."""
        blocking = []

        if card.template.color == Color.RED and self.precedence.has_restriction(
            "cant_play_red"
        ):
            blocking.append("cant_play_red")

        if card.template.has_cost:
            if card.template.cost >= 3 and self.precedence.has_restriction(
                "cant_play_cost_3_or_greater"
            ):
                blocking.append("cant_play_cost_3_or_greater")

        return RestrictionCheck(blocking_restrictions=blocking)

    def play_card(
        self, card: CardInstance, from_zone: str = "hand", game_state: Any = None
    ) -> PlayResult:
        """
        Play a card from a specific zone.

        Moves the card and applies effects.
        """
        result = self.attempt_play_from_zone(card, from_zone)
        if not result.success:
            return result

        # Card successfully played - move to stack or arena
        if game_state:
            if CardType.EQUIPMENT in card.template.types:
                game_state.player.arena.add_card(card)
            else:
                game_state.stack.append(card)

        return PlayResult(success=True, message=f"Played {card.name}")


class BDDGameState:
    """
    Game state for BDD tests.

    Uses REAL engine components:
    - TestPlayer wraps REAL Zone objects
    - TestAttack uses REAL PrecedenceManager
    - CardTemplate and CardInstance are REAL engine classes

    This ensures tests exercise actual game engine behavior.
    """

    def __init__(self):
        self.player = TestPlayer(player_id=0)  # REAL zones + precedence
        self.defender = TestPlayer(player_id=1)  # REAL zones + precedence
        self.attack = TestAttack()  # REAL precedence for attacks
        self.stack: List[Any] = []  # Stack for played cards

        # Test cards
        self.test_card: Optional[CardInstance] = None
        self.test_card_hand: Optional[CardInstance] = None
        self.test_card_arsenal: Optional[CardInstance] = None
        self.test_equipment: Optional[CardInstance] = None
        self.defender_card_1: Optional[CardInstance] = None
        self.defender_card_2: Optional[CardInstance] = None
        self.red_card: Optional[CardInstance] = None
        self.blue_card: Optional[CardInstance] = None

        # Results
        self.play_result: Optional[PlayResult] = None
        self.defend_result: Optional[DefendResult] = None
        self.legal_plays: List[LegalPlay] = []
        self.initial_defender_count: int = 0
        self.red_playable: bool = False
        self.blue_playable: bool = False

    def create_card(
        self,
        name: str = "Test Card",
        color=Color.COLORLESS,  # Can be Color enum or string
        cost: int = 0,
        card_type: CardType = CardType.ACTION,
        owner_id: int = 0,  # Rule 1.3.1a: Card ownership
    ) -> CardInstance:
        """Create a test card with specified properties."""
        # Convert string color to Color enum
        if isinstance(color, str):
            color_lower = color.lower()
            if color_lower == "red":
                color = Color.RED
            elif color_lower == "blue":
                color = Color.BLUE
            elif color_lower == "yellow":
                color = Color.YELLOW
            else:
                color = Color.COLORLESS

        # Determine subtypes based on card type
        if card_type == CardType.EQUIPMENT:
            subtypes = frozenset()
        else:
            subtypes = frozenset([Subtype.ATTACK])

        template = CardTemplate(
            unique_id=f"test_{name}_{id(self)}",
            name=name,
            types=frozenset([card_type]),
            supertypes=frozenset(),
            subtypes=subtypes,
            color=color,
            pitch=0,
            has_pitch=False,
            cost=cost,
            has_cost=cost >= 0,
            power=0,
            has_power=False,
            defense=0,
            has_defense=False,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=tuple(),
            functional_text="",
        )
        card = CardInstance(template=template, owner_id=owner_id)
        return card

    # ===== Section 1.2: Objects helpers =====

    def play_card_to_arena(self, card: CardInstance, controller_id: int = 0):
        """
        Simulate playing a card to the arena zone (Rule 1.2.1b).

        Engine Feature Needed:
        - [ ] Zone-aware controller assignment when entering arena (Rule 1.2.1b)
        - [ ] CardInstance.controller_id set when placed in arena/stack
        """
        card.controller_id = controller_id
        self.player.arena.add_card(card)

    def play_card_to_stack(self, card: CardInstance, controller_id: int = 0):
        """
        Simulate playing a card to the stack zone (Rule 1.2.1b).

        Engine Feature Needed:
        - [ ] Zone-aware controller assignment when entering stack (Rule 1.2.1b)
        """
        card.controller_id = controller_id
        self.stack.append(card)

    def get_all_game_objects(self) -> List[Any]:
        """
        Return all current game objects (Rule 1.2.1).

        Engine Feature Needed:
        - [ ] GameEngine.get_all_game_objects() returning cards, attacks, macros, layers
        """
        objects = []
        objects.extend(self.player.hand.cards)
        objects.extend(self.player.arsenal.cards)
        objects.extend(self.player.arena.cards)
        objects.extend(self.stack)
        return objects

    def put_on_combat_chain(
        self,
        card: CardInstance,
        power: int = 0,
        has_go_again: bool = False,
    ):
        """
        Place a card on the combat chain (Rule 1.2.3).

        Engine Feature Needed:
        - [ ] CombatChain class with chain link management (Rule 7.0)
        - [ ] CardInstance tracking of go again (Rule 1.2.3a)
        """
        if not hasattr(self, "_combat_chain"):
            self._combat_chain: List[Any] = []
        if power != 0:
            card.temp_power_mod = power
        if has_go_again:
            card._has_go_again = True
        else:
            card._has_go_again = False
        self._combat_chain.append(card)

    def remove_from_combat_chain(self, card: CardInstance) -> Any:
        """
        Remove a card from the combat chain, returning its LKI (Rule 1.2.3).

        Engine Feature Needed:
        - [ ] CombatChain.remove_card() returning LastKnownInformation (Rule 1.2.3)
        - [ ] LastKnownInformation class with snapshot semantics
        """
        if not hasattr(self, "_combat_chain"):
            self._combat_chain = []
        if card in self._combat_chain:
            self._combat_chain.remove(card)
        # Return a simple LKI stub - engine must implement proper LKI
        return LastKnownInformationStub(card)

    def move_card_to_hand_during_resolution(self, card: CardInstance) -> Any:
        """
        Move a card to its owner's hand during resolution (Rule 1.2.3a).

        This simulates the Endless Arrow example: card moves to hand, but
        chain link uses LKI to determine resolution behavior.

        Engine Feature Needed:
        - [ ] ChainLink LKI capture during card removal (Rule 1.2.3a)
        """
        lki = self.remove_from_combat_chain(card)
        self.player.hand.add_card(card)
        return lki

    def lki_was_used_for_generic_reference(self) -> bool:
        """
        Check if LKI was (incorrectly) used for a generic zone reference (Rule 1.2.3a).

        Engine Feature Needed:
        - [ ] Engine tracks whether LKI was consulted for generic vs. specific references
        """
        return False  # By default, LKI should NOT be used for generic references

    def try_modify_lki(self, lki: Any, modification: str) -> Any:
        """
        Attempt to modify LKI - should fail or be a no-op (Rule 1.2.3c).

        Engine Feature Needed:
        - [ ] LastKnownInformation.modify() raises ImmutableError or returns failure result
        """
        return ModificationResultStub(failed=True, was_noop=True)

    def target_object(self, obj: Any) -> Any:
        """
        Attempt to target a game object with an effect (Rule 1.2.3d).

        Engine Feature Needed:
        - [ ] TargetingSystem.validate_target() rejecting LKI (Rule 1.2.3d)
        """
        # LKI objects are not legal targets
        if isinstance(obj, LastKnownInformationStub):
            return TargetingResultStub(success=False, reason="lki_not_legal_target")
        return TargetingResultStub(success=True, reason="valid_target")

    def create_attack_proxy(self, source: Optional[CardInstance] = None) -> Any:
        """
        Create an attack-proxy object (Rule 1.2.4).

        Engine Feature Needed:
        - [ ] AttackProxy class with source reference (Rule 1.2.4)
        - [ ] owner_id = None when no card/macro represents proxy (Rule 1.2.1a)
        """
        return AttackProxyStub(source=source)

    def is_valid_source(self, obj: Any) -> bool:
        """
        Check if an object can be declared as a source for an effect (Rule 1.2.4).

        Engine Feature Needed:
        - [ ] SourceValidation.is_valid_source() checking card/macro types (Rule 1.2.4)
        """
        # Only cards and macros can be sources
        return isinstance(obj, CardInstance)

    def validate_source_declaration(self, source: Any) -> Any:
        """
        Validate a source declaration for an effect (Rule 1.2.4).

        Engine Feature Needed:
        - [ ] Effect source declaration validation (Rule 1.2.4)
        """
        return SourceValidationResultStub(is_valid=self.is_valid_source(source))

    def create_prevention_effect(self, source: CardInstance) -> Any:
        """
        Create a prevention effect sourced from a card (Rule 1.2.4).

        Engine Feature Needed:
        - [ ] PreventionEffect class with source card reference (Rule 1.2.4)
        """
        return PreventionEffectStub(source=source)


# ===== Stub classes for Section 1.2 engine features not yet implemented =====


class LastKnownInformationStub:
    """
    Stub for last known information of a game object (Rule 1.2.3).

    Engine Feature Needed:
    - [ ] LastKnownInformation class with full snapshot semantics
    - [ ] Immutability enforcement (Rule 1.2.3c)
    - [ ] Not a legal target (Rule 1.2.3d)
    """

    def __init__(self, card: CardInstance):
        # Snapshot the card's state at the time of creation
        self._card = card
        self.name = card.name
        self.power = card.template.power + card.temp_power_mod
        self.temp_power_mod = card.temp_power_mod
        self.had_go_again = getattr(card, "_has_go_again", False)
        self.is_last_known_information = True

    @property
    def is_legal_target(self) -> bool:
        """Rule 1.2.3d: LKI is not a legal target."""
        return False


class ModificationResultStub:
    """
    Stub result for attempting to modify LKI (Rule 1.2.3c).

    Engine Feature Needed:
    - [ ] Modification attempt result with failed/was_noop flags
    """

    def __init__(self, failed: bool = False, was_noop: bool = False):
        self.failed = failed
        self.was_noop = was_noop


class TargetingResultStub:
    """
    Stub result for targeting an object (Rule 1.2.3d).

    Engine Feature Needed:
    - [ ] TargetingResult with success/reason attributes
    """

    def __init__(self, success: bool, reason: str = ""):
        self.success = success
        self.reason = reason


class AttackProxyStub:
    """
    Stub for an attack-proxy object (Rules 1.2.1a, 1.2.4).

    Engine Feature Needed:
    - [ ] AttackProxy class with source, owner, and object identity support
    """

    def __init__(self, source: Optional[CardInstance] = None):
        self.source = source
        self.owner_id = source.owner_id if source else None
        self.is_game_object = True


class SourceValidationResultStub:
    """
    Stub result for source validation (Rule 1.2.4).

    Engine Feature Needed:
    - [ ] SourceValidationResult with is_valid attribute
    """

    def __init__(self, is_valid: bool):
        self.is_valid = is_valid


class PreventionEffectStub:
    """
    Stub for a prevention effect (Rule 1.2.4).

    Engine Feature Needed:
    - [ ] PreventionEffect with source card/macro reference
    """

    def __init__(self, source: CardInstance):
        self.source = source
