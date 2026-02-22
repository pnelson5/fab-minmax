"""
Effect functions for FAB Engine.
"""

from fab_engine.cards.model import Keyword


def deal_arcane_damage(engine, source_player, target_player, amount: int, source_card):
    """Deal arcane damage to a hero.

    Arcane damage bypasses combat. It can be prevented by Arcane Barrier.
    """
    remaining = amount

    for card in target_player.zones.all_equipment:
        if remaining <= 0:
            break
        ab_value = card.get_keyword_param(Keyword.ARCANE_BARRIER)
        if ab_value > 0:
            can_prevent = min(ab_value, remaining, target_player.hero.resource_points)
            if can_prevent > 0:
                target_player.hero.resource_points -= can_prevent
                remaining -= can_prevent

    if remaining > 0:
        target_player.hero.life_total -= remaining
        source_player.damage_dealt_this_turn += remaining
        source_player.arcane_damage_dealt_this_turn += remaining
        engine._check_game_over()

    return remaining


def deal_generic_damage(engine, target_player, amount: int):
    """Deal generic (non-typed) damage to a hero."""
    if amount > 0:
        target_player.hero.life_total -= amount
        engine._check_game_over()
    return amount


def draw_cards(player, count: int) -> int:
    """Draw cards from deck to hand."""
    drawn = 0
    for _ in range(count):
        card = player.zones.deck.draw_top()
        if card is None:
            break
        player.zones.hand.add(card)
        drawn += 1
    return drawn


def gain_resources(player, amount: int):
    """Gain resource points."""
    player.hero.resource_points += amount


def gain_action_points(player, amount: int):
    """Gain action points."""
    player.hero.action_points += amount


def banish_card(player, card):
    """Banish a card."""
    player.zones.banished.add(card)
