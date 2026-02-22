import pytest
from fab_engine.zones.zone import Zone, ZoneType
from fab_engine.zones.player_zones import PlayerZones
from fab_engine.cards.model import (
    CardTemplate,
    CardInstance,
    CardType,
    Subtype,
    Color,
)


def make_test_card(name: str = "Test Card") -> CardInstance:
    """Create a test card instance."""
    ct = CardTemplate(
        unique_id=f"test-{name}",
        name=name,
        types=frozenset({CardType.ACTION}),
        supertypes=frozenset(),
        subtypes=frozenset(),
        color=Color.RED,
        pitch=1,
        has_pitch=True,
        cost=1,
        has_cost=True,
        power=3,
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
    return CardInstance(template=ct)


class TestZone:
    def test_zone_creation(self):
        """Test Zone creation."""
        zone = Zone(ZoneType.DECK, owner_id=0)
        assert zone.is_empty
        assert zone.size == 0

    def test_add_card(self):
        """Test adding cards to a zone."""
        zone = Zone(ZoneType.DECK, owner_id=0)
        card = make_test_card()
        zone.add(card)
        assert zone.size == 1
        assert not zone.is_empty

    def test_add_top_bottom(self):
        """Test adding cards to top/bottom."""
        zone = Zone(ZoneType.DECK, owner_id=0)
        card1 = make_test_card("Card 1")
        card2 = make_test_card("Card 2")
        card3 = make_test_card("Card 3")

        zone.add(card1, position="bottom")
        zone.add(card2, position="top")
        zone.add(card3, position="top")

        assert zone.peek_top() == card3
        assert zone.draw_top() == card3
        assert zone.peek_top() == card2

    def test_remove_card(self):
        """Test removing cards from a zone."""
        zone = Zone(ZoneType.DECK, owner_id=0)
        card = make_test_card()
        zone.add(card)

        assert zone.remove(card) is True
        assert zone.is_empty

        assert zone.remove(card) is False

    def test_draw_top(self):
        """Test drawing from top of zone."""
        zone = Zone(ZoneType.DECK, owner_id=0)
        card1 = make_test_card("Card 1")
        card2 = make_test_card("Card 2")
        zone.add(card1)
        zone.add(card2)

        drawn = zone.draw_top()
        assert drawn == card2
        assert zone.size == 1

    def test_max_size(self):
        """Test max size enforcement."""
        zone = Zone(ZoneType.ARSENAL, owner_id=0, max_size=1)
        card1 = make_test_card("Card 1")
        card2 = make_test_card("Card 2")

        assert zone.add(card1) is True
        assert zone.add(card2) is False
        assert zone.size == 1

    def test_contains(self):
        """Test contains check."""
        zone = Zone(ZoneType.DECK, owner_id=0)
        card = make_test_card()
        zone.add(card)

        assert zone.contains(card) is True


class TestPlayerZones:
    def test_player_zones_creation(self):
        """Test PlayerZones creation."""
        pz = PlayerZones(player_id=0)
        assert pz.player_id == 0

        assert pz.deck is not None
        assert pz.hand is not None
        assert pz.pitch is not None
        assert pz.graveyard is not None
        assert pz.arsenal is not None
        assert pz.banished is not None

    def test_equipment_zones(self):
        """Test equipment zones exist."""
        pz = PlayerZones(player_id=0)
        assert len(pz.equipment_zones) == 4

    def test_weapon_zones(self):
        """Test weapon zones exist."""
        pz = PlayerZones(player_id=0)
        assert len(pz.weapon_zones) == 2

    def test_get_equipment_zone_for_card(self):
        """Test routing equipment to correct zones."""
        pz = PlayerZones(player_id=0)

        head_ct = CardTemplate(
            unique_id="head",
            name="Head Test",
            types=frozenset({CardType.EQUIPMENT}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.HEAD}),
            color=Color.COLORLESS,
            pitch=-1,
            has_pitch=False,
            cost=1,
            has_cost=True,
            power=-1,
            has_power=False,
            defense=1,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="",
        )
        head_card = CardInstance(template=head_ct)
        zone = pz.get_equipment_zone_for_card(head_card)
        assert zone == pz.head

        chest_ct = CardTemplate(
            unique_id="chest",
            name="Chest Test",
            types=frozenset({CardType.EQUIPMENT}),
            supertypes=frozenset(),
            subtypes=frozenset({Subtype.CHEST}),
            color=Color.COLORLESS,
            pitch=-1,
            has_pitch=False,
            cost=2,
            has_cost=True,
            power=-1,
            has_power=False,
            defense=2,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=(),
            functional_text="",
        )
        chest_card = CardInstance(template=chest_ct)
        zone = pz.get_equipment_zone_for_card(chest_card)
        assert zone == pz.chest
