"""
Card loading utilities for FAB Engine.
"""

import json
import os
from typing import List, Optional, Dict, Set
from fab_engine.cards.model import CardTemplate, CardInstance, HeroState, Supertype


TALENT_SUPERTYPES = {
    "Chaos",
    "Draconic",
    "Earth",
    "Elemental",
    "Ice",
    "Light",
    "Lightning",
    "Mystic",
    "Revered",
    "Reviled",
    "Royal",
    "Shadow",
}


def load_card_database(
    db_path: str = "~/repos/github/flesh-and-blood-cards/json/english/card.json",
) -> List[CardTemplate]:
    """Load cards from the FaB card database."""
    db_path = os.path.expanduser(db_path)
    with open(db_path, "r") as f:
        cards = json.load(f)

    templates = []
    for card_json in cards:
        try:
            template = CardTemplate.from_card_json(card_json)
            templates.append(template)
        except Exception as e:
            pass  # Skip invalid cards

    return templates


def is_kano_eligible(card: CardTemplate) -> bool:
    """Check if card is eligible for Kano's deck (Common/Rare only)."""
    is_wizard = Supertype.WIZARD in card.supertypes
    is_generic = Supertype.GENERIC in card.supertypes

    if not (is_wizard or is_generic):
        return False

    return True


def is_generic_eligible(card: CardTemplate) -> bool:
    """Check if card is eligible for Generic hero deck."""
    return Supertype.GENERIC in card.supertypes


class CardLoader:
    """Card loader with filtering and deck management."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            default_path = os.path.expanduser(
                "~/repos/github/flesh-and-blood-cards/json/english/card.json"
            )
            if os.path.exists(default_path):
                db_path = default_path
            else:
                db_path = "/Users/pxn/repos/github/flesh-and-blood-cards/json/english/card.json"

        self._all_cards: List[CardTemplate] = []
        self._kano_cards: List[CardTemplate] = []
        self._generic_cards: List[CardTemplate] = []
        self._heroes: Dict[str, CardTemplate] = {}
        self._weapons: Dict[str, CardTemplate] = {}
        self._equipment: Dict[str, CardTemplate] = {}

        self._load_cards(db_path)

    def _load_cards(self, db_path: str):
        """Load and categorize cards from database."""
        all_templates = load_card_database(db_path)

        for template in all_templates:
            self._all_cards.append(template)

            if is_kano_eligible(template):
                self._kano_cards.append(template)

            if is_generic_eligible(template):
                self._generic_cards.append(template)

            if template.is_hero:
                self._heroes[template.name] = template

            if template.is_weapon:
                self._weapons[template.name] = template

            if template.is_equipment:
                self._equipment[template.name] = template

    @property
    def all_cards(self) -> List[CardTemplate]:
        return self._all_cards

    @property
    def kano_cards(self) -> List[CardTemplate]:
        return self._kano_cards

    @property
    def generic_cards(self) -> List[CardTemplate]:
        return self._generic_cards

    @property
    def heroes(self) -> Dict[str, CardTemplate]:
        return self._heroes

    @property
    def weapons(self) -> Dict[str, CardTemplate]:
        return self._weapons

    @property
    def equipment(self) -> Dict[str, CardTemplate]:
        return self._equipment

    def get_kano_young(self) -> Optional[CardTemplate]:
        """Get Kano (Young) hero."""
        for name, hero in self._heroes.items():
            if name == "Kano":
                return hero
        return None

    def get_kano_adult(self) -> Optional[CardTemplate]:
        """Get Kano, Dracai of Aether (Adult) hero."""
        for name, hero in self._heroes.items():
            if name == "Kano, Dracai of Aether":
                return hero
        return None

    def get_generic_hero(self) -> Optional[CardTemplate]:
        """Get a generic hero for the opponent."""
        for name, hero in self._heroes.items():
            if "Generic" in name or "Generic Hero" in name:
                return hero
        for hero in self._heroes.values():
            if hero.life > 0 and hero.intellect > 0:
                return hero
        return None

    def get_arcane_weapons(self) -> List[CardTemplate]:
        """Get weapons that deal arcane damage (staves, orbs)."""
        return [w for w in self._weapons.values() if w.has_arcane]

    def get_arcane_barrier_equipment(self) -> List[CardTemplate]:
        """Get equipment with Arcane Barrier."""
        from fab_engine.cards.model import Keyword

        return [
            e for e in self._equipment.values() if e.has_keyword(Keyword.ARCANE_BARRIER)
        ]

    def create_deck(
        self, card_templates: List[CardTemplate], count: int = 40
    ) -> List[CardInstance]:
        """Create a deck of CardInstances from templates."""
        import random

        deck = []
        for template in card_templates:
            for _ in range(count):
                deck.append(CardInstance(template=template))
        random.shuffle(deck)
        return deck


def load_card_database(
    db_path: str = "~/repos/github/flesh-and-blood-cards/json/english/card.json",
) -> List[CardTemplate]:
    """Load cards from the FaB card database."""
    import json
    import os

    db_path = os.path.expanduser(db_path)
    with open(db_path, "r") as f:
        cards = json.load(f)

    templates = []
    for card_json in cards:
        try:
            template = CardTemplate.from_card_json(card_json)
            templates.append(template)
        except Exception:
            pass

    return templates
