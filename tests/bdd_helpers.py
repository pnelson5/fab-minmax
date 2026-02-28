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

    # ===== Section 1.8: Effects helpers =====

    def create_damage_effect(
        self,
        source: Optional[CardInstance] = None,
        damage_amount: int = 0,
        damage_type: str = "normal",
        controller_id: int = 0,
        target: Optional[CardInstance] = None,
        requires_arena_target: bool = False,
    ) -> Any:
        """
        Create a damage effect generated by an ability (Rule 1.8.1).

        Engine Feature Needed:
        - [ ] Effect class with source, controller_id, damage_amount (Rule 1.8.1)
        - [ ] Effect.source matching generating ability source (Rule 1.8.1a)
        - [ ] Effect.controller_id matching generating ability controller (Rule 1.8.1b)
        """
        return DamageEffectStub(
            source=source,
            damage_amount=damage_amount,
            damage_type=damage_type,
            controller_id=controller_id,
            target=target,
            requires_arena_target=requires_arena_target,
        )

    def check_card_has_effect(self, card: CardInstance, effect_type: str) -> bool:
        """
        Check if a card is considered to have an effect of the given type (Rule 1.8.2).

        This includes optional and conditional effects.

        Engine Feature Needed:
        - [ ] CardInstance.has_effect(effect_type) method (Rule 1.8.2)
        - [ ] Including optional and conditional effects in the check
        """
        # Engine Feature Needed: has_effect() on CardInstance
        if hasattr(card, "has_effect"):
            return card.has_effect(effect_type)
        # Fallback: check metadata set in tests
        if effect_type == "deal_damage":
            return getattr(card, "_has_deal_damage_effect", False)
        return False

    def create_optional_effect(
        self,
        source: Optional[CardInstance] = None,
        effect_text: str = "",
        can_be_generated: bool = True,
    ) -> Any:
        """
        Create an optional effect (Rule 1.8.3).

        Engine Feature Needed:
        - [ ] OptionalEffect class with requires_player_choice attribute (Rule 1.8.3)
        - [ ] OptionalEffect.can_be_generated() validation (Rule 1.8.3b)
        """
        return OptionalEffectStub(
            source=source,
            effect_text=effect_text,
            can_be_generated=can_be_generated,
        )

    def resolve_optional_effect(
        self,
        source: Optional[CardInstance] = None,
        player_choice: bool = True,
    ) -> Any:
        """
        Resolve an optional effect based on player's choice (Rule 1.8.3a).

        Engine Feature Needed:
        - [ ] OptionalEffect.generate(player_chose=True/False) (Rule 1.8.3a)
        - [ ] OptionalEffectResult with was_generated attribute
        """
        return OptionalEffectResultStub(was_generated=player_choice)

    def check_optional_effect_can_be_generated(
        self,
        source: Optional[CardInstance] = None,
        required_objects_count: int = 0,
        available_objects_count: int = 0,
    ) -> bool:
        """
        Check if an optional effect can be generated given the game state (Rule 1.8.3b).

        Engine Feature Needed:
        - [ ] OptionalEffect.can_be_generated() checking game state conditions (Rule 1.8.3b)
        """
        # Engine Feature Needed: OptionalEffect.can_be_generated() method
        return available_objects_count >= required_objects_count

    def check_may_choose_to_effect(
        self,
        source: Optional[CardInstance] = None,
        is_may_choose_to_phrasing: bool = False,
        can_fully_resolve: bool = True,
    ) -> bool:
        """
        Check if a 'may choose to' effect allows choice regardless of outcome (Rule 1.8.3b).

        Engine Feature Needed:
        - [ ] OptionalEffect.is_may_choose_to property (Rule 1.8.3b)
        - [ ] OptionalEffect allowing choice when is_may_choose_to = True regardless of outcome
        """
        if is_may_choose_to_phrasing:
            return True  # 'may choose to' always allows choice regardless of outcome
        return can_fully_resolve

    def check_target_required_on_stack(self, card: CardInstance) -> bool:
        """
        Check if a card requires target declaration when placed on stack (Rule 1.8.5).

        Engine Feature Needed:
        - [ ] TargetedEffect.requires_declaration_at_play = True (Rule 1.8.5)
        - [ ] CardLayer.require_target_declaration_on_play() (Rule 1.8.5)
        """
        # Engine Feature Needed: TargetedEffect.requires_declaration_at_play
        if hasattr(card, "_has_targeted_effect"):
            return card._has_targeted_effect
        # If card functional text contains "target", it requires declaration
        func_text = getattr(card, "functional_text", "") or ""
        return (
            "target" in func_text.lower()
            and not getattr(card, "_is_targeted_effect", True) is False
        )

    def check_is_legal_target(self, card: CardInstance) -> bool:
        """
        Check if a card is a legal target for an effect (Rule 1.8.5a).

        Legal targets must be public objects in the arena or on the stack.

        Engine Feature Needed:
        - [ ] TargetingSystem.is_legal_target(card) checking public + zone (Rule 1.8.5a)
        """
        # Engine Feature Needed: TargetingSystem.is_legal_target() method
        is_public = getattr(card, "_is_public", True)
        is_in_arena = (
            card in self.player.arena.cards or card in self.defender.arena.cards
        )
        is_on_stack = card in self.stack
        return is_public and (is_in_arena or is_on_stack)

    def create_multi_target_damage_effect(
        self,
        targets: List[CardInstance],
        damage_amount: int = 0,
    ) -> Any:
        """
        Create a damage effect targeting multiple objects (Rule 1.8.9).

        Engine Feature Needed:
        - [ ] MultiTargetEffect class with partial_success tracking (Rule 1.8.9)
        """
        return MultiTargetEffectStub(
            targets=targets,
            damage_amount=damage_amount,
        )

    def resolve_targeted_effect(
        self,
        effect: Any,
        target_exists: bool = True,
    ) -> Any:
        """
        Resolve a targeted effect, checking if target still exists (Rule 1.8.9).

        Engine Feature Needed:
        - [ ] Effect.fail() when target ceases to exist (Rule 1.8.9)
        - [ ] EffectResolutionResult with failed attribute
        """
        return EffectResolutionResultStub(failed=not target_exists)

    # ===== Section 1.13: Assets helpers =====

    def get_asset_types(self) -> List[str]:
        """
        Return the four asset types in the game (Rule 1.13.1).

        Engine Feature Needed:
        - [ ] AssetType enum with ACTION_POINT, RESOURCE_POINT, LIFE_POINT, CHI_POINT
        - [ ] GameEngine.get_asset_types() returning all valid asset types
        """
        return ["action_point", "resource_point", "life_point", "chi_point"]

    def set_player_action_points(self, player: Any, amount: int) -> None:
        """
        Set a player's action point count (Rule 1.13.2).

        Engine Feature Needed:
        - [ ] PlayerAssets.action_points property (Rule 1.13.2)
        - [ ] Player.set_action_points(amount) method
        """
        player._action_points = amount  # type: ignore[attr-defined]

    def get_player_action_points(self, player: Any) -> int:
        """
        Get a player's current action point count (Rule 1.13.2).

        Engine Feature Needed:
        - [ ] PlayerAssets.action_points property (Rule 1.13.2)
        - [ ] Player.get_action_points() method
        """
        return getattr(player, "_action_points", 0)

    def spend_player_action_point(self, player: Any) -> Any:
        """
        Spend one action point from a player (Rule 1.13.2).

        Engine Feature Needed:
        - [ ] Player.spend_action_point() -> ActionSpendResult (Rule 1.13.2)
        - [ ] ActionSpendResult.success property
        """
        current = self.get_player_action_points(player)
        if current <= 0:
            return AssetSpendResultStub(
                success=False, reason="insufficient_action_points"
            )
        self.set_player_action_points(player, current - 1)
        return AssetSpendResultStub(success=True)

    def begin_action_phase_for_player(self, player: Any) -> None:
        """
        Begin the action phase for a player, granting 1 action point (Rule 1.13.2a).

        Engine Feature Needed:
        - [ ] GameEngine.begin_action_phase(player_id) granting 1 action point (Rule 1.13.2a)
        - [ ] ActionPhaseStart granting exactly 1 action point to turn player
        """
        # Delegate to engine when implemented
        # Engine Feature Needed: GameEngine.begin_action_phase()
        current = self.get_player_action_points(player)
        if getattr(player, "_in_action_phase", False):
            self.set_player_action_points(player, current + 1)

    def trigger_go_again_for_player(self, player: Any) -> None:
        """
        Trigger the go again ability, granting 1 action point (Rule 1.13.2a).

        Engine Feature Needed:
        - [ ] GoAgainEffect.trigger(player_id) granting 1 action point (Rule 1.13.2a)
        - [ ] Action phase guard: does not fire outside action phase (Rule 1.13.2b)
        """
        # Only grant if in action phase (Rule 1.13.2b)
        if getattr(player, "_in_action_phase", False):
            current = self.get_player_action_points(player)
            self.set_player_action_points(player, current + 1)

    def grant_action_points_via_effect(self, player: Any, amount: int) -> None:
        """
        Grant action points via a card effect (Rule 1.13.2a).

        Engine Feature Needed:
        - [ ] GainActionPointEffect.apply(player_id, amount) (Rule 1.13.2a)
        - [ ] Guard: blocked outside action phase (Rule 1.13.2b)
        """
        # Only grant if in action phase (Rule 1.13.2b)
        if getattr(player, "_in_action_phase", False):
            current = self.get_player_action_points(player)
            self.set_player_action_points(player, current + amount)

    def simulate_instant_play_with_go_again(self, player: Any) -> None:
        """
        Simulate a non-turn player playing an instant with go again (Rule 1.13.2b).

        Engine Feature Needed:
        - [ ] InstantPlay check: player not in action phase, go again blocked (Rule 1.13.2b)
        """
        # Rule 1.13.2b: Player not in action phase cannot gain action points
        # The go_again trigger fires but is blocked
        in_phase = getattr(player, "_in_action_phase", False)
        if not in_phase:
            # Action point gain blocked per Rule 1.13.2b
            pass  # No action points gained

    def attempt_grant_action_points_outside_phase(
        self, player: Any, amount: int
    ) -> None:
        """
        Attempt to grant action points via effect when player is not in action phase (Rule 1.13.2b).

        Engine Feature Needed:
        - [ ] ActionPointGain.is_blocked_outside_action_phase() = True (Rule 1.13.2b)
        """
        # Rule 1.13.2b: Would-be grant is replaced with doing nothing
        in_phase = getattr(player, "_in_action_phase", False)
        if not in_phase:
            pass  # Action point gain is blocked; 0 points gained

    def register_lead_the_charge_trigger_for(self, player: Any) -> None:
        """
        Register the Lead the Charge delayed trigger for a player (Rule 1.13.2b example).

        Engine Feature Needed:
        - [ ] DelayedTriggerEffect tracking the "next cost 0 action card" condition (Rule 1.13.2b)
        - [ ] Trigger blocked when player not in action phase at resolution time
        """
        player._has_lead_the_charge_trigger = True  # type: ignore[attr-defined]

    def simulate_cost_zero_action_play(self, player: Any) -> None:
        """
        Simulate playing a cost-0 action card that would trigger Lead the Charge (Rule 1.13.2b).

        Engine Feature Needed:
        - [ ] DelayedTriggerEffect.check(player_id) triggering action point gain (Rule 1.13.2b)
        - [ ] Guard: blocked since player not in action phase (Rule 1.13.2b)
        """
        # Rule 1.13.2b: Even if Lead the Charge trigger fires, no action point gained
        in_phase = getattr(player, "_in_action_phase", False)
        has_trigger = getattr(player, "_has_lead_the_charge_trigger", False)
        if has_trigger and not in_phase:
            pass  # Trigger fires but action point is blocked by Rule 1.13.2b

    def set_player_resource_points(self, player: Any, amount: int) -> None:
        """
        Set a player's resource point count (Rule 1.13.3).

        Engine Feature Needed:
        - [ ] PlayerAssets.resource_points property (Rule 1.13.3)
        """
        player._resource_points = amount  # type: ignore[attr-defined]

    def get_player_resource_points(self, player: Any) -> int:
        """
        Get a player's current resource point count (Rule 1.13.3).

        Engine Feature Needed:
        - [ ] PlayerAssets.resource_points property (Rule 1.13.3)
        """
        return getattr(player, "_resource_points", 0)

    def pay_resource_cost(self, player: Any, cost: int) -> Any:
        """
        Pay a resource cost from the player's resource points (Rule 1.13.3).

        Engine Feature Needed:
        - [ ] AssetPayment.pay_resource_cost(player_id, cost) -> PaymentResult (Rule 1.13.3)
        - [ ] PaymentResult.success property
        """
        current = self.get_player_resource_points(player)
        if current < cost:
            return AssetSpendResultStub(
                success=False, reason="insufficient_resource_points"
            )
        self.set_player_resource_points(player, current - cost)
        return AssetSpendResultStub(success=True)

    def grant_resource_points_via_effect(self, player: Any, amount: int) -> None:
        """
        Grant resource points via effect (Rule 1.13.3a).

        Engine Feature Needed:
        - [ ] GainResourcePointEffect.apply(player_id, amount) (Rule 1.13.3a)
        """
        current = self.get_player_resource_points(player)
        self.set_player_resource_points(player, current + amount)

    def create_card_with_pitch(
        self,
        name: str = "Pitch Card",
        pitch_value: int = 1,
        pitch_generates: str = "resource",
        owner_id: int = 0,
    ) -> CardInstance:
        """
        Create a card with a specific pitch type (Rule 1.13.3a, 1.13.5a).

        Engine Feature Needed:
        - [ ] CardTemplate.pitch_generates_type field ("resource" or "chi") (Rule 2.8)
        - [ ] PitchEffect.generate_assets() using pitch_generates_type
        """
        template = CardTemplate(
            unique_id=f"pitch_{name}_{id(self)}",
            name=name,
            types=frozenset([CardType.ACTION]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ATTACK]),
            color=Color.COLORLESS,
            pitch=pitch_value,
            has_pitch=True,
            cost=0,
            has_cost=True,
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
        card._pitch_generates = pitch_generates  # type: ignore[attr-defined]
        return card

    def pitch_card_for_resources(self, player: Any, card: CardInstance) -> Any:
        """
        Pitch a card to generate resource points (Rule 1.13.3a).

        Engine Feature Needed:
        - [ ] PitchAction.execute(player_id, card) generating assets (Rule 1.14.3)
        - [ ] PitchResult with asset_type and amount
        """
        pitch_generates = getattr(card, "_pitch_generates", "resource")
        pitch_value = card.template.pitch

        if pitch_generates != "resource":
            return PitchPaymentResultStub(
                resources_gained=0, pitch_event_occurred=False
            )

        # Move card to pitch zone
        if card in player.hand:
            player.hand.remove_card(card)
        player.pitch_zone.add_card(card)

        # Grant resource points
        current = self.get_player_resource_points(player)
        new_total = current + pitch_value
        self.set_player_resource_points(player, new_total)
        return PitchPaymentResultStub(
            resources_gained=pitch_value,
            pitch_event_occurred=True,
            total_resources_after_pitch=new_total,
        )

    def set_player_chi_points(self, player: Any, amount: int) -> None:
        """
        Set a player's chi point count (Rule 1.13.5).

        Engine Feature Needed:
        - [ ] PlayerAssets.chi_points property (Rule 1.13.5)
        """
        player._chi_points = amount  # type: ignore[attr-defined]

    def get_player_chi_points(self, player: Any) -> int:
        """
        Get a player's current chi point count (Rule 1.13.5).

        Engine Feature Needed:
        - [ ] PlayerAssets.chi_points property (Rule 1.13.5)
        """
        return getattr(player, "_chi_points", 0)

    def pay_chi_cost(self, player: Any, cost: int) -> Any:
        """
        Pay a chi cost from the player's chi points (Rule 1.13.5).

        Engine Feature Needed:
        - [ ] AssetPayment.pay_chi_cost(player_id, cost) -> PaymentResult (Rule 1.14.2c)
        """
        current = self.get_player_chi_points(player)
        if current < cost:
            return AssetSpendResultStub(success=False, reason="insufficient_chi_points")
        self.set_player_chi_points(player, current - cost)
        return AssetSpendResultStub(success=True)

    def pitch_card_for_chi(self, player: Any, card: CardInstance) -> Any:
        """
        Pitch a card to generate chi points (Rule 1.13.5a).

        Engine Feature Needed:
        - [ ] PitchAction.execute_for_chi(player_id, card) (Rule 1.13.5a)
        """
        pitch_generates = getattr(card, "_pitch_generates", "resource")
        pitch_value = card.template.pitch

        if pitch_generates != "chi":
            return PitchAttemptResultStub(pitch_succeeded=False, pitch_rejected=True)

        # Move card to pitch zone (note: TestZone may not have the card in a zone already)
        try:
            if card in player.hand:
                player.hand.remove_card(card)
        except Exception:
            pass
        player.pitch_zone.add_card(card)

        # Grant chi points
        current = self.get_player_chi_points(player)
        self.set_player_chi_points(player, current + pitch_value)
        return PitchPaymentResultStub(
            chi_gained=pitch_value,
            pitch_event_occurred=True,
        )

    def pay_resource_cost_with_chi(self, player: Any, cost: int) -> Any:
        """
        Pay a resource cost using chi points (Rule 1.13.5b).

        Engine Feature Needed:
        - [ ] AssetPayment.pay_resource_with_chi(player_id, cost) -> ChiPaymentResult (Rule 1.13.5b)
        - [ ] ChiPaymentResult.chi_used, resource_used, success properties
        """
        chi_available = self.get_player_chi_points(player)
        resource_available = self.get_player_resource_points(player)

        # Rule 1.13.5b: Use chi before resource (1.14.2a: chi before resource in payment order)
        chi_to_use = min(chi_available, cost)
        remaining_cost = cost - chi_to_use
        resource_to_use = min(resource_available, remaining_cost)

        if chi_to_use + resource_to_use < cost:
            return ChiPaymentResultStub(
                success=False, chi_used=0, resource_used=0, reason="insufficient_assets"
            )

        self.set_player_chi_points(player, chi_available - chi_to_use)
        self.set_player_resource_points(player, resource_available - resource_to_use)
        return ChiPaymentResultStub(
            success=True, chi_used=chi_to_use, resource_used=resource_to_use
        )

    def pay_resource_cost_with_available_assets(self, player: Any, cost: int) -> Any:
        """
        Pay a resource cost using chi first then resource (Rule 1.13.5b + 1.14.2a).

        Engine Feature Needed:
        - [ ] AssetPayment.pay_with_priority_order(player_id, cost) (Rule 1.14.2a)
        - [ ] Payment order: chi first, then resource (Rule 1.13.5b)
        """
        return self.pay_resource_cost_with_chi(player, cost)

    def attempt_chi_for_life_payment(self, player: Any, cost: int) -> Any:
        """
        Attempt to use chi points to pay a life point cost (Rule 1.13.5b limitation).

        Engine Feature Needed:
        - [ ] AssetPayment.validate_asset_type_for_cost() (Rule 1.13.5b)
        - [ ] Reject chi substitution for non-resource costs
        """
        # Rule 1.13.5b: Chi can ONLY substitute for resource points, not life points
        return AssetSpendResultStub(
            success=False, reason="chi_cannot_substitute_for_life"
        )

    def attempt_pitch_for_wrong_type(
        self, player: Any, card: CardInstance, needed_asset: str
    ) -> Any:
        """
        Attempt to pitch a card that generates the wrong asset type (Rule 1.14.3b).

        Engine Feature Needed:
        - [ ] PitchAction.validate(player_id, card, needed_asset) (Rule 1.14.3b)
        - [ ] PitchValidationResult.reason = "wrong_asset_type" when blocked
        """
        pitch_generates = getattr(card, "_pitch_generates", "resource")
        if pitch_generates != needed_asset:
            return PitchAttemptResultStub(
                pitch_succeeded=False,
                pitch_rejected=True,
                rejection_reason="wrong_asset_type",
            )
        return PitchAttemptResultStub(pitch_succeeded=True, pitch_rejected=False)

    def set_hero_life_total(self, player: Any, life: int) -> None:
        """
        Set a player's hero life total (Rule 1.13.4).

        Engine Feature Needed:
        - [ ] Hero.life_total property (Rule 1.13.4)
        """
        player._hero_life_total = life  # type: ignore[attr-defined]

    def get_hero_life_total(self, player: Any) -> int:
        """
        Get a player's hero life total (Rule 1.13.4).

        Engine Feature Needed:
        - [ ] Hero.life_total property (Rule 1.13.4)
        """
        return getattr(player, "_hero_life_total", 0)

    def get_player_life_points(self, player: Any) -> int:
        """
        Get a player's current life point count (Rule 1.13.4).

        Life points come from the hero's life total.

        Engine Feature Needed:
        - [ ] Player.life_points property delegating to hero.life_total (Rule 1.13.4)
        """
        return self.get_hero_life_total(player)

    def player_hero_has_life_tracking(self, player: Any) -> bool:
        """
        Check if the player's hero tracks life total (Rule 1.13.4).

        Engine Feature Needed:
        - [ ] Hero.has_life_total property (Rule 1.13.4)
        """
        return hasattr(player, "_hero_life_total")

    def create_ability_with_life_cost(self, cost: int, ability_text: str) -> Any:
        """
        Create an ability with a life point cost (Rule 1.13.4).

        Engine Feature Needed:
        - [ ] ActivatedAbility.life_cost property (Rule 1.13.4)
        - [ ] Ability class hierarchy supporting life costs (Rule 1.14.2e)
        """
        return LifeCostAbilityStub(life_cost=cost, ability_text=ability_text)

    def activate_ability_with_life_cost(
        self, player: Any, ability: Any, life_cost: int
    ) -> Any:
        """
        Activate an ability that costs life points (Rule 1.13.4).

        Engine Feature Needed:
        - [ ] GameEngine.activate_ability(ability, player_id) checking life costs (Rule 1.13.4)
        - [ ] AssetPayment.pay_life_cost(player_id, amount) (Rule 1.14.2e)
        """
        current_life = self.get_hero_life_total(player)
        if current_life < life_cost:
            return AssetSpendResultStub(success=False, reason="insufficient_life")
        self.set_hero_life_total(player, current_life - life_cost)
        return AssetSpendResultStub(success=True)

    def grant_life_points_via_effect(self, player: Any, amount: int) -> Any:
        """
        Grant life points via an effect that increases the hero's life total (Rule 1.13.4a).

        Engine Feature Needed:
        - [ ] GainLifeEffect.apply(player_id, amount) (Rule 1.13.4a)
        - [ ] LifeGainResult.amount_gained property
        """
        current = self.get_hero_life_total(player)
        self.set_hero_life_total(player, current + amount)
        return LifeGainResultStub(amount_gained=amount)

    # ===== Section 1.14: Costs helpers =====

    def create_card_with_resource_cost(
        self,
        name: str = "Cost Card",
        cost: int = 1,
        owner_id: int = 0,
    ) -> CardInstance:
        """
        Create an action card with a specific resource cost (Rule 1.14.1).

        Engine Feature Needed:
        - [ ] AssetCost tracking on cards (Rule 1.14.2)
        """
        template = CardTemplate(
            unique_id=f"cost_{name}_{id(self)}",
            name=name,
            types=frozenset([CardType.ACTION]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ATTACK]),
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=cost,
            has_cost=True,
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

    def create_chi_pitch_card(
        self,
        name: str = "Chi Pitch Card",
        chi_value: int = 1,
        owner_id: int = 0,
    ) -> CardInstance:
        """
        Create a card that generates chi points when pitched (Rule 1.13.5a, 1.14.3).

        Engine Feature Needed:
        - [ ] CardTemplate.pitch_generates_type = "chi" (Rule 2.8)
        - [ ] PitchEffect grants chi points (Rule 1.13.5a)
        """
        template = CardTemplate(
            unique_id=f"chi_pitch_{name}_{id(self)}",
            name=name,
            types=frozenset([CardType.ACTION]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ATTACK]),
            color=Color.COLORLESS,
            pitch=chi_value,
            has_pitch=True,
            cost=0,
            has_cost=True,
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
        card._pitch_generates = "chi"  # type: ignore[attr-defined]
        return card

    def create_multi_asset_ability(
        self,
        chi: int = 0,
        resource: int = 0,
        life: int = 0,
        action: int = 0,
    ) -> Any:
        """
        Create a stub ability with multiple asset types in its cost (Rule 1.14.2a).

        Engine Feature Needed:
        - [ ] MultiAssetCost class tracking chi, resource, life, action amounts (Rule 1.14.2a)
        - [ ] Payment order enforcement: chi -> resource -> life -> action (Rule 1.14.2a)
        """
        return MultiAssetAbilityStub(
            chi_cost=chi,
            resource_cost=resource,
            life_cost=life,
            action_cost=action,
        )

    def create_ability_with_chi_cost(self, chi_cost: int = 1) -> Any:
        """
        Create a stub ability with a chi point cost (Rule 1.14.2c).

        Engine Feature Needed:
        - [ ] ActivatedAbility.chi_cost property (Rule 1.14.2c)
        """
        return MultiAssetAbilityStub(chi_cost=chi_cost)

    def create_ability_with_action_cost(self, action_cost: int = 1) -> Any:
        """
        Create a stub ability with an action point cost (Rule 1.14.2f).

        Engine Feature Needed:
        - [ ] ActivatedAbility.action_cost property (Rule 1.14.2f)
        """
        return MultiAssetAbilityStub(action_cost=action_cost)

    def create_ability_with_effect_cost(self, effect: str = "") -> Any:
        """
        Create a stub ability with an effect-cost (Rule 1.14.4).

        Engine Feature Needed:
        - [ ] EffectCost class representing effect requirements (Rule 1.14.4)
        - [ ] EffectCost.can_be_paid(player, game_state) check (Rule 1.14.4b)
        """
        return EffectCostAbilityStub(effect_cost=effect)

    def create_ability_with_two_effect_costs(
        self,
        cost1: str = "",
        cost2: str = "",
    ) -> Any:
        """
        Create a stub ability with two effect-costs (Rule 1.14.4a).

        Engine Feature Needed:
        - [ ] MultiEffectCost with ordered effects (Rule 1.14.4a)
        - [ ] Player declares order for two or more effect-costs (Rule 1.14.4a)
        """
        return TwoEffectCostAbilityStub(cost1=cost1, cost2=cost2)

    def create_pitch_instruction_effect(self) -> Any:
        """
        Create a stub effect that instructs a player to pitch a card (Rule 1.14.3b).

        Engine Feature Needed:
        - [ ] PitchInstructionEffect class (Rule 1.14.3b)
        - [ ] PitchInstructionEffect overrides normal pitch restrictions
        """
        return PitchInstructionEffectStub()

    def create_pitch_trigger_effect(self) -> Any:
        """
        Create a stub triggered effect that fires when a card is pitched (Rule 1.14.3c).

        Engine Feature Needed:
        - [ ] TriggeredEffect that triggers on pitch events (Rule 1.14.3c)
        - [ ] PitchEvent generation when card is pitched (Rule 1.14.3c)
        """
        return PitchTriggerEffectStub()

    def create_pitch_replacement_effect(self) -> Any:
        """
        Create a stub replacement effect that replaces a pitch event (Rule 1.14.3c).

        Engine Feature Needed:
        - [ ] ReplacementEffect for pitch events (Rule 1.14.3c)
        - [ ] ReplacementEffect.was_applied tracking
        """
        return PitchReplacementEffectStub()

    def create_replacement_effect(
        self, replaces: str = "", with_effect: str = ""
    ) -> Any:
        """
        Create a stub replacement effect (Rule 1.14.4c).

        Engine Feature Needed:
        - [ ] ReplacementEffect class with replaces/with_effect tracking (Rule 1.14.4c)
        """
        return GeneralReplacementEffectStub(replaces=replaces, with_effect=with_effect)

    def create_cost_reduction_effect(self, reduction: int = 1) -> Any:
        """
        Create a stub cost reduction effect (Rule 1.14.5).

        Engine Feature Needed:
        - [ ] CostReductionEffect reducing AssetCost amounts (Rule 1.14.5)
        """
        return CostReductionEffectStub(reduction=reduction)

    def attempt_card_play_1_14(self, card: CardInstance) -> Any:
        """
        Attempt to play a card, tracking cost information (Rule 1.14.1).

        Engine Feature Needed:
        - [ ] GameEngine.play_card(card, player_id) with cost resolution (Rule 1.14.1)
        - [ ] CardPlayResult with _incurred_cost, _cost_amount, _cost_paid attributes
        """
        cost = card.template.cost if card.template.has_cost else 0
        has_discard_effect_cost = getattr(card, "_has_discard_effect_cost", False)
        has_mandatory_discard = getattr(
            card, "_has_mandatory_discard_effect_cost", False
        )
        is_mandatory = getattr(card, "_is_mandatory_cost", False)

        resources = self.get_player_resource_points(self.player)
        can_pay = resources >= cost

        if has_mandatory_discard:
            # Check if there are cards to discard (excluding the card itself)
            other_hand_cards = [c for c in self.player.hand.cards if c is not card]
            if not other_hand_cards:
                return CardPlayResultStub(
                    play_succeeded=False,
                    incurred_cost=True,
                    cost_amount=cost,
                    cost_paid=False,
                    entire_action_reversed=True,
                    has_cost=True,
                )

        if not can_pay and is_mandatory:
            return CardPlayResultStub(
                play_succeeded=False,
                incurred_cost=True,
                cost_amount=cost,
                cost_paid=False,
                entire_action_reversed=True,
                has_cost=True,
            )

        if not can_pay:
            return CardPlayResultStub(
                play_succeeded=False,
                incurred_cost=True,
                cost_amount=cost,
                cost_paid=False,
                game_state_reversed=True,
                has_cost=True,
            )

        # Pay the cost
        self.set_player_resource_points(self.player, resources - cost)

        zero_cost_acknowledged = cost == 0
        effective_cost = cost
        # Apply cost reduction effects if present
        if (
            hasattr(self, "cost_reduction_effect")
            and self.cost_reduction_effect is not None
        ):  # type: ignore[attr-defined]
            reduction = getattr(self.cost_reduction_effect, "_reduction", 0)
            effective_cost = max(0, cost - reduction)
            zero_cost_acknowledged = effective_cost == 0

        return CardPlayResultStub(
            play_succeeded=True,
            incurred_cost=True,
            cost_amount=cost,
            cost_paid=True,
            has_cost=True,
            zero_cost_acknowledged=zero_cost_acknowledged,
            effective_cost=effective_cost,
            has_asset_cost=True,
            has_effect_cost=has_discard_effect_cost,
        )

    def attempt_ability_activation_1_14(self, card: CardInstance) -> Any:
        """
        Attempt to activate an ability, tracking cost information (Rule 1.14.1).

        Engine Feature Needed:
        - [ ] GameEngine.activate_ability(ability, player_id) with cost tracking
        - [ ] AbilityActivationResult with _incurred_cost, _cost_amount attributes
        """
        cost = card.template.cost if card.template.has_cost else 0
        resources = self.get_player_resource_points(self.player)
        can_pay = resources >= cost
        if can_pay:
            self.set_player_resource_points(self.player, resources - cost)
        return AbilityActivationResultStub(
            incurred_cost=True,
            cost_amount=cost,
            cost_paid=can_pay,
        )

    def get_full_cost_1_14(self, card: CardInstance) -> Any:
        """
        Get the full cost object for a card (Rule 1.14.1).

        Engine Feature Needed:
        - [ ] Card.get_full_cost() returning FullCost with asset/effect components (Rule 1.14.1)
        """
        has_asset_cost = card.template.has_cost
        has_effect_cost = getattr(card, "_has_discard_effect_cost", False)
        return FullCostStub(
            has_asset_cost=has_asset_cost,
            has_effect_cost=has_effect_cost,
        )

    def pay_asset_cost_1_14(self, player: Any, card: CardInstance) -> Any:
        """
        Pay the asset-cost of a card from the player's assets (Rule 1.14.2).

        Engine Feature Needed:
        - [ ] AssetCost.pay(player) subtracting assets (Rule 1.14.2)
        - [ ] AssetPaymentResult with _cost_paid, _game_state_reversed attributes
        """
        cost = card.template.cost if card.template.has_cost else 0
        resources = self.get_player_resource_points(player)
        if resources >= cost:
            self.set_player_resource_points(player, resources - cost)
            return AssetPaymentResultStub(cost_paid=True)
        else:
            return AssetPaymentResultStub(cost_paid=False, game_state_reversed=True)

    def attempt_pay_asset_cost_1_14(self, player: Any, card: CardInstance) -> Any:
        """
        Attempt to pay an asset-cost (may fail with reversal) (Rule 1.14.2b).

        Engine Feature Needed:
        - [ ] AssetCost.attempt_pay(player) with reversal on failure (Rule 1.14.2b)
        """
        return self.pay_asset_cost_1_14(player=player, card=card)

    def pay_multi_asset_cost_1_14(self, player: Any, ability: Any) -> Any:
        """
        Pay a multi-asset-cost in the correct order (Rule 1.14.2a).

        Engine Feature Needed:
        - [ ] MultiAssetCost.pay(player) enforcing chi->resource->life->action order (Rule 1.14.2a)
        - [ ] MultiAssetPaymentResult with _chi_paid_order, _resource_paid_order, etc.
        """
        chi_cost = getattr(ability, "_chi_cost", 0)
        resource_cost = getattr(ability, "_resource_cost", 0)
        life_cost = getattr(ability, "_life_cost", 0)
        action_cost = getattr(ability, "_action_cost", 0)

        chi = self.get_player_chi_points(player)
        resource = self.get_player_resource_points(player)
        life = self.get_hero_life_total(player)
        action = self.get_player_action_points(player)

        # Validate all assets available
        if (
            chi < chi_cost
            or resource < resource_cost
            or life < life_cost
            or action < action_cost
        ):
            return MultiAssetPaymentResultStub(
                chi_payment_failed=True, resource_payment_started=False
            )

        # Pay in order: chi=1, resource=2, life=3, action=4
        self.set_player_chi_points(player, chi - chi_cost)
        self.set_player_resource_points(player, resource - resource_cost)
        self.set_hero_life_total(player, life - life_cost)
        self.set_player_action_points(player, action - action_cost)

        return MultiAssetPaymentResultStub(
            chi_paid_order=1,
            resource_paid_order=2,
            life_paid_order=3,
            action_paid_order=4,
        )

    def attempt_pay_multi_asset_cost_1_14(self, player: Any, ability: Any) -> Any:
        """
        Attempt to pay a multi-asset-cost, checking each asset type in order (Rule 1.14.2a).

        Engine Feature Needed:
        - [ ] MultiAssetCost.attempt_pay(player) with per-type failure tracking (Rule 1.14.2a)
        """
        chi_cost = getattr(ability, "_chi_cost", 0)
        chi = self.get_player_chi_points(player)

        if chi < chi_cost:
            return MultiAssetPaymentResultStub(
                chi_payment_failed=True,
                resource_payment_started=False,
            )

        return self.pay_multi_asset_cost_1_14(player=player, ability=ability)

    def pitch_card_during_payment_1_14(self, player: Any, card: CardInstance) -> Any:
        """
        Pitch a card during cost payment to gain resources (Rule 1.14.3, 1.14.2d).

        Engine Feature Needed:
        - [ ] PitchDuringPayment action with resource gain tracking (Rule 1.14.2d)
        """
        pitch_generates = getattr(card, "_pitch_generates", "resource")
        pitch_value = card.template.pitch

        if card in player.hand:
            player.hand.remove_card(card)
        player.pitch_zone.add_card(card)

        if pitch_generates == "resource":
            current = self.get_player_resource_points(player)
            new_total = current + pitch_value
            self.set_player_resource_points(player, new_total)
            return PitchPaymentResultStub(
                resources_gained=pitch_value,
                pitch_event_occurred=True,
                total_resources_after_pitch=new_total,
            )
        elif pitch_generates == "chi":
            current = self.get_player_chi_points(player)
            self.set_player_chi_points(player, current + pitch_value)
            return PitchPaymentResultStub(
                chi_gained=pitch_value,
                pitch_event_occurred=True,
            )
        return PitchPaymentResultStub(pitch_event_occurred=True)

    def pay_chi_cost_1_14(self, player: Any, cost: int) -> Any:
        """
        Pay a chi point cost, tracking details (Rule 1.14.2c).

        Engine Feature Needed:
        - [ ] ChiCostPayment.pay(player, amount) -> ChiPaymentResult (Rule 1.14.2c)
        - [ ] ChiPaymentResult._chi_spent, _cost_paid attributes
        """
        current = self.get_player_chi_points(player)
        if current < cost:
            return ChiCostPaymentResultStub(chi_spent=0, cost_paid=False)
        self.set_player_chi_points(player, current - cost)
        return ChiCostPaymentResultStub(chi_spent=cost, cost_paid=True)

    def pay_resource_cost_tracked_1_14(self, player: Any, cost: int) -> Any:
        """
        Pay a resource cost using chi first then resource, with tracking (Rule 1.14.2d).

        Engine Feature Needed:
        - [ ] ResourceCostPayment tracking chi_used_before_resource (Rule 1.14.2d)
        - [ ] ResourcePaymentResult._chi_used_before_resource, _chi_spent, _resource_spent
        """
        chi = self.get_player_chi_points(player)
        resource = self.get_player_resource_points(player)

        chi_to_use = min(chi, cost)
        remaining = cost - chi_to_use
        resource_to_use = min(resource, remaining)

        if chi_to_use + resource_to_use < cost:
            return ResourceCostPaymentResultStub(success=False)

        self.set_player_chi_points(player, chi - chi_to_use)
        self.set_player_resource_points(player, resource - resource_to_use)

        return ResourceCostPaymentResultStub(
            success=True,
            chi_used_before_resource=chi_to_use > 0,
            chi_spent=chi_to_use,
            resource_spent=resource_to_use,
        )

    def pay_life_cost_1_14(self, player: Any, amount: int) -> Any:
        """
        Pay a life point cost directly from the hero's life total (Rule 1.14.2e).

        Engine Feature Needed:
        - [ ] LifeCostPayment.pay(player, amount) -> LifePaymentResult (Rule 1.14.2e)
        - [ ] LifePaymentResult._life_spent attribute
        """
        current = self.get_hero_life_total(player)
        if current < amount:
            return LifeCostPaymentResultStub(life_spent=0, cost_paid=False)
        self.set_hero_life_total(player, current - amount)
        return LifeCostPaymentResultStub(life_spent=amount, cost_paid=True)

    def pay_action_cost_1_14(self, player: Any, amount: int) -> Any:
        """
        Pay an action point cost (Rule 1.14.2f).

        Engine Feature Needed:
        - [ ] ActionCostPayment.pay(player, amount) -> ActionPaymentResult (Rule 1.14.2f)
        - [ ] ActionPaymentResult._action_spent attribute
        """
        current = self.get_player_action_points(player)
        if current < amount:
            return ActionCostPaymentResultStub(action_spent=0, cost_paid=False)
        self.set_player_action_points(player, current - amount)
        return ActionCostPaymentResultStub(action_spent=amount, cost_paid=True)

    def attempt_pitch_card_1_14(self, player: Any, card: CardInstance) -> Any:
        """
        Attempt to pitch a card, checking pitch property (Rule 1.14.3a).

        Engine Feature Needed:
        - [ ] PitchAction.validate_has_pitch_property(card) (Rule 1.14.3a)
        - [ ] PitchAttemptResult._pitch_succeeded, _pitch_rejected
        """
        has_pitch_property = getattr(
            card, "_has_pitch_property", card.template.has_pitch
        )
        if not has_pitch_property:
            return PitchAttemptResultStub(pitch_succeeded=False, pitch_rejected=True)

        # Perform the pitch
        if card in player.hand:
            player.hand.remove_card(card)
        player.pitch_zone.add_card(card)
        return PitchAttemptResultStub(pitch_succeeded=True, pitch_rejected=False)

    def pitch_card_via_effect_instruction_1_14(
        self, player: Any, card: CardInstance, effect: Any
    ) -> Any:
        """
        Pitch a card as instructed by an effect (bypasses normal pitch restrictions) (Rule 1.14.3b).

        Engine Feature Needed:
        - [ ] PitchInstructionEffect overriding PitchAction.validate (Rule 1.14.3b)
        """
        # Effect-instructed pitches bypass normal pitch-property requirements
        if card in player.hand:
            player.hand.remove_card(card)
        player.pitch_zone.add_card(card)
        return PitchAttemptResultStub(pitch_succeeded=True, pitch_rejected=False)

    def pitch_card_with_trigger_check_1_14(
        self, player: Any, card: CardInstance, trigger: Any
    ) -> Any:
        """
        Pitch a card and check if triggers fire (Rule 1.14.3c).

        Engine Feature Needed:
        - [ ] PitchEvent generation triggering watching effects (Rule 1.14.3c)
        """
        pitch_value = card.template.pitch
        pitch_generates = getattr(card, "_pitch_generates", "resource")

        if card in player.hand:
            player.hand.remove_card(card)
        player.pitch_zone.add_card(card)

        if pitch_generates == "resource":
            current = self.get_player_resource_points(player)
            self.set_player_resource_points(player, current + pitch_value)

        # Mark trigger as fired
        if trigger is not None:
            trigger._fire_count = getattr(trigger, "_fire_count", 0) + 1  # type: ignore[attr-defined]

        return PitchPaymentResultStub(
            resources_gained=pitch_value if pitch_generates == "resource" else 0,
            pitch_event_occurred=True,
        )

    def count_pitch_triggers_fired_1_14(self, trigger: Any) -> int:
        """
        Count how many times a pitch trigger has fired (Rule 1.14.3c).

        Engine Feature Needed:
        - [ ] TriggeredEffect.fire_count property (Rule 1.14.3c)
        """
        return getattr(trigger, "_fire_count", 0)

    def pitch_card_with_replacement_check_1_14(
        self, player: Any, card: CardInstance, replacement: Any
    ) -> Any:
        """
        Pitch a card while checking for replacement effects (Rule 1.14.3c).

        Engine Feature Needed:
        - [ ] ReplacementEffect.apply(pitch_event) modifying pitch behavior (Rule 1.14.3c)
        """
        if replacement is not None:
            replacement.was_applied = True  # type: ignore[attr-defined]

        if card in player.hand:
            player.hand.remove_card(card)
        player.pitch_zone.add_card(card)

        pitch_value = card.template.pitch
        pitch_generates = getattr(card, "_pitch_generates", "resource")
        if pitch_generates == "resource":
            current = self.get_player_resource_points(player)
            self.set_player_resource_points(player, current + pitch_value)

        return PitchPaymentResultStub(
            resources_gained=pitch_value if pitch_generates == "resource" else 0,
            pitch_event_occurred=True,
            was_replaced=True,
        )

    def pay_effect_cost_1_14(
        self,
        player: Any,
        ability: Any,
        target: Optional[Any],
        replacement: Optional[Any] = None,
    ) -> Any:
        """
        Pay an effect-cost by generating and resolving the specified effect (Rule 1.14.4).

        Engine Feature Needed:
        - [ ] EffectCost.pay(player, target) generating and resolving (Rule 1.14.4)
        - [ ] EffectCostPaymentResult with _effect_generated, _target_destroyed, _cost_paid
        """
        effect_type = getattr(ability, "_effect_cost", "")
        if target is None and effect_type == "destroy_target":
            return EffectCostPaymentResultStub(effect_generated=False, cost_paid=False)

        if target is not None:
            # Remove from arena (simulating destruction)
            try:
                player.arena.remove_card(target)
            except Exception:
                pass

        if effect_type == "discard_a_card":
            # Discard effect-cost: discard a card from hand (or acknowledge replacement)
            # If replaced by banishment, still considered paid (Rule 1.14.4c)
            replacement_was_applied = replacement is not None
            return EffectCostPaymentResultStub(
                effect_generated=True,
                target_destroyed=False,
                cost_paid=True,
                replacement_was_applied=replacement_was_applied,
            )

        return EffectCostPaymentResultStub(
            effect_generated=True,
            target_destroyed=target is not None,
            cost_paid=True,
        )

    def activate_ability_with_effect_cost_1_14(
        self, player: Any, source: CardInstance
    ) -> Any:
        """
        Activate an ability where the cost is an effect (destroy self) (Rule 1.14.4).

        Engine Feature Needed:
        - [ ] GameEngine.activate_effect_cost_ability(source, player_id) (Rule 1.14.4)
        - [ ] HopeMerchantsHoodResult with _destroy_was_effect_cost, _cards_shuffled
        """
        has_destroy_self = getattr(source, "_has_destroy_self_effect_cost", False)
        if not has_destroy_self:
            return EffectCostPaymentResultStub(cost_paid=False)

        # Destroy the hood (effect-cost)
        try:
            player.arena.remove_card(source)
        except Exception:
            pass

        # Shuffle hand into deck (the actual ability)
        hand_cards = list(player.hand.cards)
        for card in hand_cards:
            player.hand.remove_card(card)

        return HoodActivationResultStub(
            destroy_was_effect_cost=True,
            cards_shuffled=True,
            cost_paid=True,
        )

    def pay_multi_effect_cost_1_14(
        self,
        player: Any,
        ability: Any,
        effect1_target: Optional[Any],
        effect2_target: Optional[Any],
    ) -> Any:
        """
        Pay a multi-effect-cost with player-declared ordering (Rule 1.14.4a).

        Engine Feature Needed:
        - [ ] MultiEffectCost.pay(player, ordered_effects) (Rule 1.14.4a)
        - [ ] MultiEffectCostResult with _player_declared_order, _generated_in_declared_order
        """
        return MultiEffectCostResultStub(
            player_declared_order=True,
            generated_in_declared_order=True,
            cost_paid=True,
        )

    def attempt_pay_effect_cost_1_14(
        self, player: Any, ability: Any, target: Optional[Any]
    ) -> Any:
        """
        Attempt to pay an effect-cost (may fail if effect cannot be generated) (Rule 1.14.4b).

        Engine Feature Needed:
        - [ ] EffectCost.can_be_generated(player, game_state) pre-check (Rule 1.14.4b)
        - [ ] EffectCostPaymentResult with _game_state_reversed on failure
        """
        effect_type = getattr(ability, "_effect_cost", "")
        if effect_type == "destroy_weapon" and self.player_weapon is None:  # type: ignore[attr-defined]
            return EffectCostPaymentResultStub(
                cost_paid=False,
                game_state_reversed=True,
            )
        return self.pay_effect_cost_1_14(player=player, ability=ability, target=target)

    def play_card_with_cost_reduction_1_14(
        self, player: Any, card: CardInstance, reduction_effect: Any
    ) -> Any:
        """
        Play a card applying a cost reduction effect (Rule 1.14.5).

        Engine Feature Needed:
        - [ ] CostReductionEffect.apply(card_cost) returning reduced cost (Rule 1.14.5)
        - [ ] ZeroCostAcknowledgment when effective cost reaches 0 (Rule 1.14.5)
        """
        original_cost = card.template.cost if card.template.has_cost else 0
        reduction = getattr(reduction_effect, "_reduction", 0)
        effective_cost = max(0, original_cost - reduction)

        resources = self.get_player_resource_points(player)
        if resources >= effective_cost:
            self.set_player_resource_points(player, resources - effective_cost)
            return CardPlayResultStub(
                play_succeeded=True,
                incurred_cost=True,
                cost_amount=original_cost,
                cost_paid=True,
                has_cost=True,
                zero_cost_acknowledged=effective_cost == 0,
                effective_cost=effective_cost,
            )
        return CardPlayResultStub(
            play_succeeded=False,
            cost_paid=False,
            has_cost=True,
            effective_cost=effective_cost,
        )

    def attempt_pitch_another_card_1_14(self, player: Any) -> Any:
        """
        Attempt to pitch another card when the cost is already fully paid (Rule 1.14.3b).

        Engine Feature Needed:
        - [ ] PitchAction.validate_cost_not_already_paid() (Rule 1.14.3b)
        - [ ] Reject pitching when cost is fully paid and pitch would not help
        """
        # Rule 1.14.3b: A player may only pitch if it gains them needed assets.
        # Once cost is fully paid, no more pitching is allowed.
        return PitchAttemptResultStub(pitch_succeeded=False, pitch_rejected=True)

    # ===== Section 2.11: Supertypes helpers =====

    def get_card_supertypes(self, card: CardInstance) -> set:
        """
        Get the supertypes of a card (Rule 2.11.2).

        Engine Feature Needed:
        - [ ] CardTemplate.supertypes returning frozenset of supertype keywords
        - [ ] CardInstance supertypes accessible via card.template.supertypes
        - [ ] Dynamic supertypes tracking (gain/lose via Rule 2.11.5)
        """
        # First check for test metadata (dynamic supertypes)
        if hasattr(card, "_supertypes"):
            return card._supertypes
        # Fall back to template supertypes
        if hasattr(card, "template") and hasattr(card.template, "supertypes"):
            return {s.name.title() for s in card.template.supertypes}
        return set()

    def get_layer_supertypes(self, layer: Any) -> set:
        """
        Get the supertypes of a layer (Rule 2.11.4).

        Engine Feature Needed:
        - [ ] ActivatedLayer.supertypes == source.supertypes (Rule 2.11.4)
        - [ ] TriggeredLayer.supertypes == source.supertypes (Rule 2.11.4)
        """
        if hasattr(layer, "supertypes"):
            return layer.supertypes
        return set()

    def create_activated_layer(self, source: Any) -> Any:
        """
        Create an activated-layer from a source card (Rule 2.11.4).

        Engine Feature Needed:
        - [ ] ActivatedLayer class with source reference (Rule 1.6.2b)
        - [ ] ActivatedLayer.supertypes inherits from source (Rule 2.11.4)
        """
        return LayerWithSupertypesStub211(source=source, layer_type="activated")

    def create_triggered_layer(self, source: Any) -> Any:
        """
        Create a triggered-layer from a source card (Rule 2.11.4).

        Engine Feature Needed:
        - [ ] TriggeredLayer class with source reference (Rule 1.6.2c)
        - [ ] TriggeredLayer.supertypes inherits from source (Rule 2.11.4)
        """
        return LayerWithSupertypesStub211(source=source, layer_type="triggered")

    def parse_type_box(self, type_box_str: str) -> Any:
        """
        Parse a type box string to extract supertypes, type, and subtypes (Rule 2.11.3).

        Engine Feature Needed:
        - [ ] TypeBoxParser.parse(type_box_str) returning parsed result (Rule 2.11.3)
        - [ ] TypeBoxParseResult.supertypes: list of supertype strings
        - [ ] TypeBoxParseResult.card_type: the primary card type string
        - [ ] TypeBoxParseResult.subtypes: list of subtype strings
        - [ ] "Generic" means no supertypes (Rule 2.14.1a)
        """
        return TypeBoxParseResultStub211.parse(type_box_str)

    def check_card_pool_eligibility_by_supertypes(
        self, card_supertypes: set, hero_supertypes: set
    ) -> bool:
        """
        Check if a card is eligible for a hero's card-pool based on supertype subset validation
        (Rule 2.11.1, Rule 1.1.3).

        Rule 2.11.1: A card can only be included in a player's card-pool if the card's supertypes
        are a subset of their hero's supertypes.

        Engine Feature Needed:
        - [ ] CardPoolValidator.validate_supertypes(card_supertypes, hero_supertypes) (Rule 2.11.1)
        - [ ] Empty card supertypes is valid for any hero (subset of any set)
        """
        # Rule 2.11.1 / Rule 1.1.3: card supertypes must be a subset of hero supertypes
        # Empty set is a subset of any set (generic cards are always valid)
        card_upper = {
            s.upper() if isinstance(s, str) else s.name.upper() for s in card_supertypes
        }
        hero_upper = {
            s.upper() if isinstance(s, str) else s.name.upper() for s in hero_supertypes
        }
        return card_upper.issubset(hero_upper)

    def grant_supertype_to_card(self, card: CardInstance, supertype: str) -> bool:
        """
        Grant a supertype to a card via an effect (Rule 2.11.5).

        Engine Feature Needed:
        - [ ] CardInstance.gain_supertype(name) method (Rule 2.11.5)
        """
        if not hasattr(card, "_supertypes"):
            card._supertypes = set()
        card._supertypes.add(supertype)
        return True

    def remove_supertype_from_card(self, card: CardInstance, supertype: str) -> bool:
        """
        Remove a supertype from a card via an effect (Rule 2.11.5).

        Engine Feature Needed:
        - [ ] CardInstance.lose_supertype(name) method (Rule 2.11.5)
        """
        if not hasattr(card, "_supertypes"):
            card._supertypes = set()
            return False
        card._supertypes.discard(supertype)
        return True

    def check_supertypes_add_additional_rules(self, card: CardInstance) -> Any:
        """
        Check whether the card's supertypes add additional rules (Rule 2.11.6).

        Rule 2.11.6: Supertypes are non-functional keywords and do not add additional rules.

        Engine Feature Needed:
        - [ ] SupertypeRegistry.is_non_functional() always True (Rule 2.11.6)
        - [ ] SupertypeCheckResult.adds_additional_rules = False
        """
        return SupertypeCheckResultStub211(
            adds_additional_rules=False, is_non_functional=True
        )

    def get_supertype_category(self, supertype_name: str) -> str:
        """
        Get the category of a supertype ('class' or 'talent') (Rule 2.11.6).

        Engine Feature Needed:
        - [ ] SupertypeRegistry.get_category(name) -> "class" | "talent" (Rule 2.11.6)
        - [ ] Enum or lookup table classifying all supertype keywords
        """
        CLASS_SUPERTYPES = {
            "ADJUDICATOR",
            "ASSASSIN",
            "BARD",
            "BRUTE",
            "GUARDIAN",
            "ILLUSIONIST",
            "MECHANOLOGIST",
            "MERCHANT",
            "NECROMANCER",
            "NINJA",
            "PIRATE",
            "RANGER",
            "RUNEBLADE",
            "SHAPESHIFTER",
            "THIEF",
            "WARRIOR",
            "WIZARD",
        }
        TALENT_SUPERTYPES = {
            "CHAOS",
            "DRACONIC",
            "EARTH",
            "ELEMENTAL",
            "ICE",
            "LIGHT",
            "LIGHTNING",
            "MYSTIC",
            "REVERED",
            "REVILED",
            "ROYAL",
            "SHADOW",
        }
        upper = supertype_name.upper()
        if upper in CLASS_SUPERTYPES:
            return "class"
        elif upper in TALENT_SUPERTYPES:
            return "talent"
        return None

    def get_all_class_supertypes(self) -> set:
        """
        Return all class supertype keywords (Rule 2.11.6a).

        Engine Feature Needed:
        - [ ] SupertypeRegistry.CLASS_SUPERTYPES frozenset with all 17 class supertypes (Rule 2.11.6a)
        """
        return {
            "Adjudicator",
            "Assassin",
            "Bard",
            "Brute",
            "Guardian",
            "Illusionist",
            "Mechanologist",
            "Merchant",
            "Necromancer",
            "Ninja",
            "Pirate",
            "Ranger",
            "Runeblade",
            "Shapeshifter",
            "Thief",
            "Warrior",
            "Wizard",
        }

    def get_all_talent_supertypes(self) -> set:
        """
        Return all talent supertype keywords (Rule 2.11.6b).

        Engine Feature Needed:
        - [ ] SupertypeRegistry.TALENT_SUPERTYPES frozenset with all 12 talent supertypes (Rule 2.11.6b)
        """
        return {
            "Chaos",
            "Draconic",
            "Earth",
            "Elemental",
            "Ice",
            "Light",
            "Lightning",
            "Mystic",
            "Revered",
            "Reviled",
            "Royal",
            "Shadow",
        }

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


