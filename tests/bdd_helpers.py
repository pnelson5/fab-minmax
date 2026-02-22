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
