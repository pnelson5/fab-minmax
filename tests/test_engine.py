import pytest
from fab_engine.cards.model import (
    CardTemplate,
    CardInstance,
    CardType,
    Subtype,
    Supertype,
    Color,
    Keyword,
)
from fab_engine.zones.player_zones import PlayerZones
from fab_engine.engine.game import GameEngine, GameState, PlayerState, GamePhase
from fab_engine.engine.combat import CombatStep
from fab_engine.engine.actions import Action, ActionType


def make_attack_card(
    name: str = "Attack",
    power: int = 5,
    cost: int = 1,
    pitch: int = 1,
    keywords=frozenset(),
) -> CardInstance:
    """Create an attack action card."""
    ct = CardTemplate(
        unique_id=f"attack-{name}",
        name=name,
        types=frozenset({CardType.ACTION}),
        supertypes=frozenset(),
        subtypes=frozenset({Subtype.ATTACK}),
        color=Color.RED,
        pitch=pitch,
        has_pitch=True,
        cost=cost,
        has_cost=True,
        power=power,
        has_power=True,
        defense=-1,
        has_defense=False,
        arcane=0,
        has_arcane=False,
        life=0,
        intellect=0,
        keywords=keywords,
        keyword_params=tuple(keywords),
        functional_text="",
    )
    return CardInstance(template=ct)


def make_defense_card(name: str = "Defense", defense: int = 3) -> CardInstance:
    """Create a defense card."""
    ct = CardTemplate(
        unique_id=f"def-{name}",
        name=name,
        types=frozenset({CardType.ACTION}),
        supertypes=frozenset(),
        subtypes=frozenset(),
        color=Color.BLUE,
        pitch=3,
        has_pitch=True,
        cost=0,
        has_cost=False,
        power=-1,
        has_power=False,
        defense=defense,
        has_defense=True,
        arcane=0,
        has_arcane=False,
        life=0,
        intellect=0,
        keywords=frozenset(),
        keyword_params=(),
        functional_text="",
    )
    return CardInstance(template=ct)


def make_non_attack_action(
    name: str = "Spell", cost: int = 1, arcane: int = 0, pitch: int = 1
) -> CardInstance:
    """Create a non-attack action card."""
    ct = CardTemplate(
        unique_id=f"spell-{name}",
        name=name,
        types=frozenset({CardType.ACTION}),
        supertypes=frozenset(),
        subtypes=frozenset(),
        color=Color.BLUE,
        pitch=pitch,
        has_pitch=True,
        cost=cost,
        has_cost=True,
        power=-1,
        has_power=False,
        defense=-1,
        has_defense=False,
        arcane=arcane,
        has_arcane=arcane > 0,
        life=0,
        intellect=0,
        keywords=frozenset(),
        keyword_params=(),
        functional_text="",
    )
    return CardInstance(template=ct)


def make_hero(
    name: str = "Hero",
    life: int = 20,
    intellect: int = 4,
    supertype: Supertype = Supertype.GENERIC,
) -> CardTemplate:
    """Create a hero card."""
    return CardTemplate(
        unique_id=f"hero-{name}",
        name=name,
        types=frozenset({CardType.HERO}),
        supertypes=frozenset({supertype}),
        subtypes=frozenset(),
        color=Color.COLORLESS,
        pitch=-1,
        has_pitch=False,
        cost=-1,
        has_cost=False,
        power=-1,
        has_power=False,
        defense=-1,
        has_defense=False,
        arcane=0,
        has_arcane=False,
        life=life,
        intellect=intellect,
        keywords=frozenset(),
        keyword_params=(),
        functional_text="",
    )


class TestGameSetup:
    def test_create_game(self):
        """Test basic game creation."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        deck0 = [make_attack_card(f"Att{i}", power=4) for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}", power=3) for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1)

        assert engine.state.turn_number == 1
        assert engine.state.phase == GamePhase.ACTION_PHASE

    def test_starting_hand(self):
        """Test that players draw up to intellect."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1)

        assert engine.state.players[0].zones.hand.size == 4
        assert engine.state.players[1].zones.hand.size == 4