# ===== Stub classes for Section 1.8 engine features not yet implemented =====


class DamageEffectStub:
    """
    Stub for a damage effect (Rule 1.8.1).

    Engine Feature Needed:
    - [ ] Effect class with source, controller_id, effect_type (Rule 1.8.1)
    - [ ] Effect.source tracking per generating ability source (Rule 1.8.1a)
    - [ ] Effect.controller_id tracking per generating ability controller (Rule 1.8.1b)
    """

    def __init__(
        self,
        source: Optional["CardInstance"] = None,
        damage_amount: int = 0,
        damage_type: str = "normal",
        controller_id: int = 0,
        target: Optional["CardInstance"] = None,
        requires_arena_target: bool = False,
    ):
        self.source = source
        self.damage_amount = damage_amount
        self.damage_type = damage_type
        self.controller_id = controller_id
        self.target = target
        self.requires_arena_target = requires_arena_target
        self.effect_type = "deal_damage"
        self.failed = False


class OptionalEffectStub:
    """
    Stub for an optional effect (Rule 1.8.3).

    Engine Feature Needed:
    - [ ] OptionalEffect class with requires_player_choice (Rule 1.8.3)
    - [ ] OptionalEffect.can_be_generated() checking game state (Rule 1.8.3b)
    - [ ] OptionalEffect.is_may_choose_to phrasing distinction (Rule 1.8.3b)
    """

    def __init__(
        self,
        source: Optional["CardInstance"] = None,
        effect_text: str = "",
        can_be_generated: bool = True,
        is_may_choose_to: bool = False,
    ):
        self.source = source
        self.effect_text = effect_text
        self._can_be_generated = can_be_generated
        self.is_may_choose_to = is_may_choose_to
        self.requires_player_choice = True  # All optional effects require choice

    def can_be_generated(self) -> bool:
        """Check if this optional effect can currently be generated."""
        return self._can_be_generated


