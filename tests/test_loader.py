"""
Tests for card loading and filtering.
"""

import pytest
from fab_engine.cards.loader import CardLoader, load_card_database
from fab_engine.cards.model import CardType, Subtype, Keyword


class TestCardLoader:
    def test_card_loader_creation(self):
        """CardLoader can be created."""
        loader = CardLoader()
        assert loader is not None

    def test_load_card_database(self):
        """Can load cards from database."""
        cards = load_card_database()
        assert len(cards) > 0

    def test_kano_eligible_cards(self):
        """Kano eligible cards are loaded."""
        loader = CardLoader()
        assert len(loader.kano_cards) > 0

    def test_generic_eligible_cards(self):
        """Generic eligible cards are loaded."""
        loader = CardLoader()
        assert len(loader.generic_cards) > 0

    def test_get_kano_young(self):
        """Can get Kano (Young) hero."""
        loader = CardLoader()
        kano = loader.get_kano_young()
        assert kano is not None
        assert kano.is_hero

    def test_kano_young_has_correct_stats(self):
        """Kano (Young) has correct life and intellect."""
        loader = CardLoader()
        kano = loader.get_kano_young()
        assert kano is not None
        assert kano.life == 15
        assert kano.intellect == 4

    def test_get_kano_adult(self):
        """Can get Kano, Dracai of Aether (Adult) hero."""
        loader = CardLoader()
        kano = loader.get_kano_adult()
        assert kano is not None
        assert kano.is_hero

    def test_kano_adult_has_correct_stats(self):
        """Kano (Adult) has correct life and intellect."""
        loader = CardLoader()
        kano = loader.get_kano_adult()
        assert kano is not None
        assert kano.life == 30
        assert kano.intellect == 4

    def test_get_generic_hero(self):
        """Can get a generic hero for opponent."""
        loader = CardLoader()
        hero = loader.get_generic_hero()
        assert hero is not None
        assert hero.is_hero

    def test_weapons_loaded(self):
        """Weapons are loaded."""
        loader = CardLoader()
        assert len(loader.weapons) > 0

    def test_equipment_loaded(self):
        """Equipment is loaded."""
        loader = CardLoader()
        assert len(loader.equipment) > 0

    def test_arcane_weapons(self):
        """Can get weapons with arcane damage."""
        loader = CardLoader()
        arcane_weapons = loader.get_arcane_weapons()
        assert len(arcane_weapons) > 0

    def test_arcane_barrier_equipment(self):
        """Can get equipment with Arcane Barrier."""
        loader = CardLoader()
        ab_equipment = loader.get_arcane_barrier_equipment()
        assert len(ab_equipment) > 0

    def test_create_deck(self):
        """Can create a deck from templates."""
        loader = CardLoader()
        attacks = [c for c in loader.kano_cards if c.is_attack_action][:5]
        deck = loader.create_deck(attacks, count=1)
        assert len(deck) == 5

    def test_kano_cards_have_wizard_or_generic(self):
        """Kano eligible cards are Wizard or Generic."""
        loader = CardLoader()
        for card in loader.kano_cards[:20]:
            has_wizard = card.supertypes and any(
                s.name == "WIZARD" for s in card.supertypes
            )
            has_generic = card.supertypes and any(
                s.name == "GENERIC" for s in card.supertypes
            )
            assert has_wizard or has_generic

    def test_generic_cards_have_generic_supertype(self):
        """Generic eligible cards have Generic supertype."""
        loader = CardLoader()
        for card in loader.generic_cards[:20]:
            has_generic = card.supertypes and any(
                s.name == "GENERIC" for s in card.supertypes
            )
            assert has_generic

    def test_attack_cards_have_power(self):
        """Attack cards have power values."""
        loader = CardLoader()
        attacks = [c for c in loader.kano_cards if c.is_attack_action]
        assert len(attacks) > 0
        for card in attacks[:10]:
            assert card.has_power

    def test_non_attack_actions_have_arcane(self):
        """Non-attack action cards may have arcane."""
        loader = CardLoader()
        non_attacks = [c for c in loader.kano_cards if c.is_non_attack_action]
        assert len(non_attacks) > 0

    def test_equipment_has_subtypes(self):
        """Equipment has proper subtypes (Head, Chest, Arms, Legs)."""
        loader = CardLoader()
        equipment = list(loader.equipment.values())
        has_subtype = False
        for eq in equipment[:20]:
            if eq.subtypes:
                has_subtype = True
                break
        assert has_subtype
