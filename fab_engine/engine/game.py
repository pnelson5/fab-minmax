"""
Game engine implementation for FAB Engine.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from fab_engine.zones.player_zones import PlayerZones
from fab_engine.cards.model import (
    CardTemplate,
    CardInstance,
    HeroState,
    Subtype,
    CardType,
)
from fab_engine.engine.combat import CombatChain, CombatStep, CombatEngine
from fab_engine.engine.actions import Action, ActionType, ActionResult


class GamePhase(Enum):
    NOT_STARTED = auto()
    START_OF_GAME = auto()
    START_PHASE = auto()
    ACTION_PHASE = auto()
    END_PHASE = auto()
    GAME_OVER = auto()


@dataclass
class PlayerState:
    player_id: int
    hero: HeroState
    zones: PlayerZones
    cards_played_this_turn: List[CardInstance] = field(default_factory=list)
    attacks_this_turn: int = 0
    has_defended_with_hand_card: bool = False
    damage_dealt_this_turn: int = 0
    arcane_damage_dealt_this_turn: int = 0


@dataclass
class GameState:
    players: List[PlayerState]
    turn_player_id: int = 0
    active_player_id: int = 0
    phase: GamePhase = GamePhase.NOT_STARTED
    combat_step: CombatStep = CombatStep.NONE
    combat_chain: CombatChain = field(default_factory=CombatChain)
    turn_number: int = 0
    winner: Optional[int] = None
    game_over: bool = False

    @property
    def turn_player(self) -> PlayerState:
        return self.players[self.turn_player_id]

    @property
    def non_turn_player(self) -> PlayerState:
        return self.players[1 - self.turn_player_id]

    @property
    def active_player(self) -> PlayerState:
        return self.players[self.active_player_id]


class GameEngine:
    def __init__(self, state: GameState):
        self.state = state
        self.event_log: List[dict] = []
        self.combat_engine = CombatEngine(state, self)

    def setup_game(self, first_turn_player: int = 0):
        """Execute start-of-game procedure."""
        self.state.phase = GamePhase.START_OF_GAME
        self.state.turn_player_id = first_turn_player

        for player in self.state.players:
            player.zones.deck.shuffle()

        for player in self.state.players:
            self._draw_up_to_intellect(player)

        self.state.turn_number = 1
        self._start_phase()

    def _start_phase(self):
        """Start phase - no priority, triggers resolve."""
        self.state.phase = GamePhase.START_PHASE
        self._handle_start_of_turn_effects()
        self._begin_action_phase()

    def _handle_start_of_turn_effects(self):
        """Handle start of turn effects."""
        pass

    def _begin_action_phase(self):
        """Action phase begins."""
        self.state.phase = GamePhase.ACTION_PHASE
        self.state.combat_step = CombatStep.NONE

        self.state.turn_player.hero.action_points = 1
        self.state.active_player_id = self.state.turn_player_id

    def get_legal_actions(self, player_id: int) -> List[Action]:
        """Get all legal actions for the active player."""
        actions = []
        player = self.state.players[player_id]

        if self.state.active_player_id != player_id:
            return actions

        if (
            self.state.phase == GamePhase.ACTION_PHASE
            and self.state.combat_step == CombatStep.NONE
        ):
            for card in player.zones.hand.cards:
                if card.template.is_attack_action and player.hero.action_points >= 1:
                    if (
                        card.template.has_cost
                        and player.hero.resource_points
                        + self._calculate_pitch_value(player)
                        >= card.template.cost
                    ) or not card.template.has_cost:
                        actions.append(
                            Action(
                                action_type=ActionType.PLAY_CARD_FROM_HAND,
                                player_id=player_id,
                                card_instance_id=card.instance_id,
                            )
                        )
                elif (
                    card.template.is_non_attack_action
                    and player.hero.action_points >= 1
                ):
                    if (
                        card.template.has_cost
                        and player.hero.resource_points
                        + self._calculate_pitch_value(player)
                        >= card.template.cost
                    ) or not card.template.has_cost:
                        actions.append(
                            Action(
                                action_type=ActionType.PLAY_CARD_FROM_HAND,
                                player_id=player_id,
                                card_instance_id=card.instance_id,
                            )
                        )
                elif card.template.is_instant:
                    if (
                        card.template.has_cost
                        and player.hero.resource_points
                        + self._calculate_pitch_value(player)
                        >= card.template.cost
                    ) or not card.template.has_cost:
                        actions.append(
                            Action(
                                action_type=ActionType.PLAY_CARD_FROM_HAND,
                                player_id=player_id,
                                card_instance_id=card.instance_id,
                            )
                        )

            actions.append(
                Action(
                    action_type=ActionType.END_PHASE,
                    player_id=player_id,
                )
            )

            if player.hero.action_points > 0 and not player.hero.has_used_hero_ability:
                hero_name = player.hero.template.name
                if "Kano" in hero_name and player.hero.resource_points >= 3:
                    actions.append(
                        Action(
                            action_type=ActionType.ACTIVATE_HERO_ABILITY,
                            player_id=player_id,
                        )
                    )

        elif (
            self.state.phase == GamePhase.ACTION_PHASE
            and self.state.combat_step == CombatStep.DEFEND
        ):
            defending_player = self.state.non_turn_player

            hand_defense_ids = [
                c.instance_id
                for c in defending_player.zones.hand.cards
                if c.template.has_defense
            ]
            equip_defense_ids = [
                c.instance_id
                for c in defending_player.zones.all_equipment
                if c.template.has_defense and c.effective_defense > 0
            ]

            for hid in hand_defense_ids:
                actions.append(
                    Action(
                        action_type=ActionType.DECLARE_DEFENDERS,
                        player_id=defending_player.player_id,
                        defender_ids=[hid],
                    )
                )

            if not hand_defense_ids and not equip_defense_ids:
                actions.append(
                    Action(
                        action_type=ActionType.DECLARE_DEFENDERS,
                        player_id=defending_player.player_id,
                        defender_ids=[],
                    )
                )

        return actions

    def execute_action(self, action: Action) -> ActionResult:
        """Execute a player action and advance game state."""
        if action.player_id != self.state.active_player_id:
            return ActionResult(success=False, message="Not active player")

        if self.state.game_over:
            return ActionResult(success=False, message="Game over")

        if action.action_type == ActionType.PITCH_CARD:
            return self._execute_pitch_card(action)
        elif action.action_type == ActionType.PLAY_CARD_FROM_HAND:
            return self._execute_play_card_from_hand(action)
        elif action.action_type == ActionType.DECLARE_DEFENDERS:
            return self._execute_declare_defenders(action)
        elif action.action_type == ActionType.END_PHASE:
            return self._execute_end_phase(action)
        elif action.action_type == ActionType.ACTIVATE_HERO_ABILITY:
            return self._execute_activate_hero_ability(action)

        return ActionResult(success=False, message="Unknown action type")

    def _calculate_pitch_value(self, player: PlayerState) -> int:
        """Calculate total pitch value of pitchable cards in hand."""
        total = 0
        for card in player.zones.hand.cards:
            if card.template.has_pitch:
                total += card.template.pitch
        return total

    def _auto_pitch_for_cost(self, player: PlayerState, cost: int) -> bool:
        """Automatically pitch cards from hand to cover the cost.

        Per rule 1.14.3b, a player may only pitch a card to gain resources to pay a cost.
        This method pitches cards until the player can afford the cost or runs out of pitchable cards.

        Returns True if sufficient resources were generated, False otherwise.
        """
        while player.hero.resource_points < cost:
            pitchable = [c for c in player.zones.hand.cards if c.template.has_pitch]
            if not pitchable:
                return False

            card = pitchable[0]
            player.zones.hand.remove(card)
            player.zones.pitch.add(card)
            player.hero.resource_points += card.template.pitch

        return True

    def _execute_pitch_card(self, action: Action) -> ActionResult:
        player = self.state.players[action.player_id]
        card = player.zones.hand.get_by_id(action.card_instance_id)

        if card is None:
            return ActionResult(success=False, message="Card not in hand")
        if not card.template.has_pitch:
            return ActionResult(success=False, message="Card cannot be pitched")

        player.zones.hand.remove(card)
        player.zones.pitch.add(card)
        player.hero.resource_points += card.template.pitch

        return ActionResult(success=True, message=f"Pitched {card.name}")

    def _execute_activate_hero_ability(self, action: Action) -> ActionResult:
        """Execute a hero ability activation."""
        player = self.state.players[action.player_id]
        hero_name = player.hero.template.name

        if player.hero.has_used_hero_ability:
            return ActionResult(
                success=False, message="Hero ability already used this turn"
            )

        if "Kano" in hero_name:
            return self._execute_kano_ability(player)

        return ActionResult(success=False, message=f"Unknown hero: {hero_name}")

    def _execute_kano_ability(self, player: PlayerState) -> ActionResult:
        """Kano's hero ability: Instant - {r}{r}{r}: Look at top card, if non-attack action, may banish and play as instant."""
        cost = 3

        if player.hero.resource_points < cost:
            return ActionResult(success=False, message="Not enough resources")

        player.hero.resource_points -= cost
        player.hero.has_used_hero_ability = True

        top_card = player.zones.deck.peek_top()
        if top_card is None:
            return ActionResult(success=True, message="Kano ability - deck empty")

        is_action = CardType.ACTION in top_card.template.types
        is_attack = Subtype.ATTACK in top_card.template.subtypes

        if is_action and not is_attack:
            card = player.zones.deck.draw_top()
            if card is not None:
                card.is_face_up = True
                player.zones.banished.add(card)
                card.temp_keywords["playable_from_banished"] = 1

        return ActionResult(success=True, message="Kano ability activated")

    def _execute_play_card_from_hand(self, action: Action) -> ActionResult:
        player = self.state.players[action.player_id]
        card = player.zones.hand.get_by_id(action.card_instance_id)

        if card is None:
            return ActionResult(success=False, message="Card not in hand")

        if Subtype.ATTACK in card.template.subtypes:
            if player.hero.action_points < 1:
                return ActionResult(success=False, message="Not enough action points")
            player.hero.action_points -= 1

            if card.template.has_cost:
                if not self._auto_pitch_for_cost(player, card.template.cost):
                    player.hero.action_points += 1
                    return ActionResult(
                        success=False, message="Not enough resources after pitching"
                    )
                player.hero.resource_points -= card.template.cost

            player.zones.hand.remove(card)
            self._open_combat_with_attack(player, card)
            player.cards_played_this_turn.append(card)

            return ActionResult(success=True, message=f"Played {card.name}")
        else:
            if CardType.ACTION in card.template.types:
                if player.hero.action_points < 1:
                    return ActionResult(
                        success=False, message="Not enough action points"
                    )
                player.hero.action_points -= 1

            if card.template.has_cost:
                if not self._auto_pitch_for_cost(player, card.template.cost):
                    if CardType.ACTION in card.template.types:
                        player.hero.action_points += 1
                    return ActionResult(
                        success=False, message="Not enough resources after pitching"
                    )
                player.hero.resource_points -= card.template.cost

            player.zones.hand.remove(card)
            self._resolve_non_attack_card(player, card)
            player.cards_played_this_turn.append(card)

            return ActionResult(success=True, message=f"Played {card.name}")

    def _open_combat_with_attack(self, player: PlayerState, card: CardInstance):
        target_player_id = 1 - player.player_id
        self.state.combat_chain.open_chain(card, target_player_id)
        self.combat_engine.begin_layer_step()
        self.combat_engine.resolve_layer_step()
        self.combat_engine.begin_attack_step()
        self.combat_engine.begin_defend_step()

    def _resolve_non_attack_card(self, player: PlayerState, card: CardInstance):
        if card.template.has_arcane and card.template.arcane > 0:
            target = self.state.non_turn_player
            from fab_engine.engine.effects import deal_arcane_damage

            deal_arcane_damage(self, player, target, card.template.arcane, card)

        player.zones.graveyard.add(card)

        from fab_engine.cards.model import Keyword

        if card.has_keyword(Keyword.GO_AGAIN):
            player.hero.action_points += 1

    def _execute_declare_defenders(self, action: Action) -> ActionResult:
        player = self.state.players[action.player_id]

        hand_defenders = [
            cid for cid in action.defender_ids if player.zones.hand.get_by_id(cid)
        ]
        equip_defenders = [
            cid
            for cid in action.defender_ids
            if any(zone.get_by_id(cid) for zone in player.zones.equipment_zones)
        ]

        self.combat_engine.declare_defenders(player, hand_defenders, equip_defenders)
        self.combat_engine.resolve_damage_step()
        self.combat_engine.begin_resolution_step()

        self._check_and_continue_combat()

        return ActionResult(success=True, message="Defenders declared")

    def _check_and_continue_combat(self):
        """Check if turn player can continue playing attacks during Resolution Step."""
        turn_player = self.state.turn_player

        can_play_attack = False
        for card in turn_player.zones.hand.cards:
            if card.template.is_attack_action and card.template.has_cost:
                if (
                    turn_player.hero.action_points >= 1
                    and turn_player.hero.resource_points >= card.template.cost
                ):
                    can_play_attack = True
                    break
            elif card.template.is_attack_action and not card.template.has_cost:
                if turn_player.hero.action_points >= 1:
                    can_play_attack = True
                    break

        if not can_play_attack:
            self.combat_engine.begin_close_step()

    def _execute_end_phase(self, action: Action) -> ActionResult:
        self._end_phase()
        return ActionResult(success=True, message="Ended phase")

    def _end_phase(self):
        """End phase."""
        self.state.phase = GamePhase.END_PHASE

        self._offer_arsenal(self.state.turn_player)

        self._return_pitch_to_deck(self.state.players[0])
        self._return_pitch_to_deck(self.state.players[1])

        self._untap_all(self.state.turn_player)

        for player in self.state.players:
            player.hero.action_points = 0
            player.hero.resource_points = 0

        self._draw_up_to_intellect(self.state.turn_player)
        if self.state.turn_number == 1:
            self._draw_up_to_intellect(self.state.non_turn_player)

        self._clear_turn_effects()

        self.state.turn_player_id = 1 - self.state.turn_player_id
        self.state.turn_number += 1

        for player in self.state.players:
            player.cards_played_this_turn.clear()
            player.attacks_this_turn = 0
            player.has_defended_with_hand_card = False
            player.damage_dealt_this_turn = 0
            player.arcane_damage_dealt_this_turn = 0
            player.hero.has_used_hero_ability = False

        self._start_phase()

    def _draw_up_to_intellect(self, player: PlayerState):
        while player.zones.hand.size < player.hero.intellect:
            card = player.zones.deck.draw_top()
            if card is None:
                break
            player.zones.hand.add(card)

    def _return_pitch_to_deck(self, player: PlayerState):
        while not player.zones.pitch.is_empty:
            card = player.zones.pitch.draw_top()
            player.zones.deck.add(card, position="bottom")

    def _untap_all(self, player: PlayerState):
        for card in player.zones.all_equipment + player.zones.all_weapons:
            card.is_tapped = False

    def _offer_arsenal(self, player: PlayerState):
        pass

    def _clear_turn_effects(self):
        for player in self.state.players:
            for card in player.zones.hand.cards:
                card.reset_temp_mods()
            for card in player.zones.arsenal.cards:
                card.reset_temp_mods()

    def _check_game_over(self):
        """Check if any player has lost."""
        for player in self.state.players:
            if not player.hero.is_alive:
                self.state.game_over = True
                self.state.winner = 1 - player.player_id
                self.state.phase = GamePhase.GAME_OVER
                return True
        return False


def create_game(
    player_0_hero: CardTemplate,
    player_0_deck: List[CardInstance],
    player_1_hero: CardTemplate,
    player_1_deck: List[CardInstance],
) -> GameEngine:
    """Create a new game with two players."""

    player_0_zones = PlayerZones(0)
    player_0_hero_state = HeroState(
        template=player_0_hero,
        life_total=player_0_hero.life,
    )
    for card in player_0_deck:
        player_0_zones.deck.add(card)
    player_0_zones.hero.add(CardInstance(template=player_0_hero))

    player_1_zones = PlayerZones(1)
    player_1_hero_state = HeroState(
        template=player_1_hero,
        life_total=player_1_hero.life,
    )
    for card in player_1_deck:
        player_1_zones.deck.add(card)
    player_1_zones.hero.add(CardInstance(template=player_1_hero))

    player_0 = PlayerState(
        player_id=0,
        hero=player_0_hero_state,
        zones=player_0_zones,
    )

    player_1 = PlayerState(
        player_id=1,
        hero=player_1_hero_state,
        zones=player_1_zones,
    )

    game_state = GameState(
        players=[player_0, player_1],
    )

    engine = GameEngine(game_state)
    engine.setup_game(first_turn_player=0)

    return engine