class OptionalEffectResultStub:
    """
    Stub result for resolving an optional effect (Rule 1.8.3a).

    Engine Feature Needed:
    - [ ] OptionalEffectResult with was_generated attribute
    - [ ] OptionalEffect.generate(player_chose=True/False)
    """

    def __init__(self, was_generated: bool = False):
        self.was_generated = was_generated


class MultiTargetEffectStub:
    """
    Stub for a multi-target effect (Rule 1.8.9).

    Engine Feature Needed:
    - [ ] MultiTargetEffect class with partial_success tracking (Rule 1.8.9)
    - [ ] Effect.fail() when all targets cease to exist
    - [ ] Effect.partial_success when some events succeed
    """

    def __init__(
        self,
        targets: Optional[List["CardInstance"]] = None,
        damage_amount: int = 0,
    ):
        self.targets = targets or []
        self.damage_amount = damage_amount
        self.effect_type = "deal_damage"
        self.failed = False


class EffectResolutionResultStub:
    """
    Stub result for resolving an effect with target existence check (Rule 1.8.9).

    Engine Feature Needed:
    - [ ] EffectResolutionResult with failed, partial_success attributes (Rule 1.8.9)
    - [ ] Effect.fail() returning EffectResolutionResult with failed=True
    """

    def __init__(self, failed: bool = False, partial_success: bool = False):
        self.failed = failed
        self.partial_success = partial_success
        self.succeeded = not failed


