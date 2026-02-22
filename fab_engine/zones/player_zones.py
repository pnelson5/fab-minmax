"""
Player zones container for FAB Engine.
"""

from typing import List, Optional
from fab_engine.zones.zone import Zone, ZoneType
from fab_engine.cards.model import CardInstance, Subtype


class PlayerZones:
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.hero = Zone(ZoneType.HERO, player_id, max_size=1)
        self.deck = Zone(ZoneType.DECK, player_id)
        self.hand = Zone(ZoneType.HAND, player_id)
        self.pitch = Zone(ZoneType.PITCH, player_id)
        self.graveyard = Zone(ZoneType.GRAVEYARD, player_id)
        self.arsenal = Zone(ZoneType.ARSENAL, player_id, max_size=1)
        self.banished = Zone(ZoneType.BANISHED, player_id)
        self.head = Zone(ZoneType.HEAD, player_id, max_size=1)
        self.chest = Zone(ZoneType.CHEST, player_id, max_size=1)
        self.arms = Zone(ZoneType.ARMS, player_id, max_size=1)
        self.legs = Zone(ZoneType.LEGS, player_id, max_size=1)
        self.weapon_1 = Zone(ZoneType.WEAPON_1, player_id, max_size=1)
        self.weapon_2 = Zone(ZoneType.WEAPON_2, player_id, max_size=1)

    @property
    def equipment_zones(self) -> List[Zone]:
        return [self.head, self.chest, self.arms, self.legs]

    @property
    def weapon_zones(self) -> List[Zone]:
        return [self.weapon_1, self.weapon_2]

    @property
    def all_equipment(self) -> List[CardInstance]:
        cards = []
        for zone in self.equipment_zones:
            cards.extend(zone.cards)
        return cards

    @property
    def all_weapons(self) -> List[CardInstance]:
        cards = []
        for zone in self.weapon_zones:
            cards.extend(zone.cards)
        return cards

    def get_equipment_zone_for_card(self, card: CardInstance) -> Optional[Zone]:
        subtypes = card.template.subtypes
        if Subtype.HEAD in subtypes:
            return self.head
        elif Subtype.CHEST in subtypes:
            return self.chest
        elif Subtype.ARMS in subtypes:
            return self.arms
        elif Subtype.LEGS in subtypes:
            return self.legs
        return None

    def get_weapon_zone_for_card(self, card: CardInstance) -> Optional[Zone]:
        if self.weapon_1.is_empty:
            return self.weapon_1
        if self.weapon_2.is_empty:
            return self.weapon_2
        return None

    def get_zone_by_type(self, zone_type: ZoneType) -> Optional[Zone]:
        zone_map = {
            ZoneType.HERO: self.hero,
            ZoneType.DECK: self.deck,
            ZoneType.HAND: self.hand,
            ZoneType.PITCH: self.pitch,
            ZoneType.GRAVEYARD: self.graveyard,
            ZoneType.ARSENAL: self.arsenal,
            ZoneType.BANISHED: self.banished,
            ZoneType.HEAD: self.head,
            ZoneType.CHEST: self.chest,
            ZoneType.ARMS: self.arms,
            ZoneType.LEGS: self.legs,
            ZoneType.WEAPON_1: self.weapon_1,
            ZoneType.WEAPON_2: self.weapon_2,
        }
        return zone_map.get(zone_type)
