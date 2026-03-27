# Feature file for Section 8.4: Label Keywords
# Reference: Flesh and Blood Comprehensive Rules Section 8.4
#
# 8.4 Label Keywords
#
# 8.4.1 Combo
#   Combo is a label for a static ability typically written as
#   "Combo - If [NAMES] was the last attack this combat chain, [EFFECTS]"
#
# 8.4.2 Crush
#   Crush is a label for a triggered-static ability typically written as
#   "Crush - When this deals 4 or more damage, [EFFECTS]."
#   8.4.2a The Crush ability is conditional on an event that deals damage,
#   not just a hit-event. (See rule 7.5.5)
#
# 8.4.3 Reprise
#   Reprise is a label for a resolution ability typically written as
#   "Reprise - If the defending hero has defended with a card from their hand
#   this chain link, [EFFECTS]."
#   8.4.3a The condition of a reprise ability effect is checked on resolution -
#   it does not retroactively generate effects if the condition is met after resolution.
#
# 8.4.4 Channel
#   Channel is a label for an ability typically written as
#   "Channel [SUPERTYPE] - At the beginning of your end phase, put a flow counter
#   on this then destroy it unless you put a [SUPERTYPE] card from your pitch zone
#   on the bottom of your deck for each flow counter on it."
#
# 8.4.5 Material
#   Material is a label for an ability typically written as
#   "Material - While this is under a permanent, [EFFECTS]."
#
# 8.4.6 Rupture
#   Rupture is a label for an ability typically written as
#   "Rupture - If this is played [as / at] chain link 4 or higher, [EFFECTS]."
#
# 8.4.7 Contract
#   Contract is a label for a static ability typically written as
#   "Contract - You are contracted to [CONDITION]. Whenever you complete this
#   contract, [EFFECT]"
#
# 8.4.8 Surge
#   Surge is a label for a resolution or static ability typically written as
#   "Surge - If this deals N damage, [EFFECTS]."
#
# 8.4.9 Solflare
#   Solflare is a label for an ability typically written as
#   "Solflare - When this is charged to your hero's soul, [EFFECTS]."
#
# 8.4.10 Unity
#   Unity is a label for an ability typically written as
#   "Unity - When this defends together with a card from hand, [EFFECTS]."
#
# 8.4.11 Evo Upgrade
#   Evo Upgrade is a label for an ability typically written as
#   "Evo Upgrade - [EFFECTS] for each evo you have equipped"
#
# 8.4.12 Galvanize
#   Galvanize is a label for an ability typically written as
#   "Galvanize - When this defends, you may destroy an item you control. If you do, [EFFECTS]"
#
# 8.4.13 Tower
#   Tower is a label for an ability typically written as
#   "Tower - If this has 13 or more {p}, [EFFECTS]"
#
# 8.4.14 Decompose
#   Decompose is a label for an ability typically written as
#   "Decompose - You may banish 2 Earth cards and an action card from your graveyard. If you do, [EFFECTS]."
#
# 8.4.15 Earth Bond
#   Earth Bond is a label for an ability typically written as
#   "Earth Bond - If an earth card was pitched to play this, [EFFECTS]."
#
# 8.4.16 Lightning Flow
#   Lightning Flow is a label for an ability typically written as
#   "Lightning Flow - If you've played a Lightning card this turn, [EFFECTS]."
#
# 8.4.17 Heavy
#   Heavy is a label for an ability typically written as
#   "Heavy - If this is the only card equipped to your weapon zones, [EFFECTS]."
#
# 8.4.18 High Tide
#   High Tide is a label for an ability typically written as
#   "High Tide - If there are 2 or more blue cards in your pitch zone, [EFFECTS]."
#
# 8.4.19 Go Fish
#   Go Fish is a label for an ability typically written as
#   "Go Fish - When this hits a hero, they choose and reveal a card from their hand.
#   If it's [ADJECTIVE] they discard it and you create a Gold token."

