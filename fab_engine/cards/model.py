"""
Card model for Flesh and Blood.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Set, Dict
from enum import Enum, auto


class CardType(Enum):
    ACTION = auto()
    ATTACK_REACTION = auto()
    DEFENSE_REACTION = auto()
    INSTANT = auto()
    EQUIPMENT = auto()
    WEAPON = auto()
    HERO = auto()


class Supertype(Enum):
    WIZARD = auto()
    GENERIC = auto()
    GUARDIAN = auto()
    WARRIOR = auto()
    NINJA = auto()
    BRUTE = auto()
    RANGER = auto()
    RUNESMITH = auto()
    MECHANOLOGIST = auto()
    MERCINARY = auto()
    SHADOW = auto()
    ILLUSIONIST = auto()
    BARD = auto()
    DRUID = auto()
    SENTINEL = auto()
    ARCANIST = auto()
    PSYCHE = auto()
    FAE = auto()


class Subtype(Enum):
    ATTACK = auto()
    ARMS = auto()
    CHEST = auto()
    HEAD = auto()
    LEGS = auto()
    SWORD = auto()
    STAFF = auto()
    ORB = auto()
    ONE_HAND = auto()
    TWO_HAND = auto()
    OFF_HAND = auto()
    AURA = auto()
    ITEM = auto()
    DAGGER = auto()
    BOW = auto()
    IMPLEMENT = auto()


class Color(Enum):
    RED = auto()
    YELLOW = auto()
    BLUE = auto()
    COLORLESS = auto()


class Keyword(Enum):
    GO_AGAIN = auto()
    DOMINATE = auto()
    ARCANE_BARRIER = auto()
    BATTLEWORN = auto()
    BLADE_BREAK = auto()
    TEMPER = auto()
    PHANTASM = auto()
    OVERPOWER = auto()
    PIERCING = auto()
    SPELLVOID = auto()
    QUELL = auto()
    WARD = auto()
    GUARDWELL = auto()
    AZURE = auto()
    CRIMSON = auto()


def _parse_color(color_str: str) -> Color:
    if color_str is None:
        return Color.COLORLESS
    c = str(color_str).lower()
    if c == "red":
        return Color.RED
    elif c == "yellow":
        return Color.YELLOW
    elif c == "blue":
        return Color.BLUE
    return Color.COLORLESS


def _parse_card_types(types_list: List[str]) -> Set[CardType]:
    result = set()
    for t in types_list:
        t_lower = t.lower()
        if "action" in t_lower:
            result.add(CardType.ACTION)
        if "attack reaction" in t_lower:
            result.add(CardType.ATTACK_REACTION)
        if "defense reaction" in t_lower:
            result.add(CardType.DEFENSE_REACTION)
        if "instant" in t_lower:
            result.add(CardType.INSTANT)
        if "equipment" in t_lower:
            result.add(CardType.EQUIPMENT)
        if "weapon" in t_lower:
            result.add(CardType.WEAPON)
        if "hero" in t_lower:
            result.add(CardType.HERO)
    return result


def _parse_supertypes(types_list: List[str]) -> Set[Supertype]:
    result = set()
    for t in types_list:
        t_lower = t.lower()
        if "wizard" in t_lower:
            result.add(Supertype.WIZARD)
        elif "generic" in t_lower:
            result.add(Supertype.GENERIC)
        elif "guardian" in t_lower:
            result.add(Supertype.GUARDIAN)
        elif "warrior" in t_lower:
            result.add(Supertype.WARRIOR)
        elif "ninja" in t_lower:
            result.add(Supertype.NINJA)
        elif "brute" in t_lower:
            result.add(Supertype.BRUTE)
        elif "ranger" in t_lower:
            result.add(Supertype.RANGER)
        elif "runesmith" in t_lower:
            result.add(Supertype.RUNESMITH)
        elif "mechanologist" in t_lower:
            result.add(Supertype.MECHANOLOGIST)
        elif "mercenary" in t_lower:
            result.add(Supertype.MERCINARY)
        elif "shadow" in t_lower:
            result.add(Supertype.SHADOW)
        elif "illusionist" in t_lower:
            result.add(Supertype.ILLUSIONIST)
        elif "bard" in t_lower:
            result.add(Supertype.BARD)
        elif "druid" in t_lower:
            result.add(Supertype.DRUID)
        elif "sentinel" in t_lower:
            result.add(Supertype.SENTINEL)
        elif "arcane" in t_lower:
            result.add(Supertype.ARCANIST)
        elif "psyche" in t_lower:
            result.add(Supertype.PSYCHE)
        elif "fae" in t_lower:
            result.add(Supertype.FAE)
    return result


def _parse_subtypes(types_list: List[str]) -> Set[Subtype]:
    result = set()
    for t in types_list:
        t_lower = t.lower()
        if "attack" in t_lower:
            result.add(Subtype.ATTACK)
        if "arms" in t_lower:
            result.add(Subtype.ARMS)
        if "chest" in t_lower:
            result.add(Subtype.CHEST)
        if "head" in t_lower:
            result.add(Subtype.HEAD)
        if "legs" in t_lower:
            result.add(Subtype.LEGS)
        if "sword" in t_lower:
            result.add(Subtype.SWORD)
        if "staff" in t_lower:
            result.add(Subtype.STAFF)
        if "orb" in t_lower:
            result.add(Subtype.ORB)
        if "one-handed" in t_lower or "one hand" in t_lower:
            result.add(Subtype.ONE_HAND)
        if "two-handed" in t_lower or "two hand" in t_lower:
            result.add(Subtype.TWO_HAND)
        if "off-hand" in t_lower or "off hand" in t_lower:
            result.add(Subtype.OFF_HAND)
        if "aura" in t_lower:
            result.add(Subtype.AURA)
        if "item" in t_lower:
            result.add(Subtype.ITEM)
        if "dagger" in t_lower:
            result.add(Subtype.DAGGER)
        if "bow" in t_lower:
            result.add(Subtype.BOW)
        if "implement" in t_lower:
            result.add(Subtype.IMPLEMENT)
    return result


def _parse_keywords(
    keywords_list: List[str], abilities_list: List[str]
) -> Dict[Keyword, int]:
    result = {}

    all_text = " ".join(keywords_list + [str(a) for a in abilities_list]).lower()

    if "go again" in all_text or "go again" in str(keywords_list).lower():
        result[Keyword.GO_AGAIN] = 1

    if "dominate" in all_text:
        result[Keyword.DOMINATE] = 1

    if "arcane barrier" in all_text:
        import re

        match = re.search(r"arcane barrier (\d+)", all_text)
        if match:
            result[Keyword.ARCANE_BARRIER] = int(match.group(1))
        else:
            result[Keyword.ARCANE_BARRIER] = 1

    if "battleworn" in all_text:
        result[Keyword.BATTLEWORN] = 1

    if "blade break" in all_text:
        result[Keyword.BLADE_BREAK] = 1

    if "temper" in all_text:
        result[Keyword.TEMPER] = 1

    if "phantasm" in all_text:
        result[Keyword.PHANTASM] = 1

    if "overpower" in all_text:
        result[Keyword.OVERPOWER] = 1

    if "piercing" in all_text:
        import re

        match = re.search(r"piercing (\d+)", all_text)
        if match:
            result[Keyword.PIERCING] = int(match.group(1))
        else:
            result[Keyword.PIERCING] = 1

    if "spellvoid" in all_text:
        import re

        match = re.search(r"spellvoid (\d+)", all_text)
        if match:
            result[Keyword.SPELLVOID] = int(match.group(1))
        else:
            result[Keyword.SPELLVOID] = 1

    if "quell" in all_text:
        import re

        match = re.search(r"quell (\d+)", all_text)
        if match:
            result[Keyword.QUELL] = int(match.group(1))
        else:
            result[Keyword.QUELL] = 1

    if "ward" in all_text:
        import re

        match = re.search(r"ward (\d+)", all_text)
        if match:
            result[Keyword.WARD] = int(match.group(1))
        else:
            result[Keyword.WARD] = 1

    if "guardwell" in all_text:
        result[Keyword.GUARDWELL] = 1

    if "azure" in all_text:
        result[Keyword.AZURE] = 1

    if "crimson" in all_text:
        result[Keyword.CRIMSON] = 1

    return result


def _parse_numeric(value, default: int = -1) -> int:
    if value is None or value == "":
        return default
    try:
        return int(float(value))
    except:
        return default


@dataclass(frozen=True)
class CardTemplate:
    unique_id: str
    name: str
    types: frozenset
    supertypes: frozenset
    subtypes: frozenset
    color: Color
    pitch: int
    has_pitch: bool
    cost: int
    has_cost: bool
    power: int
    has_power: bool
    defense: int
    has_defense: bool
    arcane: int
    has_arcane: bool
    life: int
    intellect: int
    keywords: frozenset
    keyword_params: tuple
    functional_text: str

    @property
    def is_attack_action(self) -> bool:
        return CardType.ACTION in self.types and Subtype.ATTACK in self.subtypes

    @property
    def is_non_attack_action(self) -> bool:
        return CardType.ACTION in self.types and Subtype.ATTACK not in self.subtypes

    @property
    def is_instant(self) -> bool:
        return CardType.INSTANT in self.types

    @property
    def is_defense_reaction(self) -> bool:
        return CardType.DEFENSE_REACTION in self.types

    @property
    def is_attack_reaction(self) -> bool:
        return CardType.ATTACK_REACTION in self.types

    @property
    def is_equipment(self) -> bool:
        return CardType.EQUIPMENT in self.types

    @property
    def is_weapon(self) -> bool:
        return CardType.WEAPON in self.types

    @property
    def is_hero(self) -> bool:
        return CardType.HERO in self.types

    @classmethod
    def from_card_json(cls, card_json: dict) -> "CardTemplate":
        unique_id = card_json.get("id", "")
        name = card_json.get("name", "")

        types_list = card_json.get("types", [])
        card_types = _parse_card_types(types_list)
        supertypes = _parse_supertypes(types_list)
        subtypes = _parse_subtypes(types_list)

        color = _parse_color(card_json.get("color"))

        pitch_val = _parse_numeric(card_json.get("pitch"))
        has_pitch = pitch_val >= 0

        cost_val = _parse_numeric(card_json.get("cost"))
        has_cost = cost_val >= 0

        power_val = _parse_numeric(card_json.get("power"))
        has_power = power_val >= 0

        defense_val = _parse_numeric(card_json.get("defense"))
        has_defense = defense_val >= 0

        arcane_val = _parse_numeric(card_json.get("arcane"))
        has_arcane = arcane_val >= 0

        life_val = _parse_numeric(card_json.get("health"), default=0)
        if life_val == 0 and "Hero" in types_list:
            life_val = 20  # Default for heroes without explicit health
        intellect_val = _parse_numeric(card_json.get("intelligence"), default=0)
        if intellect_val == 0 and "Hero" in types_list:
            intellect_val = 4

        keywords_list = card_json.get("card_keywords", [])
        abilities_list = card_json.get("abilities_and_effects", [])
        keywords_dict = _parse_keywords(keywords_list, abilities_list)

        keyword_params = tuple(keywords_dict.items())

        func_text = card_json.get("functional_text_plain", "")

        return cls(
            unique_id=unique_id,
            name=name,
            types=frozenset(card_types),
            supertypes=frozenset(supertypes),
            subtypes=frozenset(subtypes),
            color=color,
            pitch=pitch_val,
            has_pitch=has_pitch,
            cost=cost_val,
            has_cost=has_cost,
            power=power_val,
            has_power=has_power,
            defense=defense_val,
            has_defense=has_defense,
            arcane=arcane_val,
            has_arcane=has_arcane,
            life=life_val,
            intellect=intellect_val,
            keywords=frozenset(keywords_dict.keys()),
            keyword_params=keyword_params,
            functional_text=func_text,
        )

    def get_keyword_param(self, kw: Keyword) -> int:
        for k, v in self.keyword_params:
            if k == kw:
                return v
        return 0

    def has_keyword(self, kw: Keyword) -> bool:
        return kw in self.keywords


_instance_id_counter = 0


def _get_next_instance_id() -> int:
    global _instance_id_counter
    _instance_id_counter += 1
    return _instance_id_counter


@dataclass
class CardInstance:
    template: CardTemplate
    instance_id: int = field(default_factory=_get_next_instance_id)
    owner_id: int = 0  # Rule 1.3.1a: The owner of a card
    controller_id: Optional[int] = None  # Rule 1.3.1b: Controller (when in arena/stack)

    defense_counters: int = 0
    power_counters: int = 0
    is_face_up: bool = True
    is_tapped: bool = False

    temp_power_mod: int = 0
    temp_defense_mod: int = 0
    temp_keywords: dict = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.template.name

    @property
    def effective_defense(self) -> int:
        base = self.template.defense
        if base < 0:
            return -1
        return max(0, base + self.defense_counters + self.temp_defense_mod)

    @property
    def effective_power(self) -> int:
        base = self.template.power
        if base < 0:
            return -1
        return max(0, base + self.power_counters + self.temp_power_mod)

    def has_keyword(self, kw: Keyword) -> bool:
        return kw in self.template.keywords or kw in self.temp_keywords

    def get_keyword_param(self, kw: Keyword) -> int:
        if kw in self.temp_keywords:
            return self.temp_keywords[kw]
        return self.template.get_keyword_param(kw)

    def reset_temp_mods(self):
        self.temp_power_mod = 0
        self.temp_defense_mod = 0
        self.temp_keywords.clear()


@dataclass
class HeroState:
    template: CardTemplate
    life_total: int
    action_points: int = 0
    resource_points: int = 0
    has_used_hero_ability: bool = False

    @property
    def intellect(self) -> int:
        return self.template.intellect

    @property
    def is_alive(self) -> bool:
        return self.life_total > 0
