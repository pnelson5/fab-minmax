import pytest
from fab_engine.cards.model import (
    CardTemplate,
    CardInstance,
    CardType,
    Subtype,
    Supertype,
    Color,
    Keyword,
    HeroState,
)


class TestCardTemplate:
    def test_card_template_creation(self):
        """Test CardTemplate basic creation."""
        ct = CardTemplate(
            unique_id="test-1",
            name="Test Card",
            types=frozenset({CardType.ACTION}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.ATTACK}),
            color=Color.RED,
            pitch=2,
            has_pitch=True,
            cost=3,
            has_cost=True,
            power=5,
            has_power=True,
            defense=4,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset({Keyword.GO_AGAIN}),
            keyword_params=((Keyword.GO_AGAIN, 1),),
            functional_text="Test card",
        )
        assert ct.name == "Test Card"
        assert ct.pitch == 2
        assert ct.cost == 3

    def test_is_attack_action(self):
        """Test is_attack_action property."""
        ct = CardTemplate(
            unique_id="test-1",
            name="Attack Card",
            types=frozenset({CardType.ACTION}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.ATTACK}),
            color=Color.RED,
            pitch=2,
            has_pitch=True,
            cost=3,
            has_cost=True,
            power=5,
            has_power=True,
            defense=-1,
            has_defense=False,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="",
        )
        assert ct.is_attack_action is True
        assert ct.is_non_attack_action is False
        assert ct.is_equipment is False
        assert ct.is_weapon is False

    def test_is_non_attack_action(self):
        """Test non-attack action cards."""
        ct = CardTemplate(
            unique_id="test-2",
            name="Non-Attack Action",
            types=frozenset({CardType.ACTION}),
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.BLUE,
            pitch=3,
            has_pitch=True,
            cost=1,
            has_cost=True,
            power=-1,
            has_power=False,
            defense=-1,
            has_defense=False,
            arcane=2,
            has_arcane=True,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="Deal 2 arcane damage",
        )
        assert ct.is_attack_action is False
        assert ct.is_non_attack_action is True

    def test_keyword_checking(self):
        """Test keyword checking."""
        ct = CardTemplate(
            unique_id="test-3",
            name="Go Again Card",
            types=frozenset({CardType.ACTION}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.ATTACK}),
            color=Color.RED,
            pitch=1,
            has_pitch=True,
            cost=2,
            has_cost=True,
            power=4,
            has_power=True,
            defense=-1,
            has_defense=False,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset({Keyword.GO_AGAIN}),
            keyword_params=((Keyword.GO_AGAIN, 1),),
            functional_text="Attack with go again",
        )
        assert ct.has_keyword(Keyword.GO_AGAIN)
        assert ct.get_keyword_param(Keyword.GO_AGAIN) == 1
        assert ct.has_keyword(Keyword.DOMINATE) is False


class TestCardInstance:
    def test_card_instance_creation(self):
        """Test CardInstance basic creation."""
        ct = CardTemplate(
            unique_id="test-1",
            name="Test Card",
            types=frozenset({CardType.ACTION}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.ATTACK}),
            color=Color.RED,
            pitch=2,
            has_pitch=True,
            cost=3,
            has_cost=True,
            power=5,
            has_power=True,
            defense=4,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="",
        )
        ci = CardInstance(template=ct)
        assert ci.name == "Test Card"
        assert ci.instance_id > 0

    def test_effective_defense(self):
        """Test effective defense with counters."""
        ct = CardTemplate(
            unique_id="test-1",
            name="Defense Card",
            types=frozenset({CardType.EQUIPMENT}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.CHEST}),
            color=Color.COLORLESS,
            pitch=-1,
            has_pitch=False,
            cost=3,
            has_cost=True,
            power=-1,
            has_power=False,
            defense=4,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset({Keyword.BATTLEWORN}),
            keyword_params=((Keyword.BATTLEWORN, 1),),
            functional_text="Defense 4, Battleworn",
        )
        ci = CardInstance(template=ct)
        assert ci.effective_defense == 4

        ci.defense_counters = -1
        assert ci.effective_defense == 3

        ci.defense_counters = -5
        assert ci.effective_defense == 0

    def test_effective_power(self):
        """Test effective power with counters."""
        ct = CardTemplate(
            unique_id="test-1",
            name="Attack Card",
            types=frozenset({CardType.ACTION}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.ATTACK}),
            color=Color.RED,
            pitch=1,
            has_pitch=True,
            cost=2,
            has_cost=True,
            power=5,
            has_power=True,
            defense=-1,
            has_defense=False,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="",
        )
        ci = CardInstance(template=ct)
        assert ci.effective_power == 5

        ci.power_counters = 2
        assert ci.effective_power == 7

    def test_temp_keywords(self):
        """Test temporary keywords."""
        ct = CardTemplate(
            unique_id="test-1",
            name="Test Card",
            types=frozenset({CardType.ACTION}),
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.RED,
            pitch=1,
            has_pitch=True,
            cost=1,
            has_cost=True,
            power=-1,
            has_power=False,
            defense=-1,
            has_defense=False,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="",
        )
        ci = CardInstance(template=ct)
        assert ci.has_keyword(Keyword.GO_AGAIN) is False

        ci.temp_keywords[Keyword.GO_AGAIN] = 1
        assert ci.has_keyword(Keyword.GO_AGAIN) is True


class TestHeroState:
    def test_hero_creation(self):
        """Test HeroState creation."""
        ct = CardTemplate(
            unique_id="kano-young",
            name="Kano",
            types=frozenset({CardType.HERO}),
            supertypes=frozenset({Supertype.WIZARD}),
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
            life=15,
            intellect=4,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="Kano hero card",
        )
        hero = HeroState(template=ct, life_total=ct.life)
        assert hero.life_total == 15
        assert hero.intellect == 4
        assert hero.is_alive is True
        assert hero.action_points == 0
        assert hero.resource_points == 0
