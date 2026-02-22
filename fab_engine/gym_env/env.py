"""
Gymnasium environment for Flesh and Blood.
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Optional, Tuple, Dict, Any, List

from fab_engine.cards.loader import CardLoader
from fab_engine.cards.model import CardInstance
from fab_engine.engine.game import GameEngine, GameState, GamePhase
from fab_engine.engine.actions import Action, ActionType


class FaBEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    MAX_HAND_SIZE = 11
    MAX_DECK_SIZE = 40
    MAX_PITCH_SIZE = 10
    NUM_FEATURES_PER_CARD = 8

    def __init__(
        self,
        card_db_path: Optional[str] = None,
        opponent_type: str = "heuristic",
    ):
        super().__init__()

        self.card_loader = CardLoader(card_db_path)
        self.opponent_type = opponent_type
        self.game_engine: Optional[GameEngine] = None

        self.observation_space = self._create_observation_space()
        self.action_space = spaces.Discrete(100)

    def _create_observation_space(self) -> spaces.Dict:
        return spaces.Dict(
            {
                "player_life": spaces.Box(0, 40, shape=(1,), dtype=np.float32),
                "player_resources": spaces.Box(0, 20, shape=(1,), dtype=np.float32),
                "player_action_points": spaces.Box(0, 3, shape=(1,), dtype=np.float32),
                "player_hand_size": spaces.Box(0, 20, shape=(1,), dtype=np.float32),
                "player_deck_size": spaces.Box(0, 60, shape=(1,), dtype=np.float32),
                "player_pitch_size": spaces.Box(0, 20, shape=(1,), dtype=np.float32),
                "opponent_life": spaces.Box(0, 40, shape=(1,), dtype=np.float32),
                "opponent_hand_size": spaces.Box(0, 20, shape=(1,), dtype=np.float32),
                "opponent_deck_size": spaces.Box(0, 60, shape=(1,), dtype=np.float32),
                "phase": spaces.Box(0, 5, shape=(1,), dtype=np.float32),
                "turn_number": spaces.Box(0, 50, shape=(1,), dtype=np.float32),
                "combat_open": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
                "hand_cards": spaces.Box(
                    0,
                    100,
                    shape=(self.MAX_HAND_SIZE, self.NUM_FEATURES_PER_CARD),
                    dtype=np.float32,
                ),
                "top_of_deck": spaces.Box(
                    0, 100, shape=(self.NUM_FEATURES_PER_CARD,), dtype=np.float32
                ),
            }
        )

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict] = None,
    ) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
        super().reset(seed=seed)

        kano_hero = self.card_loader.get_kano_young()
        if kano_hero is None:
            raise ValueError("Kano hero not found in card database")

        generic_hero = self.card_loader.get_generic_hero()
        if generic_hero is None:
            raise ValueError("Generic hero not found in card database")

        kano_cards = self._build_kano_deck()
        generic_cards = self._build_generic_deck()

        import random

        random.shuffle(kano_cards)
        random.shuffle(generic_cards)

        from fab_engine.engine.game import create_game

        self.game_engine = create_game(
            player_0_hero=kano_hero,
            player_0_deck=kano_cards,
            player_1_hero=generic_hero,
            player_1_deck=generic_cards,
        )

        self._opponent_step()

        observation = self._get_observation()
        info = {}

        return observation, info

    def _build_kano_deck(self) -> List[CardInstance]:
        cards = []

        attacks = [c for c in self.card_loader.kano_cards if c.is_attack_action]
        non_attacks = [c for c in self.card_loader.kano_cards if c.is_non_attack_action]
        instants = [c for c in self.card_loader.kano_cards if c.is_instant]

        for _ in range(30):
            if attacks:
                cards.append(CardInstance(template=attacks[len(cards) % len(attacks)]))

        remaining = 40 - len(cards)
        for i in range(remaining):
            source = non_attacks + instants
            if source:
                cards.append(CardInstance(template=source[i % len(source)]))

        return cards

    def _build_generic_deck(self) -> List[CardInstance]:
        cards = []

        attacks = [c for c in self.card_loader.generic_cards if c.is_attack_action]

        for _ in range(35):
            if attacks:
                cards.append(CardInstance(template=attacks[len(cards) % len(attacks)]))

        for _ in range(5):
            if self.card_loader.generic_cards:
                idx = len(cards) % len(self.card_loader.generic_cards)
                cards.append(CardInstance(template=self.card_loader.generic_cards[idx]))

        return cards

    def step(
        self,
        action: int,
    ) -> Tuple[Dict[str, np.ndarray], float, bool, bool, Dict[str, Any]]:
        if self.game_engine is None:
            raise RuntimeError("Environment not reset")

        if self.game_engine.state.game_over:
            observation = self._get_observation()
            return (
                observation,
                0.0,
                True,
                False,
                {"winner": self.game_engine.state.winner},
            )

        # Get actions for the active player
        active_player = self.game_engine.state.active_player_id
        player_actions = self.game_engine.get_legal_actions(active_player)

        action_obj = None
        if action < len(player_actions):
            action_obj = player_actions[action]

        if action_obj is None:
            observation = self._get_observation()
            return observation, -1.0, False, False, {"message": "Invalid action"}

        result = self.game_engine.execute_action(action_obj)

        reward = 0.0
        if result.success:
            reward = 0.1

        self._opponent_step()

        if self.game_engine.state.game_over:
            if self.game_engine.state.winner == 0:
                reward = 100.0
            else:
                reward = -100.0

        observation = self._get_observation()
        terminated = self.game_engine.state.game_over
        truncated = False
        info = {"winner": self.game_engine.state.winner}

        return observation, reward, terminated, truncated, info

    def _opponent_step(self):
        if self.game_engine is None:
            return

        state = self.game_engine.state

        # Don't run opponent turn logic during combat defend step
        # The defending player needs to declare defenders, not take their turn
        if state.combat_step.name == "DEFEND":
            return

        # Don't run during reaction step - need to wait for reactions
        if state.combat_step.name == "REACTION":
            return

        while not state.game_over and state.active_player_id == 1:
            self._execute_opponent_action()

    def _execute_opponent_action(self):
        opponent_actions = self.game_engine.get_legal_actions(1)

        if not opponent_actions:
            from fab_engine.engine.actions import Action

            self.game_engine.execute_action(
                Action(
                    action_type=ActionType.END_PHASE,
                    player_id=1,
                )
            )
            return

        for action in opponent_actions:
            if action.action_type == ActionType.PITCH_CARD:
                self.game_engine.execute_action(action)
                break
            elif action.action_type == ActionType.PLAY_CARD_FROM_HAND:
                self.game_engine.execute_action(action)
                break
            elif action.action_type == ActionType.END_PHASE:
                self.game_engine.execute_action(action)
                break
        else:
            from fab_engine.engine.actions import Action

            self.game_engine.execute_action(
                Action(
                    action_type=ActionType.END_PHASE,
                    player_id=1,
                )
            )

    def _get_observation(self) -> Dict[str, np.ndarray]:
        if self.game_engine is None:
            return self._empty_observation()

        state = self.game_engine.state
        player = state.turn_player
        opponent = state.non_turn_player

        obs = {
            "player_life": np.array([player.hero.life_total], dtype=np.float32),
            "player_resources": np.array(
                [player.hero.resource_points], dtype=np.float32
            ),
            "player_action_points": np.array(
                [player.hero.action_points], dtype=np.float32
            ),
            "player_hand_size": np.array([player.zones.hand.size], dtype=np.float32),
            "player_deck_size": np.array([player.zones.deck.size], dtype=np.float32),
            "player_pitch_size": np.array([player.zones.pitch.size], dtype=np.float32),
            "opponent_life": np.array([opponent.hero.life_total], dtype=np.float32),
            "opponent_hand_size": np.array(
                [opponent.zones.hand.size], dtype=np.float32
            ),
            "opponent_deck_size": np.array(
                [opponent.zones.deck.size], dtype=np.float32
            ),
            "phase": np.array([float(state.phase.value)], dtype=np.float32),
            "turn_number": np.array([state.turn_number], dtype=np.float32),
            "combat_open": np.array(
                [1.0 if state.combat_chain.is_open else 0.0], dtype=np.float32
            ),
            "hand_cards": self._encode_hand(player.zones.hand.cards),
            "top_of_deck": self._encode_card(player.zones.deck.peek_top()),
        }

        return obs

    def _encode_hand(self, cards: List[CardInstance]) -> np.ndarray:
        encoded = np.zeros(
            (self.MAX_HAND_SIZE, self.NUM_FEATURES_PER_CARD), dtype=np.float32
        )

        for i, card in enumerate(cards[: self.MAX_HAND_SIZE]):
            encoded[i] = self._encode_card(card)

        return encoded

    def _encode_card(self, card: Optional[CardInstance]) -> np.ndarray:
        if card is None:
            return np.zeros(self.NUM_FEATURES_PER_CARD, dtype=np.float32)

        template = card.template

        features = [
            template.cost if template.has_cost else 0,
            template.power if template.has_power else 0,
            template.defense if template.has_defense else 0,
            template.arcane if template.has_arcane else 0,
            template.pitch if template.has_pitch else 0,
            1.0 if template.is_attack_action else 0.0,
            1.0 if template.is_instant else 0.0,
            1.0 if template.has_keyword(2) else 0.0,  # GO_AGAIN
        ]

        return np.array(features, dtype=np.float32)

    def _empty_observation(self) -> Dict[str, np.ndarray]:
        return {
            "player_life": np.zeros(1, dtype=np.float32),
            "player_resources": np.zeros(1, dtype=np.float32),
            "player_action_points": np.zeros(1, dtype=np.float32),
            "player_hand_size": np.zeros(1, dtype=np.float32),
            "player_deck_size": np.zeros(1, dtype=np.float32),
            "player_pitch_size": np.zeros(1, dtype=np.float32),
            "opponent_life": np.zeros(1, dtype=np.float32),
            "opponent_hand_size": np.zeros(1, dtype=np.float32),
            "opponent_deck_size": np.zeros(1, dtype=np.float32),
            "phase": np.zeros(1, dtype=np.float32),
            "turn_number": np.zeros(1, dtype=np.float32),
            "combat_open": np.zeros(1, dtype=np.float32),
            "hand_cards": np.zeros(
                (self.MAX_HAND_SIZE, self.NUM_FEATURES_PER_CARD), dtype=np.float32
            ),
            "top_of_deck": np.zeros(self.NUM_FEATURES_PER_CARD, dtype=np.float32),
        }

    def render(self):
        if self.game_engine is None:
            print("No game in progress")
            return

        state = self.game_engine.state
        player = state.turn_player
        opponent = state.non_turn_player

        print(f"\n=== Turn {state.turn_number} | Phase: {state.phase.name} ===")
        print(
            f"Kano (Player 0): {player.hero.life_total} life, {player.hero.resource_points} resources, {player.hero.action_points} AP"
        )
        print(
            f"  Hand: {player.zones.hand.size} cards, Deck: {player.zones.deck.size}, Pitch: {player.zones.pitch.size}"
        )
        print(f"Opponent: {opponent.hero.life_total} life")
        print(
            f"  Hand: {opponent.zones.hand.size} cards, Deck: {opponent.zones.deck.size}"
        )
        print(f"Combat: {'Open' if state.combat_chain.is_open else 'Closed'}")
        print()

    def close(self):
        self.game_engine = None
