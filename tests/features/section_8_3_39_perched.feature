# Feature file for Section 8.3.39: Perched (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.39
#
# 8.3.39 Perched
#   Perched is a static ability that means "This can be equipped in addition
#   to a 2H weapon. This can't be attacked while it's equipped."
#
# 8.3.39a A card with perched may be equipped to, and occupy, a weapon zone
#   that a two-hander weapon is already equipped to but does not occupy;
#   otherwise, a card with perched cannot be equipped if the player does not
#   have an empty zone to equip to.
#
# 8.3.39b A card with perched cannot be equipped unless it has a subtype that
#   allows it to be equipped to a specific zone.
#
# 8.3.39c An equipped card with perched cannot be the target of an attack,
#   but it may be the target of other non-attack effects.
#
# Key aspects:
# - Perched is a STATIC ability
# - Perched allows equipping alongside a 2H weapon (in the unused part of the weapon zone)
# - Perched card can only equip if: (a) 2H weapon zone has unoccupied space, OR (b) there is an empty zone
# - Perched card must still have a valid equip subtype (e.g., Off-Hand) to be equipped
# - While equipped, a perched card cannot be attacked
# - While equipped, a perched card CAN be targeted by non-attack effects

Feature: Section 8.3.39 - Perched Ability Keyword
    As a game engine
    I need to correctly implement the Perched ability keyword
    So that cards can be equipped alongside 2H weapons and are protected from attacks while equipped

    # ===== Rule 8.3.39: Perched is a static ability =====

    Scenario: Perched is a static ability
        Given a card has the "Perched" keyword
        When I inspect the Perched ability on the card
        Then the Perched ability is a static ability
        And the Perched ability is not a triggered ability
        And the Perched ability is not an activated ability

    # ===== Rule 8.3.39: Perched meaning is correct =====

    Scenario: Perched means this can be equipped alongside 2H weapon and cannot be attacked while equipped
        Given a card has the "Perched" keyword
        When I inspect the Perched ability on the card
        Then the Perched ability means "This can be equipped in addition to a 2H weapon. This can't be attacked while it's equipped."

    # ===== Rule 8.3.39a: Perched card equips to unoccupied part of 2H weapon zone =====

    Scenario: Perched card can be equipped when a 2H weapon occupies one weapon zone slot
        Given a player has a two-hander weapon equipped in the left weapon zone
        And the right weapon zone is unoccupied
        And the player has a card with "Perched" that has a valid equip subtype
        When the player equips the perched card
        Then the perched card is equipped successfully
        And the perched card occupies the unoccupied weapon zone

    # ===== Rule 8.3.39a: Perched card cannot equip without empty zone =====

    Scenario: Perched card cannot be equipped when all weapon zones are occupied
        Given a player has a two-hander weapon that occupies all weapon zone slots
        And the player has a card with "Perched" that has a valid equip subtype
        When the player attempts to equip the perched card
        Then the perched card cannot be equipped
        And the equip action is rejected

    # ===== Rule 8.3.39a: Perched card can equip to empty zone even without a 2H weapon =====

    Scenario: Perched card can be equipped to an empty weapon zone without a 2H weapon
        Given a player has no weapons equipped
        And the player has a card with "Perched" that has a valid equip subtype
        When the player equips the perched card
        Then the perched card is equipped successfully

    # ===== Rule 8.3.39b: Perched card requires a valid equip subtype =====

    Scenario: Perched card without a valid equip subtype cannot be equipped
        Given a player has an empty weapon zone
        And the player has a card with "Perched" but no valid equip subtype
        When the player attempts to equip the perched card
        Then the perched card cannot be equipped
        And the equip action is rejected due to missing equip subtype

    Scenario: Perched card with a valid equip subtype can be equipped
        Given a player has an empty weapon zone
        And the player has a card with "Perched" and a valid equip subtype for that zone
        When the player equips the perched card
        Then the perched card is equipped successfully

    # ===== Rule 8.3.39c: Equipped perched card cannot be attacked =====

    Scenario: Equipped perched card cannot be the target of an attack
        Given a player has a card with "Perched" that is equipped
        When an opponent attempts to attack the equipped perched card
        Then the attack targeting the perched card is not legal
        And the perched card cannot be attacked

    # ===== Rule 8.3.39c: Equipped perched card can be targeted by non-attack effects =====

    Scenario: Equipped perched card can be the target of non-attack effects
        Given a player has a card with "Perched" that is equipped
        When a non-attack effect targets the equipped perched card
        Then the non-attack effect can legally target the perched card
        And the perched card is a valid target for the non-attack effect

    # ===== Rule 8.3.39c: Protection only applies while equipped =====

    Scenario: Unequipped card with Perched keyword can be attacked normally
        Given a player has a card with "Perched" that is not equipped
        When an opponent attempts to attack the unequipped perched card
        Then the attack is legal
        And the unequipped perched card can be attacked
