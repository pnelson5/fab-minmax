"""
Combat chain implementation for FAB Engine.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional


class CombatStep(Enum):
    NONE = auto()
    LAYER = auto()
    ATTACK = auto()
    DEFEND = auto()
    REACTION = auto()
    DAMAGE = auto()
    RESOLUTION = auto()
    CLOSE = auto()


@dataclass
class ChainLink:
    link_number: int
    attacking_card: object
    attack_target_player_id: int
    defending_cards: List = field(default_factory=list)
    physical_damage_dealt: int = 0
    did_hit: bool = False

    @property
    def total_defense(self) -> int:
        total = 0
        for c in self.defending_cards:
            if hasattr(c, "effective_defense"):
                defense = c.effective_defense
                if defense >= 0:
                    total += max(0, defense)
        return total


class CombatChain:
    def __init__(self):
        self.is_open: bool = False
        self.chain_links: List[ChainLink] = []
        self.current_step: CombatStep = CombatStep.NONE

    @property
    def active_chain_link(self) -> Optional[ChainLink]:
        return self.chain_links[-1] if self.chain_links else None

    def open_chain(self, attacking_card, target_player_id: int):
        self.is_open = True
        link = ChainLink(
            link_number=len(self.chain_links) + 1,
            attacking_card=attacking_card,
            attack_target_player_id=target_player_id,
        )
        self.chain_links.append(link)
        self.current_step = CombatStep.LAYER

    def add_chain_link(self, attacking_card, target_player_id: int):
        link = ChainLink(
            link_number=len(self.chain_links) + 1,
            attacking_card=attacking_card,
            attack_target_player_id=target_player_id,
        )
        self.chain_links.append(link)
        self.current_step = CombatStep.LAYER

    def close(self):
        self.is_open = False
        self.current_step = CombatStep.NONE
        self.chain_links.clear()


@dataclass
class CombatEngine:
    state: object
    engine: object

    def begin_layer_step(self):
        self.state.combat_step = CombatStep.LAYER
        self.state.active_player_id = self.state.turn_player_id

    def resolve_layer_step(self):
        self.begin_attack_step()

    def begin_attack_step(self):
        self.state.combat_step = CombatStep.ATTACK
        chain = self.state.combat_chain
        link = chain.active_chain_link

        target_player = self.state.players[link.attack_target_player_id]
        if not target_player.hero.is_alive:
            self.begin_close_step()
            return

        self.state.active_player_id = self.state.turn_player_id

    def begin_defend_step(self):
        self.state.combat_step = CombatStep.DEFEND
        chain = self.state.combat_chain
        link = chain.active_chain_link
        defending_player_id = link.attack_target_player_id
        self.state.active_player_id = defending_player_id

    def declare_defenders(
        self, player, hand_card_ids: List[int], equipment_ids: List[int]
    ):
        chain = self.state.combat_chain
        link = chain.active_chain_link
        attack = link.attacking_card

        from fab_engine.cards.model import Keyword, CardType

        for card_id in hand_card_ids:
            card = player.zones.hand.get_by_id(card_id)
            if card is None:
                continue
            if not card.template.has_defense:
                continue

            if attack.has_keyword(Keyword.DOMINATE):
                if player.has_defended_with_hand_card:
                    continue

            if attack.has_keyword(Keyword.OVERPOWER):
                action_defenders = [
                    c
                    for c in link.defending_cards
                    if CardType.ACTION in c.template.types
                ]
                if action_defenders:
                    if CardType.ACTION in card.template.types:
                        continue

            player.zones.hand.remove(card)
            link.defending_cards.append(card)
            player.has_defended_with_hand_card = True

        for card_id in equipment_ids:
            card = None
            for zone in player.zones.equipment_zones:
                card = zone.get_by_id(card_id)
                if card:
                    break
            if card is None:
                continue
            if not card.template.has_defense:
                continue
            if card.effective_defense <= 0:
                continue

            link.defending_cards.append(card)

        self.begin_reaction_step()

    def begin_reaction_step(self):
        self.state.combat_step = CombatStep.REACTION
        self.state.active_player_id = self.state.turn_player_id

    def resolve_damage_step(self):
        self.state.combat_step = CombatStep.DAMAGE
        chain = self.state.combat_chain
        link = chain.active_chain_link
        attack = link.attacking_card

        attack_power = attack.effective_power
        total_defense = link.total_defense

        if attack_power > total_defense:
            damage = attack_power - total_defense
            target = self.state.players[link.attack_target_player_id]
            target.hero.life_total -= damage
            link.physical_damage_dealt = damage
            link.did_hit = True

            attacker = self.state.turn_player
            attacker.damage_dealt_this_turn += damage

            self.engine._check_game_over()

        self.state.active_player_id = self.state.turn_player_id

    def begin_resolution_step(self):
        self.state.combat_step = CombatStep.RESOLUTION
        chain = self.state.combat_chain
        link = chain.active_chain_link

        attack = link.attacking_card
        from fab_engine.cards.model import Keyword

        if attack.has_keyword(Keyword.GO_AGAIN):
            self.state.turn_player.hero.action_points += 1

        if link.did_hit:
            self._process_on_hit_effects(link)

        self.state.active_player_id = self.state.turn_player_id

    def _process_on_hit_effects(self, link: ChainLink):
        attack = link.attacking_card

        if attack.template.has_arcane and attack.template.arcane > 0:
            target = self.state.players[link.attack_target_player_id]
            from fab_engine.engine.effects import deal_arcane_damage

            deal_arcane_damage(
                self.engine,
                self.state.turn_player,
                target,
                attack.template.arcane,
                attack,
            )

    def begin_close_step(self):
        self.state.combat_step = CombatStep.CLOSE
        chain = self.state.combat_chain

        for link in chain.chain_links:
            for card in link.defending_cards:
                self._process_post_defend_effects(card)

        for link in chain.chain_links:
            attack_card = link.attacking_card
            attacker = self.state.players[self.state.turn_player_id]
            attacker.zones.graveyard.add(attack_card)

            for card in link.defending_cards:
                if not card.template.is_equipment:
                    defender = self.state.players[link.attack_target_player_id]
                    defender.zones.graveyard.add(card)

        chain.close()

        self.state.phase = self.state.turn_player.hero.action_points > 0 and 1 or 2
        from fab_engine.engine.game import GamePhase

        self.state.phase = GamePhase.ACTION_PHASE
        self.state.combat_step = CombatStep.NONE
        self.state.active_player_id = self.state.turn_player_id

    def _process_post_defend_effects(self, card):
        from fab_engine.cards.model import Keyword

        if card.has_keyword(Keyword.BATTLEWORN):
            card.defense_counters -= 1

        if card.has_keyword(Keyword.BLADE_BREAK):
            self._destroy_equipment(card)

        if card.has_keyword(Keyword.TEMPER):
            card.defense_counters -= 1
            if card.effective_defense <= 0:
                self._destroy_equipment(card)

        if card.has_keyword(Keyword.GUARDWELL):
            card.defense_counters -= card.effective_defense

    def _destroy_equipment(self, card):
        player = self.state.players[0]
        for zone in player.zones.equipment_zones:
            if zone.contains(card):
                zone.remove(card)
                player.zones.graveyard.add(card)
                return

        player = self.state.players[1]
        for zone in player.zones.equipment_zones:
            if zone.contains(card):
                zone.remove(card)
                player.zones.graveyard.add(card)
                return
