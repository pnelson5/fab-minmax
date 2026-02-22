"""
Heuristic opponent agent for FAB Engine.
"""

from typing import Optional, List
from fab_engine.engine.game import GameEngine
from fab_engine.engine.actions import Action, ActionType


class HeuristicAgent:
    """Greedy heuristic opponent that makes simple decisions."""

    def __init__(self, player_id: int = 1):
        self.player_id = player_id

    def select_action(self, game: GameEngine) -> Optional[Action]:
        """Select an action for the opponent."""

        if game.state.game_over:
            return None

        if game.state.active_player_id != self.player_id:
            return None

        actions = game.get_legal_actions(self.player_id)

        if not actions:
            return None

        for action in actions:
            if action.action_type == ActionType.PLAY_CARD_FROM_HAND:
                card = game.state.players[self.player_id].zones.hand.get_by_id(
                    action.card_instance_id
                )
                if card and card.template.is_attack_action:
                    if game.state.combat_chain.is_open:
                        continue
                    return action

        for action in actions:
            if action.action_type == ActionType.PLAY_CARD_FROM_HAND:
                card = game.state.players[self.player_id].zones.hand.get_by_id(
                    action.card_instance_id
                )
                if card and card.template.is_attack_action:
                    return action

        for action in actions:
            if action.action_type == ActionType.PITCH_CARD:
                card = game.state.players[self.player_id].zones.hand.get_by_id(
                    action.card_instance_id
                )
                if card:
                    return action

        for action in actions:
            if action.action_type == ActionType.END_PHASE:
                return action

        return actions[0] if actions else None

    def execute_turn(self, game: GameEngine) -> bool:
        """Execute opponent's turn until they pass."""

        while (
            not game.state.game_over and game.state.active_player_id == self.player_id
        ):
            action = self.select_action(game)
            if action is None:
                break
            game.execute_action(action)

        return game.state.game_over
