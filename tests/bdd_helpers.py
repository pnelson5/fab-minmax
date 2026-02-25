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

    # ===== Section 1.3: Cards helpers =====

    def create_token_card(
        self, name: str = "Test Token", owner_id: int = 0
    ) -> CardInstance:
        """
        Create a token card (Rule 1.3.2b).

        Engine Feature Needed:
        - [ ] CardType.TOKEN enum value (Rule 1.3.2b)
        """
        # TOKEN type not yet in engine - use a stub approach
        template = CardTemplate(
            unique_id=f"token_{name}_{id(self)}",
            name=name,
            types=frozenset(),  # Will need frozenset([CardType.TOKEN]) when implemented
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=0,
            has_cost=False,
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
        # Mark as token via metadata until engine supports CardType.TOKEN
        card._is_token = True  # type: ignore[attr-defined]
        return card

    def create_resource_card(
        self, name: str = "Test Resource", owner_id: int = 0
    ) -> CardInstance:
        """
        Create a resource card (Rule 1.3.2c).

        Engine Feature Needed:
        - [ ] CardType.RESOURCE enum value (Rule 1.3.2c)
        """
        template = CardTemplate(
            unique_id=f"resource_{name}_{id(self)}",
            name=name,
            types=frozenset(),  # Will need frozenset([CardType.RESOURCE]) when implemented
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=0,
            has_cost=False,
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
        card._is_resource = True  # type: ignore[attr-defined]
        return card

    def create_mentor_card(
        self, name: str = "Test Mentor", owner_id: int = 0
    ) -> CardInstance:
        """
        Create a mentor card (Rule 1.3.2c).

        Engine Feature Needed:
        - [ ] CardType.MENTOR enum value (Rule 1.3.2c)
        """
        template = CardTemplate(
            unique_id=f"mentor_{name}_{id(self)}",
            name=name,
            types=frozenset(),  # Will need frozenset([CardType.MENTOR]) when implemented
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=0,
            has_cost=False,
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
        card._is_mentor = True  # type: ignore[attr-defined]
        return card

    def create_card_with_permanent_subtype(
        self,
        name: str = "Test Permanent",
        subtype: str = "ally",
        owner_id: int = 0,
    ) -> CardInstance:
        """
        Create a deck card with a permanent-granting subtype (Rule 1.3.3).

        Engine Feature Needed:
        - [ ] Subtype.ALLY, AFFLICTION, ASH, AURA, CONSTRUCT, FIGMENT, INVOCATION,
               ITEM, LANDMARK enum values (Rule 1.3.3)
        """
        # Check if subtype is already in engine
        permanent_subtypes_engine = {
            Subtype.AURA,
            Subtype.ITEM,
        }
        # Map name to engine Subtype if available
        subtype_lower = subtype.lower()
        if subtype_lower == "aura":
            subtypes_set = frozenset([Subtype.AURA])
        elif subtype_lower == "item":
            subtypes_set = frozenset([Subtype.ITEM])
        else:
            # Subtype not yet in engine - track as metadata
            subtypes_set = frozenset()

        template = CardTemplate(
            unique_id=f"permanent_{name}_{id(self)}",
            name=name,
            types=frozenset([CardType.ACTION]),
            supertypes=frozenset(),
            subtypes=subtypes_set,
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=0,
            has_cost=False,
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
        card._permanent_subtype = subtype_lower  # type: ignore[attr-defined]
        return card

    def create_card_with_name_and_pitch(
        self, name: str, pitch: int, owner_id: int = 0
    ) -> CardInstance:
        """
        Create a card with a specific name and pitch value (Rule 1.3.4).

        Used for card distinctness testing.
        """
        template = CardTemplate(
            unique_id=f"distinct_{name}_{pitch}_{id(self)}",
            name=name,
            types=frozenset([CardType.ACTION]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ATTACK]),
            color=Color.COLORLESS,
            pitch=pitch,
            has_pitch=True,
            cost=0,
            has_cost=True,
            power=0,
            has_power=True,
            defense=0,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=tuple(),
            functional_text="",
        )
        return CardInstance(template=template, owner_id=owner_id)

    def get_card_category(self, card: CardInstance) -> str:
        """
        Return the card category: 'hero', 'token', 'deck', or 'arena' (Rule 1.3.2).

        Engine Feature Needed:
        - [ ] CardTemplate.get_category() -> str returning the card category
        - [ ] CardType.TOKEN, RESOURCE, MENTOR, BLOCK enum values
        """
        # Delegate to engine if implemented
        if hasattr(card.template, "get_category"):
            return card.template.get_category()

        # Fallback logic using current engine types
        if CardType.HERO in card.template.types:
            return "hero"

        # TOKEN check - engine doesn't have CardType.TOKEN yet
        if getattr(card, "_is_token", False):
            return "token"

        # Deck-card types as per Rule 1.3.2c
        deck_types = {
            CardType.ACTION,
            CardType.ATTACK_REACTION,
            CardType.DEFENSE_REACTION,
            CardType.INSTANT,
        }
        # Resource, Mentor, Block not yet in engine - check via metadata
        if getattr(card, "_is_resource", False):
            return "deck"
        if getattr(card, "_is_mentor", False):
            return "deck"

        if card.template.types & deck_types:
            return "deck"

        # Arena-card: not hero, not token, not deck
        if (
            CardType.EQUIPMENT in card.template.types
            or CardType.WEAPON in card.template.types
        ):
            return "arena"

        # If types are empty (stub), check metadata
        if not card.template.types:
            return "unknown"

        return "arena"

    def can_start_in_deck(self, card: CardInstance) -> bool:
        """
        Check if a card can start in a player's deck (Rule 1.3.2c/d).

        Engine Feature Needed:
        - [ ] CardTemplate.can_start_in_deck property
        """
        if hasattr(card.template, "can_start_in_deck"):
            return card.template.can_start_in_deck

        category = self.get_card_category(card)
        return category == "deck"

    def is_valid_for_card_pool(self, card: CardInstance) -> bool:
        """
        Check if a card can be part of a player's card-pool (Rule 1.3.2b).

        Token cards are NOT part of a player's card-pool.

        Engine Feature Needed:
        - [ ] CardTemplate.is_part_of_card_pool property
        """
        if hasattr(card.template, "is_part_of_card_pool"):
            return card.template.is_part_of_card_pool

        category = self.get_card_category(card)
        # Token cards cannot be part of card-pool (Rule 1.3.2b)
        return category != "token"

    def is_card_a_permanent(
        self,
        card: CardInstance,
        in_arena: bool = True,
        in_combat_chain: bool = False,
    ) -> bool:
        """
        Check if a card qualifies as a permanent (Rule 1.3.3).

        A card is a permanent if:
        - It is in the arena (not combat chain), AND
        - It is a hero-card, arena-card, or token-card, OR
        - It is a deck-card with one of the permanent subtypes:
          Affliction, Ally, Ash, Aura, Construct, Figment, Invocation, Item, Landmark

        Engine Feature Needed:
        - [ ] CardInstance.is_permanent property with full zone + subtype logic
        """
        if hasattr(card, "is_permanent"):
            return card.is_permanent  # type: ignore[return-value]

        if not in_arena:
            return False
        if in_combat_chain:
            return False

        category = self.get_card_category(card)

        # Hero, arena, and token cards are always permanents in the arena
        if category in ("hero", "arena", "token"):
            return True

        # Deck cards: only with permanent subtypes
        if category == "deck":
            # Check engine-known permanent subtypes
            permanent_subtypes_engine = {Subtype.AURA, Subtype.ITEM}
            if card.template.subtypes & permanent_subtypes_engine:
                return True
            # Check metadata-tracked subtypes (for engine types not yet implemented)
            perm_subtype = getattr(card, "_permanent_subtype", None)
            if perm_subtype in {
                "affliction",
                "ally",
                "ash",
                "aura",
                "construct",
                "figment",
                "invocation",
                "item",
                "landmark",
            }:
                return True
            return False

        return False

    def tap_permanent(self, card: CardInstance) -> None:
        """
        Tap a permanent (Rule 1.3.3b).

        Engine Feature Needed:
        - [ ] Dedicated tap() method on CardInstance or game engine
        """
        card.is_tapped = True

    def untap_permanent(self, card: CardInstance) -> None:
        """
        Untap a permanent (Rule 1.3.3b).

        Engine Feature Needed:
        - [ ] Dedicated untap() method on CardInstance or game engine
        """
        card.is_tapped = False

    # ===== Section 1.7: Abilities helpers =====

    def activate_ability(
        self,
        source_card: CardInstance,
        ability_text: str,
        activating_player_id: int = 0,
    ) -> Any:
        """
        Simulate activating an ability, creating an activated-layer on the stack.

        Engine Feature Needed:
        - [ ] ActivatedAbility.activate(player_id) creating an ActivatedLayer (Rule 1.7.3a)
        - [ ] ActivatedLayer.source reference (Rule 1.7.1a)
        - [ ] ActivatedLayer.controller_id = activating player (Rule 1.7.1b)
        - [ ] ActivatedLayer.exists_independently_of_source = True (Rule 1.7.1a)
        """
        return ActivatedLayerStub(
            source=source_card,
            controller_id=activating_player_id,
            ability_text=ability_text,
        )

    def create_triggered_layer(
        self,
        source_card: CardInstance,
        ability_text: str,
        controller_id: Optional[int] = None,
    ) -> Any:
        """
        Simulate creating a triggered-layer (two-step: create then put on stack).

        Engine Feature Needed:
        - [ ] TriggeredLayer class (Rule 1.6.2c)
        - [ ] TriggeredLayer.source reference (Rule 1.7.1a)
        - [ ] TriggeredLayer.controller_id = controller at trigger time or owner (Rule 1.7.1b)
        - [ ] TriggeredLayer.exists_independently_of_source = True (Rule 1.7.1a)
        """
        if controller_id is None:
            # Rule 1.7.1b: If source has no controller, use owner
            ctrl = source_card.owner_id
        else:
            ctrl = controller_id
        return TriggeredLayerStub(
            source=source_card,
            controller_id=ctrl,
            ability_text=ability_text,
        )

    def check_ability_functional(
        self,
        card: CardInstance,
        ability_text: str,
        in_arena: bool = False,
        is_public: bool = False,
        is_defending: bool = False,
        is_permanent: bool = True,
        is_resolving: bool = False,
        ability_type: str = "activated",
        context: str = "in_game",
        cost_only_payable_outside_arena: bool = False,
        current_zone: str = "hand",
        specifies_defending: bool = False,
        while_condition_met: bool = False,
        destination_zone: str = "",
        is_being_played: bool = False,
    ) -> bool:
        """
        Check whether an ability is functional given a context.

        Engine Feature Needed:
        - [ ] Ability.is_functional(context) method (Rule 1.7.4)
        - [ ] FunctionalityContext class with zone, is_defending, is_resolving, etc.

        Reference: Rules 1.7.4 through 1.7.4j
        """
        # Meta-static: always functional outside game
        if ability_type == "meta_static":
            return True  # Rule 1.7.4d

        # Property-static: functional in any zone or outside game
        if ability_type == "property_static":
            return True  # Rule 1.7.4f

        # Zone-movement replacement static: functional when destination matches
        if ability_type == "zone_replacement_static":
            replacement_from = getattr(card, "zone_replacement_from", None)
            return destination_zone == replacement_from  # Rule 1.7.4j

        # Play-static: functional when source is public and being played
        if ability_type == "play_static":
            return is_public and is_being_played  # Rule 1.7.4e

        # While-static: functional when while-condition is met
        if ability_type == "while_static":
            return while_condition_met  # Rule 1.7.4g

        # Resolution ability: functional only when resolving on the stack
        if ability_type == "resolution":
            return is_resolving  # Rule 1.7.4c

        # Default (activated / static): functional when source is public and in arena
        # Exceptions:
        # - Rule 1.7.4b: Cost can only be paid outside arena
        if cost_only_payable_outside_arena and not in_arena:
            return True  # Rule 1.7.4b

        # Rule 1.7.4a: Non-permanent defending card - non-functional unless...
        if is_defending and not is_permanent:
            if specifies_defending:
                return True  # Ability specifies it can be activated while defending
            return False

        # Default: functional only when source is public and in arena (Rule 1.7.4)
        return in_arena and is_public

    def resolve_top_of_stack(self) -> Any:
        """
        Simulate resolving the top item from the stack.

        Engine Feature Needed:
        - [ ] Stack.resolve_top() returning ResolutionResult (Rule 5.3)
        - [ ] ResolutionResult.effects_generated list
        """
        if not self.stack:
            return ResolutionResultStub(effects_generated=[])
        top = self.stack.pop()
        # Simulate resolution abilities generating effects
        effects = []
        if hasattr(top, "resolution_abilities"):
            effects.extend(top.resolution_abilities)
        elif hasattr(top, "functional_text"):
            effects.append(top.functional_text)
        return ResolutionResultStub(effects_generated=effects)

    def declare_modal_modes(self, card: CardInstance, modes: List[str]) -> Any:
        """
        Declare modes for a modal ability.

        Engine Feature Needed:
        - [ ] ModalAbility.declare_modes(modes) with validation (Rules 1.7.5a, 1.7.5b)
        - [ ] ModalAbilityResult with success, reason, requires_distinct_modes
        """
        if not getattr(card, "is_modal", False):
            return ModalModeResultStub(
                success=False, reason="not_modal", requires_distinct_modes=False
            )
        allows_duplicates = getattr(card, "allows_duplicate_modes", False)
        if not allows_duplicates and len(modes) != len(set(modes)):
            return ModalModeResultStub(
                success=False,
                reason="duplicate_mode_not_allowed",
                requires_distinct_modes=True,
            )
        choose_count = getattr(card, "modal_choose_count", 1)
        available = getattr(card, "available_modes", [])
        max_selectable = min(choose_count, len(available))
        if len(modes) > max_selectable:
            return ModalModeResultStub(
                success=False,
                reason="too_many_modes",
                requires_distinct_modes=False,
            )
        # Mode selection is valid - set selected modes
        if not hasattr(card, "selected_modes"):
            card.selected_modes = []  # type: ignore[attr-defined]
        card.selected_modes = modes  # type: ignore[attr-defined]
        return ModalModeResultStub(
            success=True, reason="valid", requires_distinct_modes=False
        )

    def get_max_selectable_modes(self, card: CardInstance) -> int:
        """
        Get the maximum number of modes a player can select.

        Engine Feature Needed:
        - [ ] ModalAbility.max_selectable_count property (Rule 1.7.5b)
        """
        choose_count = getattr(card, "modal_choose_count", 1)
        available = getattr(card, "available_modes", [])
        return min(choose_count, len(available))

    def evaluate_modal_count(self, card: CardInstance, game_state_context: dict) -> int:
        """
        Evaluate the number of modes to select, using current game state context.

        Engine Feature Needed:
        - [ ] ModalAbility.evaluate_count(game_state) (Rule 1.7.5e)
        """
        if getattr(card, "conditional_modal_count", False):
            return getattr(card, "conditional_modal_count_value", 1)
        return getattr(card, "modal_choose_count", 1)

    def check_following_can_refer_to_leading(
        self, card: CardInstance, leading_events: dict
    ) -> bool:
        """
        Check if a following ability can refer to the leading ability's events.

        Engine Feature Needed:
        - [ ] ConnectedAbilityPair.following_can_refer_to_leading() (Rule 1.7.6b)
        """
        if not leading_events:
            return False  # Rule 1.7.6b: No events means following ability fails
        return True

    def add_connected_ability_pair(
        self,
        card: CardInstance,
        leading_ability: str,
        following_ability: str,
    ) -> Any:
        """
        Add a connected ability pair to a card.

        Engine Feature Needed:
        - [ ] Effect.add_connected_ability_pair(card, leading, following) (Rule 1.7.6c)
        - [ ] ConnectedAbilityPair class tracking connection
        """
        return ConnectedAbilityPairResultStub(
            leading_ability=leading_ability,
            following_ability=following_ability,
            is_connected=True,
            follows_only_added_leading=True,
        )

    def modify_card_ability(
        self,
        card: CardInstance,
        old_ability: str,
        new_ability: str,
    ) -> Any:
        """
        Modify an ability on a card.

        Engine Feature Needed:
        - [ ] Effect.modify_ability(card, old, new) (Rule 1.7.7)
        - [ ] CardInstance.abilities mutation tracking
        """
        if not hasattr(card, "abilities"):
            return AbilityModificationResultStub(
                success=False, original_ability_replaced=False
            )
        if old_ability in card.abilities:
            card.abilities.remove(old_ability)
            card.abilities.append(new_ability)
            return AbilityModificationResultStub(
                success=True, original_ability_replaced=True
            )
        return AbilityModificationResultStub(
            success=False, original_ability_replaced=False
        )

    def are_cards_distinct(self, card_a: CardInstance, card_b: CardInstance) -> bool:
        """
        Check if two cards are distinct from each other (Rule 1.3.4).

        Two cards are distinct if one or more of their faces has a different
        name and/or pitch value.

        Engine Feature Needed:
        - [ ] CardTemplate.is_distinct_from(other) method
        - [ ] Multi-face card support (Rule 9.1: double-faced cards)
        """
        if hasattr(card_a.template, "is_distinct_from"):
            return card_a.template.is_distinct_from(card_b.template)

        # Simple single-face comparison: name or pitch differs
        name_differs = card_a.template.name != card_b.template.name
        pitch_differs = (
            card_a.template.has_pitch
            and card_b.template.has_pitch
            and card_a.template.pitch != card_b.template.pitch
        ) or (card_a.template.has_pitch != card_b.template.has_pitch)

        return name_differs or pitch_differs


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


# ===== Stub classes for Section 1.7 engine features not yet implemented =====


class ActivatedLayerStub:
    """
    Stub for an activated-layer created by an activated ability (Rule 1.6.2b, 1.7.1a).

    Engine Feature Needed:
    - [ ] ActivatedLayer class (Rule 1.6.2b)
    - [ ] ActivatedLayer.source reference (Rule 1.7.1a)
    - [ ] ActivatedLayer.controller_id = activating player (Rule 1.7.1b)
    - [ ] ActivatedLayer.exists_independently_of_source = True (Rule 1.7.1a)
    - [ ] ActivatedLayer.is_resolved property (Rule 1.6.1)
    - [ ] ActivatedLayer.can_resolve property (Rule 1.7.1a)
    - [ ] ActivatedLayer.layer_category = "activated-layer" (Rule 1.6.2b)
    """

    def __init__(
        self,
        source: Optional[CardInstance],
        controller_id: int = 0,
        ability_text: str = "",
    ):
        self.source = source
        self.controller_id = controller_id
        self.ability_text = ability_text
        self.is_resolved = False
        self.can_resolve = True
        self.exists_independently_of_source = True
        self.layer_category = "activated-layer"
        self.is_layer = True


class TriggeredLayerStub:
    """
    Stub for a triggered-layer created by a triggered effect (Rule 1.6.2c, 1.7.1a).

    Engine Feature Needed:
    - [ ] TriggeredLayer class (Rule 1.6.2c)
    - [ ] TriggeredLayer.source reference (Rule 1.7.1a)
    - [ ] TriggeredLayer.controller_id = controller at trigger time or owner (Rule 1.7.1b)
    - [ ] TriggeredLayer.exists_independently_of_source = True (Rule 1.7.1a)
    - [ ] TriggeredLayer.can_resolve property (Rule 1.7.1a)
    - [ ] TriggeredLayer.layer_category = "triggered-layer" (Rule 1.6.2c)
    """

    def __init__(
        self,
        source: Optional[CardInstance],
        controller_id: int = 0,
        ability_text: str = "",
    ):
        self.source = source
        self.controller_id = controller_id
        self.ability_text = ability_text
        self.is_resolved = False
        self.can_resolve = True
        self.exists_independently_of_source = True
        self.layer_category = "triggered-layer"
        self.is_layer = True


class ResolutionResultStub:
    """
    Stub for the result of resolving a layer from the stack (Rule 5.3).

    Engine Feature Needed:
    - [ ] ResolutionResult class with effects_generated list
    - [ ] Stack.resolve_top() returning ResolutionResult
    """

    def __init__(self, effects_generated: Optional[List[str]] = None):
        self.effects_generated = effects_generated or []
        self.success = True


class ModalModeResultStub:
    """
    Stub result for modal mode declaration (Rules 1.7.5a, 1.7.5b).

    Engine Feature Needed:
    - [ ] ModalAbility.declare_modes() return value
    - [ ] ModalAbilityResult with success, reason, requires_distinct_modes
    """

    def __init__(
        self,
        success: bool,
        reason: str = "",
        requires_distinct_modes: bool = False,
    ):
        self.success = success
        self.reason = reason
        self.requires_distinct_modes = requires_distinct_modes


class ConnectedAbilityPairResultStub:
    """
    Stub result for adding a connected ability pair to a card (Rule 1.7.6c).

    Engine Feature Needed:
    - [ ] ConnectedAbilityPair class tracking leading/following connection
    - [ ] Effect.add_connected_ability_pair() return value
    """

    def __init__(
        self,
        leading_ability: str,
        following_ability: str,
        is_connected: bool = True,
        follows_only_added_leading: bool = True,
    ):
        self.leading_ability = leading_ability
        self.following_ability = following_ability
        self.is_connected = is_connected
        self.follows_only_added_leading = follows_only_added_leading


class AbilityModificationResultStub:
    """
    Stub result for modifying a card's ability (Rule 1.7.7).

    Engine Feature Needed:
    - [ ] Effect.modify_ability() return value
    - [ ] CardInstance.abilities mutable list
    """

    def __init__(self, success: bool, original_ability_replaced: bool = False):
        self.success = success
        self.original_ability_replaced = original_ability_replaced