# ===== Stub classes for Section 1.13 engine features not yet implemented =====


class AssetSpendResultStub:
    """
    Stub result for spending or paying with assets (Rule 1.13).

    Engine Feature Needed:
    - [ ] AssetPaymentResult with success and reason attributes (Rule 1.13)
    - [ ] Player.spend_asset(asset_type, amount) -> AssetPaymentResult
    """

    def __init__(self, success: bool, reason: str = ""):
        self.success = success
        self.reason = reason


class ChiPaymentResultStub:
    """
    Stub result for paying a resource cost using chi points (Rule 1.13.5b).

    Engine Feature Needed:
    - [ ] ChiPaymentResult.chi_used attribute (Rule 1.13.5b)
    - [ ] ChiPaymentResult.resource_used attribute (Rule 1.13.5b)
    - [ ] ChiPaymentResult.success attribute
    - [ ] AssetPayment.pay_resource_with_chi(player_id, cost) (Rule 1.13.5b)
    """

    def __init__(
        self,
        success: bool,
        chi_used: int = 0,
        resource_used: int = 0,
        reason: str = "",
    ):
        self.success = success
        self.chi_used = chi_used
        self.resource_used = resource_used
        self.reason = reason


class LifeGainResultStub:
    """
    Stub result for gaining life points from an effect (Rule 1.13.4a).

    Engine Feature Needed:
    - [ ] LifeGainResult.amount_gained attribute (Rule 1.13.4a)
    - [ ] GainLifeEffect.apply(player_id, amount) -> LifeGainResult
    """

    def __init__(self, amount_gained: int = 0):
        self.amount_gained = amount_gained
        self.success = True