class TestPitching:
    def test_pitch_card(self):
        """Test pitching a card for resources."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        attack_card = make_attack_card("Att", pitch=2)
        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1, seed=42)
        add_to_hand(engine, 0, attack_card)

        player = engine.state.players[0]
        assert player.hero.resource_points == 0

        action = Action(
            ActionType.PITCH_CARD, player_id=0, card_instance_id=attack_card.instance_id
        )
        result = engine.execute_action(action)

        assert result.success is True
        assert player.hero.resource_points == 2
        assert player.zones.pitch.size == 1


class TestPlayingCards:
    def test_play_attack_opens_combat(self):
        """Test playing an attack card opens combat chain."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        attack_card = make_attack_card("Att", power=6, cost=1)
        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1, seed=42)
        add_to_hand(engine, 0, attack_card)

        engine.state.players[0].hero.resource_points = 1

        action = Action(
            ActionType.PLAY_CARD_FROM_HAND,
            player_id=0,
            card_instance_id=attack_card.instance_id,
        )
        result = engine.execute_action(action)

        assert result.success is True
        assert engine.state.combat_chain.is_open is True

    def test_play_non_attack_action(self):
        """Test playing a non-attack action card."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        spell_card = make_non_attack_action("Arcane Bolt", cost=1, arcane=2)
        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1, seed=42)
        add_to_hand(engine, 0, spell_card)

        engine.state.players[0].hero.resource_points = 1

        action = Action(
            ActionType.PLAY_CARD_FROM_HAND,
            player_id=0,
            card_instance_id=spell_card.instance_id,
        )
        result = engine.execute_action(action)

        assert result.success is True
        assert engine.state.players[1].hero.life_total == 18


class TestCombatChain:
    def test_combat_damage(self):
        """Test combat damage calculation."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        attack_card = make_attack_card("Att", power=5, cost=1)
        defense_card = make_defense_card("Def", defense=2)
        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1, seed=42)
        add_to_hand(engine, 0, attack_card)
        add_to_hand(engine, 1, defense_card)

        engine.state.players[0].hero.resource_points = 1

        action = Action(
            ActionType.PLAY_CARD_FROM_HAND,
            player_id=0,
            card_instance_id=attack_card.instance_id,
        )
        engine.execute_action(action)

        action = Action(
            ActionType.DECLARE_DEFENDERS,
            player_id=1,
            defender_ids=[defense_card.instance_id],
        )
        result = engine.execute_action(action)

        assert result.success is True
        assert engine.state.players[1].hero.life_total == 17

    def test_go_again(self):
        """Test go again grants action point."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        attack_card = make_attack_card(
            "Att", power=3, cost=0, keywords=frozenset({Keyword.GO_AGAIN})
        )
        defense_card = make_defense_card("Def", defense=5)
        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1, seed=42)
        add_to_hand(engine, 0, attack_card)
        add_to_hand(engine, 1, defense_card)

        action = Action(
            ActionType.PLAY_CARD_FROM_HAND,
            player_id=0,
            card_instance_id=attack_card.instance_id,
        )
        engine.execute_action(action)

        action = Action(ActionType.DECLARE_DEFENDERS, player_id=1, defender_ids=[])
        engine.execute_action(action)

        assert engine.state.players[0].hero.action_points == 1


class TestTurnStructure:
    def test_end_phase_transitions(self):
        """Test that ending phase cycles to next player."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1)

        initial_turn = engine.state.turn_player_id

        action = Action(ActionType.END_PHASE, player_id=0)
        result = engine.execute_action(action)

        assert result.success is True
        assert engine.state.turn_player_id == 1 - initial_turn

    def test_pitch_zone_returns_to_deck(self):
        """Test pitch zone cards return to deck at end of turn."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 20, 4)

        attack_card = make_attack_card("Att", pitch=2)
        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1, seed=42)
        add_to_hand(engine, 0, attack_card)

        action = Action(
            ActionType.PITCH_CARD, player_id=0, card_instance_id=attack_card.instance_id
        )
        engine.execute_action(action)

        assert engine.state.players[0].zones.pitch.size == 1

        action = Action(ActionType.END_PHASE, player_id=0)
        engine.execute_action(action)

        assert engine.state.players[0].zones.pitch.is_empty


class TestGameOver:
    def test_game_ends_when_hero_dies(self):
        """Test game ends when hero reaches 0 life."""
        hero = make_hero("Kano", 15, 4, Supertype.WIZARD)
        opponent = make_hero("Generic", 5, 4)

        attack_card = make_attack_card("Att", power=10, cost=1)
        defense_card = make_defense_card("Def", defense=2)
        deck0 = [make_attack_card(f"Att{i}") for i in range(40)]
        deck1 = [make_attack_card(f"OppAtt{i}") for i in range(40)]

        engine = create_test_game(hero, deck0, opponent, deck1, seed=42)
        add_to_hand(engine, 0, attack_card)
        add_to_hand(engine, 1, defense_card)

        engine.state.players[0].hero.resource_points = 1

        action = Action(
            ActionType.PLAY_CARD_FROM_HAND,
            player_id=0,
            card_instance_id=attack_card.instance_id,
        )
        engine.execute_action(action)

        action = Action(ActionType.DECLARE_DEFENDERS, player_id=1, defender_ids=[])
        engine.execute_action(action)

        assert engine.state.game_over is True
        assert engine.state.winner == 0


def create_test_game(hero0, deck0, hero1, deck1, seed: int = None):
    """Helper to create a test game."""
    import random

    if seed is not None:
        random.seed(seed)

    from fab_engine.engine.game import create_game

    engine = create_game(hero0, deck0, hero1, deck1)
    return engine


def add_to_hand(engine, player_id, card):
    """Add a card directly to a player's hand."""
    engine.state.players[player_id].zones.hand.add(card)
    return card