Feature: Section 8.4 - Label Keywords
    As a game engine
    I need to correctly implement label keywords
    So that ability effects are only triggered when their label conditions are met

    # ===== Rule 8.4.1: Combo — requires named card as last attack =====

    Scenario: Combo ability triggers when the named card was the last attack
        Given a card with "Combo" labeling that names "Scar for a Scar"
        And "Scar for a Scar" was the last attack this combat chain
        When I check the Combo condition
        Then the Combo condition is met

    Scenario: Combo ability does not trigger when the named card was not the last attack
        Given a card with "Combo" labeling that names "Scar for a Scar"
        And the last attack this combat chain was a different card
        When I check the Combo condition
        Then the Combo condition is not met

    Scenario: Combo ability does not trigger when no attack was made on this combat chain
        Given a card with "Combo" labeling that names "Scar for a Scar"
        And no attack has been made on the combat chain yet
        When I check the Combo condition
        Then the Combo condition is not met

    # ===== Rule 8.4.2: Crush — requires dealing 4 or more damage =====

    Scenario: Crush ability triggers when the card deals 4 or more damage
        Given a card with the "Crush" label keyword
        When the card deals 4 damage
        Then the Crush condition is met

    Scenario: Crush ability triggers when the card deals more than 4 damage
        Given a card with the "Crush" label keyword
        When the card deals 5 damage
        Then the Crush condition is met

    Scenario: Crush ability does not trigger when the card deals fewer than 4 damage
        Given a card with the "Crush" label keyword
        When the card deals 3 damage
        Then the Crush condition is not met

    Scenario: Crush ability does not trigger on zero damage
        Given a card with the "Crush" label keyword
        When the card deals 0 damage
        Then the Crush condition is not met

    # ===== Rule 8.4.2a: Crush — conditional on damage event, not just a hit =====

    Scenario: Crush is conditional on a damage event not merely a hit event
        Given a card with the "Crush" label keyword
        When the card hits but deals 0 damage
        Then the Crush condition is not met

    # ===== Rule 8.4.3: Reprise — requires defending from hand this chain link =====

    Scenario: Reprise ability triggers when the defender has defended with a card from hand
        Given a card with the "Reprise" label keyword
        And the defending hero has defended with a card from their hand this chain link
        When I check the Reprise condition
        Then the Reprise condition is met

    Scenario: Reprise ability does not trigger when the defender has not defended from hand
        Given a card with the "Reprise" label keyword
        And the defending hero has not defended with a card from their hand this chain link
        When I check the Reprise condition
        Then the Reprise condition is not met

    # ===== Rule 8.4.3a: Reprise — condition checked at resolution, not retroactively =====

    Scenario: Reprise condition is checked at resolution time
        Given a card with the "Reprise" label keyword
        And the defending hero has not yet defended from hand at the time of resolution
        When the Reprise ability resolves
        Then the Reprise condition is evaluated at resolution not retroactively

    # ===== Rule 8.4.4: Channel — places flow counter and destroys unless condition met =====

    Scenario: Channel ability puts a flow counter on the card at start of end phase
        Given a card with the "Channel" label keyword in the arena
        When the start of the end phase is processed
        Then the card has 1 flow counter

    Scenario: Channel ability destroys the card unless a supertype card is put from pitch to deck bottom
        Given a card with the "Channel" label keyword in the arena with 1 flow counter
        And the player does not put a matching supertype card from pitch to deck bottom
        When the end phase Channel check is processed
        Then the card is destroyed by Channel

    Scenario: Channel ability does not destroy the card when the player fulfills the Channel cost
        Given a card with the "Channel" label keyword in the arena with 1 flow counter
        And the player puts 1 matching supertype card from pitch zone to deck bottom
        When the end phase Channel check is processed
        Then the card is not destroyed by Channel

    # ===== Rule 8.4.5: Material — effects apply while card is under a permanent =====

    Scenario: Material ability effects are active while the card is under a permanent
        Given a card with the "Material" label keyword
        And the card is under a permanent
        When I check the Material condition
        Then the Material condition is met

    Scenario: Material ability effects are not active when the card is not under a permanent
        Given a card with the "Material" label keyword
        And the card is not under a permanent
        When I check the Material condition
        Then the Material condition is not met

    # ===== Rule 8.4.6: Rupture — effects if played at chain link 4 or higher =====

    Scenario: Rupture ability triggers when played at chain link 4
        Given a card with the "Rupture" label keyword
        When the card is played at chain link 4
        Then the Rupture condition is met

    Scenario: Rupture ability triggers when played at chain link 5 or higher
        Given a card with the "Rupture" label keyword
        When the card is played at chain link 5
        Then the Rupture condition is met

    Scenario: Rupture ability does not trigger when played at chain link 3
        Given a card with the "Rupture" label keyword
        When the card is played at chain link 3
        Then the Rupture condition is not met

    Scenario: Rupture ability does not trigger when played at chain link 1
        Given a card with the "Rupture" label keyword
        When the card is played at chain link 1
        Then the Rupture condition is not met

    # ===== Rule 8.4.7: Contract — tracks condition and rewards on completion =====

    Scenario: Contract ability recognizes when the contract condition is completed
        Given a card with the "Contract" label keyword
        And the contract condition has been fulfilled
        When I check the Contract completion status
        Then the contract is completed

    Scenario: Contract ability effect triggers when the contract is completed
        Given a card with the "Contract" label keyword
        And the contract condition has been fulfilled
        When I check the Contract completion status
        Then the Contract reward effect is triggered

    Scenario: Contract ability does not trigger when the contract condition is not fulfilled
        Given a card with the "Contract" label keyword
        And the contract condition has not been fulfilled
        When I check the Contract completion status
        Then the contract is not completed

    # ===== Rule 8.4.8: Surge — effects if the card deals N damage =====

    Scenario: Surge ability triggers when the card deals the required damage amount
        Given a card with the "Surge" label keyword requiring 3 damage
        When the card deals 3 damage
        Then the Surge condition is met

    Scenario: Surge ability does not trigger when the card deals less than required damage
        Given a card with the "Surge" label keyword requiring 3 damage
        When the card deals 2 damage
        Then the Surge condition is not met

    # ===== Rule 8.4.9: Solflare — effects when charged to hero's soul =====

    Scenario: Solflare ability triggers when the card is charged to the hero's soul
        Given a card with the "Solflare" label keyword
        When the card is charged to the hero's soul
        Then the Solflare condition is met

    Scenario: Solflare ability does not trigger when the card is not charged to the soul
        Given a card with the "Solflare" label keyword
        When the card enters the arena without being charged to soul
        Then the Solflare condition is not met

    # ===== Rule 8.4.10: Unity — effects when defending together with a card from hand =====

    Scenario: Unity ability triggers when the card defends together with a card from hand
        Given a card with the "Unity" label keyword
        When the card defends together with a card from hand
        Then the Unity condition is met

    Scenario: Unity ability does not trigger when the card defends alone
        Given a card with the "Unity" label keyword
        When the card defends without any card from hand
        Then the Unity condition is not met

    # ===== Rule 8.4.11: Evo Upgrade — scales with number of evos equipped =====

    Scenario: Evo Upgrade effect scales with 1 evo equipped
        Given a card with the "Evo Upgrade" label keyword
        And the player has 1 evo equipped
        When I check the Evo Upgrade effect
        Then the Evo Upgrade value is 1

    Scenario: Evo Upgrade effect scales with 3 evos equipped
        Given a card with the "Evo Upgrade" label keyword
        And the player has 3 evos equipped
        When I check the Evo Upgrade effect
        Then the Evo Upgrade value is 3

    Scenario: Evo Upgrade effect is 0 when no evos are equipped
        Given a card with the "Evo Upgrade" label keyword
        And the player has 0 evos equipped
        When I check the Evo Upgrade effect
        Then the Evo Upgrade value is 0

    # ===== Rule 8.4.12: Galvanize — when defending, may destroy an item =====

    Scenario: Galvanize ability triggers when the card defends
        Given a card with the "Galvanize" label keyword
        When the card defends
        Then the Galvanize option is available

    Scenario: Galvanize additional effects apply when player destroys an item while defending
        Given a card with the "Galvanize" label keyword
        And the player controls an item
        When the card defends and the player destroys the item
        Then the Galvanize condition is met

    Scenario: Galvanize additional effects do not apply when player does not destroy an item
        Given a card with the "Galvanize" label keyword
        When the card defends without destroying an item
        Then the Galvanize condition is not met

    # ===== Rule 8.4.13: Tower — effects when power is 13 or more =====

    Scenario: Tower ability triggers when the card has 13 or more power
        Given a card with the "Tower" label keyword with 13 power
        When I check the Tower condition
        Then the Tower condition is met

    Scenario: Tower ability triggers when the card has more than 13 power
        Given a card with the "Tower" label keyword with 15 power
        When I check the Tower condition
        Then the Tower condition is met

    Scenario: Tower ability does not trigger when the card has fewer than 13 power
        Given a card with the "Tower" label keyword with 12 power
        When I check the Tower condition
        Then the Tower condition is not met

    # ===== Rule 8.4.14: Decompose — banish 2 Earth + 1 action from graveyard =====

    Scenario: Decompose ability condition is met when 2 Earth cards and an action card are available in graveyard
        Given a card with the "Decompose" label keyword
        And the player has 2 Earth cards and an action card in their graveyard
        When I check the Decompose condition
        Then the Decompose condition is met

    Scenario: Decompose ability condition is not met when graveyard lacks required cards
        Given a card with the "Decompose" label keyword
        And the player has fewer than 2 Earth cards in their graveyard
        When I check the Decompose condition
        Then the Decompose condition is not met

    # ===== Rule 8.4.15: Earth Bond — effects if earth card was pitched to play this =====

    Scenario: Earth Bond ability triggers when an Earth card was pitched to play the card
        Given a card with the "Earth Bond" label keyword
        When the card is played and an Earth card was pitched
        Then the Earth Bond condition is met

    Scenario: Earth Bond ability does not trigger when no Earth card was pitched
        Given a card with the "Earth Bond" label keyword
        When the card is played without pitching an Earth card
        Then the Earth Bond condition is not met

    # ===== Rule 8.4.16: Lightning Flow — effects if Lightning card was played this turn =====

    Scenario: Lightning Flow ability triggers when a Lightning card was played this turn
        Given a card with the "Lightning Flow" label keyword
        And a Lightning card was played this turn
        When I check the Lightning Flow condition
        Then the Lightning Flow condition is met

    Scenario: Lightning Flow ability does not trigger when no Lightning card was played this turn
        Given a card with the "Lightning Flow" label keyword
        And no Lightning card was played this turn
        When I check the Lightning Flow condition
        Then the Lightning Flow condition is not met

    # ===== Rule 8.4.17: Heavy — effects if it is the only card in weapon zones =====

    Scenario: Heavy ability triggers when the card is the only card equipped to weapon zones
        Given a card with the "Heavy" label keyword equipped to a weapon zone
        And no other card is equipped to weapon zones
        When I check the Heavy condition
        Then the Heavy condition is met

    Scenario: Heavy ability does not trigger when another card is also in a weapon zone
        Given a card with the "Heavy" label keyword equipped to a weapon zone
        And another card is also equipped to a weapon zone
        When I check the Heavy condition
        Then the Heavy condition is not met

    # ===== Rule 8.4.18: High Tide — effects if 2 or more blue cards in pitch zone =====

    Scenario: High Tide ability triggers when there are 2 or more blue cards in pitch zone
        Given a card with the "High Tide" label keyword
        And there are 2 blue cards in the pitch zone
        When I check the High Tide condition
        Then the High Tide condition is met

    Scenario: High Tide ability triggers when there are more than 2 blue cards in pitch zone
        Given a card with the "High Tide" label keyword
        And there are 3 blue cards in the pitch zone
        When I check the High Tide condition
        Then the High Tide condition is met

    Scenario: High Tide ability does not trigger when there is only 1 blue card in pitch zone
        Given a card with the "High Tide" label keyword
        And there is 1 blue card in the pitch zone
        When I check the High Tide condition
        Then the High Tide condition is not met

    Scenario: High Tide ability does not trigger when there are no blue cards in pitch zone
        Given a card with the "High Tide" label keyword
        And there are 0 blue cards in the pitch zone
        When I check the High Tide condition
        Then the High Tide condition is not met

    # ===== Rule 8.4.19: Go Fish — when hitting a hero, they reveal a card =====

    Scenario: Go Fish ability triggers when the card hits a hero
        Given a card with the "Go Fish" label keyword
        When the card hits a hero
        Then the Go Fish ability triggers and the hero must choose and reveal a card from hand

    Scenario: Go Fish creates a Gold token when the revealed card matches the adjective
        Given a card with the "Go Fish" label keyword requiring a blue card
        When the card hits a hero and the hero reveals a blue card
        Then the hero discards the revealed card
        And the Go Fish player creates a Gold token

    Scenario: Go Fish does not create a Gold token when the revealed card does not match
        Given a card with the "Go Fish" label keyword requiring a blue card
        When the card hits a hero and the hero reveals a red card
        Then the hero does not discard the revealed card
        And no Gold token is created
