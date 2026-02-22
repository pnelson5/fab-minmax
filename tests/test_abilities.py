"""
Tests for ability system and effects.
"""

import pytest
from fab_engine.cards.abilities import AbilityRegistry, ABILITY_REGISTRY
from fab_engine.engine.effects import (
    deal_arcane_damage,
    deal_generic_damage,
    draw_cards,
    gain_resources,
)
from fab_engine.engine.game import create_game
from fab_engine.cards.loader import CardLoader
from fab_engine.cards.model import CardInstance, Keyword
from fab_engine.engine.actions import ActionType


class TestAbilityRegistry:
    def test_ability_registry_creation(self):
        """AbilityRegistry can be created."""
        registry = AbilityRegistry()
        assert registry is not None

    def test_register_play_effect(self):
        """Can register a play effect."""

        def dummy_effect(engine, player, card):
            pass

        registry = AbilityRegistry()
        registry.register_play_effect("Test Card", dummy_effect)

        effect = registry.get_play_effect("Test Card")
        assert effect is not None

    def test_register_on_hit(self):
        """Can register an on-hit effect."""

        def dummy_effect(engine, player, card):
            pass

        registry = AbilityRegistry()
        registry.register_on_hit("Test Card", dummy_effect)

        effect = registry.get_on_hit_effect("Test Card")
        assert effect is not None

    def test_register_hero_ability(self):
        """Can register a hero ability."""

        def dummy_ability(engine, player, hero):
            pass

        registry = AbilityRegistry()
        registry.register_hero_ability("Test Hero", dummy_ability)

        ability = registry.get_hero_ability("Test Hero")
        assert ability is not None

    def test_get_nonexistent_effect(self):
        """Getting nonexistent effect returns None."""
        registry = AbilityRegistry()

        effect = registry.get_play_effect("Nonexistent Card")
        assert effect is None

        on_hit = registry.get_on_hit_effect("Nonexistent Card")
        assert on_hit is None

        hero = registry.get_hero_ability("Nonexistent Hero")
        assert hero is None


class TestEffects:
    def test_deal_arcane_damage(self):
        """deal_arcane_damage reduces hero life."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        opponent = game.state.players[1]

        initial_life = opponent.hero.life_total

        card = CardInstance(template=attacks[0])
        deal_arcane_damage(game, player, opponent, 3, card)

        assert opponent.hero.life_total == initial_life - 3

    def test_deal_generic_damage(self):
        """deal_generic_damage reduces hero life."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        opponent = game.state.players[1]

        initial_life = opponent.hero.life_total

        deal_generic_damage(game, opponent, 5)

        assert opponent.hero.life_total == initial_life - 5

    def test_arcane_damage_checks_game_over(self):
        """deal_arcane_damage checks for game over."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        opponent = game.state.players[1]

        opponent.hero.life_total = 3
        card = CardInstance(template=attacks[0])

        deal_arcane_damage(game, player, opponent, 10, card)

        assert game.state.game_over

    def test_draw_cards(self):
        """draw_cards draws from deck to hand."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        initial_hand = player.zones.hand.size

        drawn = draw_cards(player, 3)

        assert drawn == 3
        assert player.zones.hand.size == initial_hand + 3

    def test_gain_resources(self):
        """gain_resources adds resource points."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        player.hero.resource_points = 0

        gain_resources(player, 5)

        assert player.hero.resource_points == 5


class TestKanoHeroAbility:
    def test_kano_ability_costs_3_resources(self):
        """Kano hero ability costs 3 resources."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        player.hero.resource_points = 3

        actions = game.get_legal_actions(0)

        ability_actions = [
            a for a in actions if a.action_type == ActionType.ACTIVATE_HERO_ABILITY
        ]

        assert len(ability_actions) == 1

        result = game.execute_action(ability_actions[0])

        assert result.success
        assert player.hero.resource_points == 0
        assert player.hero.has_used_hero_ability

    def test_kano_ability_not_enough_resources(self):
        """Kano hero ability fails without enough resources."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        player.hero.resource_points = 2

        actions = game.get_legal_actions(0)

        ability_actions = [
            a for a in actions if a.action_type == ActionType.ACTIVATE_HERO_ABILITY
        ]

        assert len(ability_actions) == 0

    def test_kano_ability_already_used(self):
        """Kano hero ability cannot be used twice per turn."""
        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        player.hero.resource_points = 10
        player.hero.has_used_hero_ability = True

        actions = game.get_legal_actions(0)

        ability_actions = [
            a for a in actions if a.action_type == ActionType.ACTIVATE_HERO_ABILITY
        ]

        assert len(ability_actions) == 0


class TestArcaneBarrier:
    def test_arcane_damage_reduces_life(self):
        """Arcane damage reduces hero life when no arcane barrier."""
        from fab_engine.cards.model import CardInstance

        loader = CardLoader()
        kano_hero = loader.get_kano_young()
        generic_hero = loader.get_generic_hero()

        attacks = [c for c in loader.kano_cards if c.is_attack_action][:10]
        kano_deck = [CardInstance(template=c) for c in attacks * 4]

        generic_attacks = [c for c in loader.generic_cards if c.is_attack_action][:10]
        generic_deck = [CardInstance(template=c) for c in generic_attacks * 4]

        game = create_game(kano_hero, kano_deck, generic_hero, generic_deck)

        player = game.state.players[0]
        opponent = game.state.players[1]

        initial_life = opponent.hero.life_total

        card = CardInstance(template=attacks[0])
        deal_arcane_damage(game, player, opponent, 3, card)

        assert opponent.hero.life_total == initial_life - 3
