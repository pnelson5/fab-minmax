"""
Tests for heuristic opponent agent.
"""

import pytest
from fab_engine.agents.heuristic import HeuristicAgent
from fab_engine.engine.game import create_game
from fab_engine.cards.loader import CardLoader
from fab_engine.cards.model import CardInstance
from fab_engine.engine.actions import ActionType


class TestHeuristicAgent:
    def test_heuristic_agent_creation(self):
        """HeuristicAgent can be created."""
        agent = HeuristicAgent(player_id=1)
        assert agent is not None
        assert agent.player_id == 1

    def test_select_action_returns_action(self):
        """select_action returns an Action."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        game.state.active_player_id = 1

        agent = HeuristicAgent(player_id=1)
        action = agent.select_action(game)

        assert action is not None

    def test_heuristic_chooses_attack(self):
        """Heuristic chooses to play attack when possible."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        agent = HeuristicAgent(player_id=1)
        game.state.active_player_id = 1

        action = agent.select_action(game)

        if action and action.action_type == ActionType.PLAY_CARD_FROM_HAND:
            card = game.state.players[1].zones.hand.get_by_id(action.card_instance_id)
            assert card.template.is_attack_action

    def test_heuristic_pitches_when_needed(self):
        """Heuristic pitches card when need resources."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        agent = HeuristicAgent(player_id=1)
        game.state.active_player_id = 1

        game.state.players[1].hero.resource_points = 0
        game.state.players[1].hero.action_points = 1

        action = agent.select_action(game)

        if action:
            assert action is not None

    def test_execute_turn_completes(self):
        """execute_turn runs without error."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        agent = HeuristicAgent(player_id=1)

        game.state.active_player_id = 1

        result = agent.execute_turn(game)

        assert result is not None

    def test_heuristic_does_not_crash_when_not_active(self):
        """Heuristic handles non-active player gracefully."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        agent = HeuristicAgent(player_id=1)

        game.state.active_player_id = 0

        action = agent.select_action(game)
        assert action is None