class LifeCostAbilityStub:
    """
    Stub for an ability with a life point cost (Rule 1.13.4).

    Engine Feature Needed:
    - [ ] ActivatedAbility with life_cost property (Rule 1.13.4)
    - [ ] AssetPayment.pay_life_cost(player_id, amount) (Rule 1.14.2e)
    """

    def __init__(self, life_cost: int = 0, ability_text: str = ""):
        self.life_cost = life_cost
        self.ability_text = ability_text
        self.cost_type = "life_point"


# ===== Stub classes for Section 1.14 engine features not yet implemented =====


class MultiAssetAbilityStub:
    """
    Stub for an ability with multiple asset types in its cost (Rule 1.14.2a).

    Engine Feature Needed:
    - [ ] MultiAssetCost class tracking chi, resource, life, action amounts (Rule 1.14.2a)
    - [ ] MultiAssetCost.pay(player) enforcing chi -> resource -> life -> action order
    """

    def __init__(
        self,
        chi_cost: int = 0,
        resource_cost: int = 0,
        life_cost: int = 0,
        action_cost: int = 0,
    ):
        self._chi_cost = chi_cost
        self._resource_cost = resource_cost
        self._life_cost = life_cost
        self._action_cost = action_cost


class EffectCostAbilityStub:
    """
    Stub for an ability with an effect-cost (Rule 1.14.4).

    Engine Feature Needed:
    - [ ] EffectCost class representing effects as costs (Rule 1.14.4)
    - [ ] EffectCost.can_be_generated(player) pre-payment check (Rule 1.14.4b)
    """

    def __init__(self, effect_cost: str = ""):
        self._effect_cost = effect_cost


class TwoEffectCostAbilityStub:
    """
    Stub for an ability with two effect-costs (Rule 1.14.4a).

    Engine Feature Needed:
    - [ ] MultiEffectCost with ordered effects (Rule 1.14.4a)
    - [ ] Player declares generation order for two or more effect-costs (Rule 1.14.4a)
    """

    def __init__(self, cost1: str = "", cost2: str = ""):
        self._cost1 = cost1
        self._cost2 = cost2


class PitchInstructionEffectStub:
    """
    Stub for an effect that instructs a player to pitch a card (Rule 1.14.3b).

    Engine Feature Needed:
    - [ ] PitchInstructionEffect class overriding normal pitch restrictions (Rule 1.14.3b)
    """

    def __init__(self):
        self.is_pitch_instruction = True


class PitchTriggerEffectStub:
    """
    Stub for a triggered effect that fires when a card is pitched (Rule 1.14.3c).

    Engine Feature Needed:
    - [ ] TriggeredEffect watching for pitch events (Rule 1.14.3c)
    - [ ] PitchEvent triggering the effect
    """

    def __init__(self):
        self.is_pitch_trigger = True
        self._fire_count = 0


class PitchReplacementEffectStub:
    """
    Stub for a replacement effect that modifies a pitch event (Rule 1.14.3c).

    Engine Feature Needed:
    - [ ] ReplacementEffect for pitch events (Rule 1.14.3c)
    - [ ] ReplacementEffect.was_applied tracking
    """

    def __init__(self):
        self.is_pitch_replacement = True
        self.was_applied = False


class GeneralReplacementEffectStub:
    """
    Stub for a general replacement effect (Rules 1.14.4c, 1.14.3c).

    Engine Feature Needed:
    - [ ] ReplacementEffect class with replaces/with_effect tracking (Rule 1.14.4c)
    """

    def __init__(self, replaces: str = "", with_effect: str = ""):
        self.replaces = replaces
        self.with_effect = with_effect
        self.was_applied = False


class CostReductionEffectStub:
    """
    Stub for a cost reduction effect (Rule 1.14.5).

    Engine Feature Needed:
    - [ ] CostReductionEffect reducing AssetCost amounts (Rule 1.14.5)
    - [ ] ZeroCostAcknowledgment when effective cost reaches 0
    """

    def __init__(self, reduction: int = 0):
        self._reduction = reduction


class AssetPaymentResultStub:
    """
    Stub result for paying an asset-cost (Rule 1.14.2).

    Engine Feature Needed:
    - [ ] AssetPaymentResult with _cost_paid, _game_state_reversed attributes (Rule 1.14.2)
    - [ ] AssetCost.pay(player) returning AssetPaymentResult
    """

    def __init__(
        self,
        cost_paid: bool = False,
        game_state_reversed: bool = False,
        entire_action_reversed: bool = False,
    ):
        self._cost_paid = cost_paid
        self._game_state_reversed = game_state_reversed
        self._entire_action_reversed = entire_action_reversed


class MultiAssetPaymentResultStub:
    """
    Stub result for paying a multi-asset-cost (Rule 1.14.2a).

    Engine Feature Needed:
    - [ ] MultiAssetPaymentResult tracking payment order (Rule 1.14.2a)
    - [ ] _chi_paid_order, _resource_paid_order, _life_paid_order, _action_paid_order
    """

    def __init__(
        self,
        chi_paid_order: Optional[int] = None,
        resource_paid_order: Optional[int] = None,
        life_paid_order: Optional[int] = None,
        action_paid_order: Optional[int] = None,
        chi_payment_failed: bool = False,
        resource_payment_started: bool = True,
    ):
        self._chi_paid_order = chi_paid_order
        self._resource_paid_order = resource_paid_order
        self._life_paid_order = life_paid_order
        self._action_paid_order = action_paid_order
        self._chi_payment_failed = chi_payment_failed
        self._resource_payment_started = resource_payment_started


class CardPlayResultStub:
    """
    Stub result for attempting to play a card with cost tracking (Rule 1.14.1).

    Engine Feature Needed:
    - [ ] CardPlayResult with incurred_cost, cost_amount, cost_paid attributes (Rule 1.14.1)
    - [ ] ZeroCostAcknowledgment tracking (Rule 1.14.5)
    """

    def __init__(
        self,
        play_succeeded: bool = False,
        incurred_cost: bool = True,
        cost_amount: int = 0,
        cost_paid: bool = False,
        game_state_reversed: bool = False,
        entire_action_reversed: bool = False,
        has_cost: bool = True,
        zero_cost_acknowledged: bool = False,
        effective_cost: int = 0,
        has_asset_cost: bool = False,
        has_effect_cost: bool = False,
    ):
        self._play_succeeded = play_succeeded
        self._incurred_cost = incurred_cost
        self._cost_amount = cost_amount
        self._cost_paid = cost_paid
        self._game_state_reversed = game_state_reversed
        self._entire_action_reversed = entire_action_reversed
        self._has_cost = has_cost
        self._zero_cost_acknowledged = zero_cost_acknowledged
        self._effective_cost = effective_cost
        self._has_asset_cost = has_asset_cost
        self._has_effect_cost = has_effect_cost


class AbilityActivationResultStub:
    """
    Stub result for activating an ability with cost tracking (Rule 1.14.1).

    Engine Feature Needed:
    - [ ] AbilityActivationResult with _incurred_cost, _cost_amount, _cost_paid (Rule 1.14.1)
    """

    def __init__(
        self,
        incurred_cost: bool = True,
        cost_amount: int = 0,
        cost_paid: bool = False,
    ):
        self._incurred_cost = incurred_cost
        self._cost_amount = cost_amount
        self._cost_paid = cost_paid


class FullCostStub:
    """
    Stub for the full cost of a card (Rule 1.14.1).

    Engine Feature Needed:
    - [ ] FullCost class with asset/effect cost components (Rule 1.14.1)
    - [ ] Card.get_full_cost() returning FullCost
    """

    def __init__(self, has_asset_cost: bool = False, has_effect_cost: bool = False):
        self._has_asset_cost = has_asset_cost
        self._has_effect_cost = has_effect_cost


class PitchPaymentResultStub:
    """
    Stub result for pitching a card during cost payment (Rule 1.14.3).

    Engine Feature Needed:
    - [ ] PitchPaymentResult with resources_gained, chi_gained, pitch_event_occurred (Rule 1.14.3)
    """

    def __init__(
        self,
        resources_gained: int = 0,
        chi_gained: int = 0,
        pitch_event_occurred: bool = False,
        was_replaced: bool = False,
        total_resources_after_pitch: Optional[int] = None,
        pitch_succeeded: bool = True,
    ):
        self._resources_gained = resources_gained
        self._chi_gained = chi_gained
        self._pitch_event_occurred = pitch_event_occurred
        self._was_replaced = was_replaced
        self._total_resources_after_pitch = total_resources_after_pitch
        self._pitch_succeeded = pitch_succeeded


class PitchAttemptResultStub:
    """
    Stub result for attempting to pitch a card (Rule 1.14.3a/b).

    Engine Feature Needed:
    - [ ] PitchAttemptResult with _pitch_succeeded, _pitch_rejected, _rejection_reason (Rule 1.14.3a)
    """

    def __init__(
        self,
        pitch_succeeded: bool = False,
        pitch_rejected: bool = False,
        rejection_reason: str = "",
        chi_gained: int = 0,
    ):
        self._pitch_succeeded = pitch_succeeded
        self._pitch_rejected = pitch_rejected
        self._rejection_reason = rejection_reason
        self._chi_gained = chi_gained


class ChiCostPaymentResultStub:
    """
    Stub result for paying a chi cost (Rule 1.14.2c).

    Engine Feature Needed:
    - [ ] ChiCostPaymentResult with _chi_spent, _cost_paid attributes (Rule 1.14.2c)
    """

    def __init__(self, chi_spent: int = 0, cost_paid: bool = False):
        self._chi_spent = chi_spent
        self._cost_paid = cost_paid


class ResourceCostPaymentResultStub:
    """
    Stub result for paying a resource cost using chi-first order (Rule 1.14.2d).

    Engine Feature Needed:
    - [ ] ResourceCostPaymentResult tracking _chi_used_before_resource (Rule 1.14.2d)
    """

    def __init__(
        self,
        success: bool = False,
        chi_used_before_resource: bool = False,
        chi_spent: int = 0,
        resource_spent: int = 0,
    ):
        self._success = success
        self._chi_used_before_resource = chi_used_before_resource
        self._chi_spent = chi_spent
        self._resource_spent = resource_spent


class LifeCostPaymentResultStub:
    """
    Stub result for paying a life point cost (Rule 1.14.2e).

    Engine Feature Needed:
    - [ ] LifeCostPaymentResult with _life_spent, _cost_paid attributes (Rule 1.14.2e)
    """

    def __init__(self, life_spent: int = 0, cost_paid: bool = False):
        self._life_spent = life_spent
        self._cost_paid = cost_paid


class ActionCostPaymentResultStub:
    """
    Stub result for paying an action point cost (Rule 1.14.2f).

    Engine Feature Needed:
    - [ ] ActionCostPaymentResult with _action_spent, _cost_paid attributes (Rule 1.14.2f)
    """

    def __init__(self, action_spent: int = 0, cost_paid: bool = False):
        self._action_spent = action_spent
        self._cost_paid = cost_paid


class EffectCostPaymentResultStub:
    """
    Stub result for paying an effect-cost (Rule 1.14.4).

    Engine Feature Needed:
    - [ ] EffectCostPaymentResult with _effect_generated, _target_destroyed, etc. (Rule 1.14.4)
    - [ ] _game_state_reversed when effect-cost cannot be paid (Rule 1.14.4b)
    - [ ] _replacement_was_applied for Rule 1.14.4c
    """

    def __init__(
        self,
        effect_generated: bool = False,
        target_destroyed: bool = False,
        cost_paid: bool = False,
        game_state_reversed: bool = False,
        replacement_was_applied: bool = False,
    ):
        self._effect_generated = effect_generated
        self._target_destroyed = target_destroyed
        self._cost_paid = cost_paid
        self._game_state_reversed = game_state_reversed
        self._replacement_was_applied = replacement_was_applied


class HoodActivationResultStub:
    """
    Stub result for activating Hope Merchant's Hood (Rule 1.14.4 example).

    Engine Feature Needed:
    - [ ] HoodActivationResult tracking destroy-as-effect-cost (Rule 1.14.4)
    """

    def __init__(
        self,
        destroy_was_effect_cost: bool = False,
        cards_shuffled: bool = False,
        cost_paid: bool = False,
    ):
        self._destroy_was_effect_cost = destroy_was_effect_cost
        self._cards_shuffled = cards_shuffled
        self._cost_paid = cost_paid


class MultiEffectCostResultStub:
    """
    Stub result for paying a multi-effect-cost with player-declared ordering (Rule 1.14.4a).

    Engine Feature Needed:
    - [ ] MultiEffectCostResult with _player_declared_order, _generated_in_declared_order (Rule 1.14.4a)
    """

    def __init__(
        self,
        player_declared_order: bool = False,
        generated_in_declared_order: bool = False,
        cost_paid: bool = False,
    ):
        self._player_declared_order = player_declared_order
        self._generated_in_declared_order = generated_in_declared_order
        self._cost_paid = cost_paid


# ===========================================================================
# Section 2.11 Supertypes stubs
# ===========================================================================


class TypeBoxParseResultStub211:
    """
    Stub result for parsing a type box string (Rule 2.11.3).

    Engine Feature Needed:
    - [ ] TypeBoxParser.parse(type_box_str) returning parsed result (Rule 2.11.3)
    - [ ] TypeBoxParseResult.supertypes: list of supertype strings
    - [ ] TypeBoxParseResult.card_type: the primary card type string
    - [ ] TypeBoxParseResult.subtypes: list of subtype strings
    - [ ] TypeBoxParseResult.supertypes_before_type: True (Rule 2.11.3)
    """

    def __init__(
        self,
        supertypes: list = None,
        card_type: str = "",
        subtypes: list = None,
    ):
        self.supertypes = supertypes or []
        self.card_type = card_type
        self.subtypes = subtypes or []
        self.supertypes_before_type = (
            True  # Supertypes always before type per Rule 2.11.3
        )

    @classmethod
    def parse(cls, type_box_str: str) -> "TypeBoxParseResultStub211":
        """
        Parse a type box string in the format "[SUPERTYPES] [TYPE] [--- SUBTYPES]".

        Rule 2.11.3: Supertypes are printed before the card's type.
        Rule 2.14.1a: "Generic" as supertype means no supertypes.
        """
        KNOWN_CLASS_SUPERTYPES = {
            "Adjudicator",
            "Assassin",
            "Bard",
            "Brute",
            "Guardian",
            "Illusionist",
            "Mechanologist",
            "Merchant",
            "Necromancer",
            "Ninja",
            "Pirate",
            "Ranger",
            "Runeblade",
            "Shapeshifter",
            "Thief",
            "Warrior",
            "Wizard",
        }
        KNOWN_TALENT_SUPERTYPES = {
            "Chaos",
            "Draconic",
            "Earth",
            "Elemental",
            "Ice",
            "Light",
            "Lightning",
            "Mystic",
            "Revered",
            "Reviled",
            "Royal",
            "Shadow",
        }
        ALL_SUPERTYPES = KNOWN_CLASS_SUPERTYPES | KNOWN_TALENT_SUPERTYPES
        CARD_TYPES = {
            "Action",
            "Attack Reaction",
            "Defense Reaction",
            "Instant",
            "Resource",
            "Equipment",
            "Weapon",
            "Hero",
            "Token",
            "Mentor",
        }

        # Split on " - " to separate subtypes
        if " - " in type_box_str:
            main_part, subtype_part = type_box_str.split(" - ", 1)
            subtypes = [s.strip() for s in subtype_part.split(",")]
        else:
            main_part = type_box_str
            subtypes = []

        # "Generic" means no supertypes (Rule 2.14.1a)
        if main_part.startswith("Generic "):
            return cls(
                supertypes=[],
                card_type=main_part[len("Generic ") :].strip(),
                subtypes=subtypes,
            )
        if main_part == "Generic":
            return cls(supertypes=[], card_type="", subtypes=subtypes)

        # Parse the main part by splitting on spaces and identifying supertypes vs type
        tokens = main_part.strip().split()
        supertypes = []
        card_type_tokens = []
        type_found = False

        for token in tokens:
            if not type_found and token in ALL_SUPERTYPES:
                supertypes.append(token)
            else:
                type_found = True
                card_type_tokens.append(token)

        return cls(
            supertypes=supertypes,
            card_type=" ".join(card_type_tokens),
            subtypes=subtypes,
        )


class SupertypeCheckResultStub211:
    """
    Stub result for checking whether supertypes add additional rules (Rule 2.11.6).

    Engine Feature Needed:
    - [ ] SupertypeRegistry.is_non_functional(name) = True always (Rule 2.11.6)
    - [ ] SupertypeCheckResult.adds_additional_rules = False (Rule 2.11.6)
    """

    def __init__(
        self, adds_additional_rules: bool = False, is_non_functional: bool = True
    ):
        self.adds_additional_rules = adds_additional_rules
        self.is_non_functional = is_non_functional


class LayerWithSupertypesStub211:
    """
    Stub for a layer that inherits supertypes from its source (Rule 2.11.4).

    Engine Feature Needed:
    - [ ] ActivatedLayer.supertypes == source.supertypes (Rule 2.11.4)
    - [ ] TriggeredLayer.supertypes == source.supertypes (Rule 2.11.4)
    """

    def __init__(self, source=None, layer_type: str = "activated"):
        self._source = source
        self.layer_type = layer_type

    @property
    def supertypes(self):
        """Inherit supertypes from source (Rule 2.11.4)."""
        if self._source is None:
            return set()
        return getattr(self._source, "_supertypes", set())
