# Feature file for Section 8.2: Subtype Keywords
# Reference: Flesh and Blood Comprehensive Rules Section 8.2
#
# 8.2.1 (1H)
#   8.2.1a A (1H) object is considered to be a one-hander.
#   8.2.1b A one-hander permanent must be equipped to a player's weapon zone.
#           A one-hander cannot be equipped if the player does not have an empty weapon zone.
#
# 8.2.2 (2H)
#   8.2.2a A (2H) object is considered to be a two-hander.
#   8.2.2b A two-hander permanent must be equipped to two of a player's weapon zones.
#           A two-hander cannot be equipped if the player does not have two empty weapon zones.
#   8.2.2c A two-hander occupies either of the two weapon zones it is equipped to, but not both.
#
# 8.2.3 Attack (subtype)
#   8.2.3a An attack card is considered an attack when on the stack or when it is on the
#           combat chain as an attacking card.
#   8.2.3b When an attack card is played, the combat chain opens (if it is closed) and the
#           layer step of combat begins.
#
# 8.2.4 Aura
#   8.2.4a When an aura resolves as a layer on the stack, it enters the arena.
#   8.2.4b When an aura enters the arena, it becomes a permanent, except when it is added
#           as a defending card to a chain link.
#
# 8.2.5 Item
#   8.2.5a When an item resolves as a layer on the stack, it enters the arena.
#   8.2.5b When an item enters the arena, it becomes a permanent, except when it is added
#           as a defending card to a chain link.
#
# 8.2.6 Arrow
#   8.2.6a An arrow can only be played from the player's arsenal and only if they control a bow.
#
# 8.2.7 Trap
#   Note: As of 2023, trap is no longer a functional subtype keyword.
#
# 8.2.8 Ally
#   8.2.8a If an ally permanent ceases to exist, it is considered to have died.
#   8.2.8b During the End Phase, an ally's life total is reset to its base life.
#   8.2.8c If an ally is attacking, the controlling player and their hero are not considered
#           an attacking hero for that chain link.
#   8.2.8d If an ally is the target of an attack, the controlling player and their hero are
#           not considered a defending hero for that chain link; and the player cannot declare
#           defending cards or play or activate defense reaction cards or abilities during the
#           reaction step of combat.
#   8.2.8e If an ally deals damage, the controlling player and their hero are not considered
#           to have dealt damage.
#   8.2.8f If an ally is dealt damage, the controlling player and their hero are not considered
#           to have been dealt damage.
#
# 8.2.9 Landmark
#   8.2.9a When a landmark resolves as a layer on the stack, it enters the arena.
#   8.2.9b When a landmark enters the arena, it becomes a permanent and all other landmark
#           permanents are cleared, except when the landmark is added as a defending card
#           to a chain link.
#
# 8.2.10 Off-Hand
#   8.2.10a An off-hand permanent must be equipped to a player's weapon zone. An off-hand
#            cannot be equipped if the player does not have an empty weapon zone.
#   8.2.10b A player cannot equip more than one off-hand.
#
# 8.2.11 Affliction
#   8.2.11a When an affliction resolves as a layer on the stack, it enters the arena.
#   8.2.11b When an affliction enters the arena, it becomes a permanent, except when it is
#            added as a defending card to a chain link.
#   8.2.11c As an object with the subtype affliction enters the arena as a permanent, its
#            controller declares an opponent and the object enters the arena under that
#            player's control. If the affliction has no controller before it enters the
#            arena, its owner declares the opponent. If the object cannot enter the arena
#            under that player's control, it is cleared and is not considered to have
#            entered the arena.
#
# 8.2.12 Ash
#   8.2.12a When an ash resolves as a layer on the stack, it enters the arena.
#   8.2.12b When an ash enters the arena, it becomes a permanent, except when it is added
#            as a defending card to a chain link.
#
# 8.2.13 Invocation
#   8.2.13a When an invocation resolves as a layer on the stack, it enters the arena with
#            its back-face active and becomes a permanent.
#
# 8.2.14 Construct
#   8.2.14a When a construct resolves as a layer on the stack, it enters the arena with
#            its back-face active and becomes a permanent.
#
# 8.2.15 Quiver
#   8.2.15a A quiver permanent must be equipped to a player's weapon zone. A quiver may be
#            equipped to, and occupy, a weapon zone that a two-hander bow is already equipped
#            to but does not occupy; otherwise, a quiver cannot be equipped if the player does
#            not have an empty weapon zone.
#   8.2.15b A player cannot equip more than one quiver.
#
# 8.2.16 Figment
#   8.2.16a When a figment resolves as a layer on the stack, it enters the arena.
#   8.2.16b When a figment enters the arena, it becomes a permanent, except when it is added
#            as a defending card to a chain link.

Feature: Section 8.2 - Subtype Keywords
    As a game engine
    I need to correctly implement subtype keyword rules
    So that objects with subtype keywords behave according to their functional rules

    # ===== 8.2.1 (1H) One-Hander =====

    Scenario: 1H object is considered a one-hander
        Given a card with the subtype "(1H)"
        When the game checks the object's handedness
        Then the object is considered a one-hander

    Scenario: One-hander requires an empty weapon zone to equip
        Given a card with the subtype "(1H)"
        And the player has an empty weapon zone
        When the game checks if the one-hander can be equipped
        Then the one-hander can be equipped to the weapon zone

    Scenario: One-hander cannot be equipped without an empty weapon zone
        Given a card with the subtype "(1H)"
        And all of the player's weapon zones are occupied
        When the game checks if the one-hander can be equipped
        Then the one-hander cannot be equipped

    # ===== 8.2.2 (2H) Two-Hander =====

    Scenario: 2H object is considered a two-hander
        Given a card with the subtype "(2H)"
        When the game checks the object's handedness
        Then the object is considered a two-hander

    Scenario: Two-hander requires two empty weapon zones to equip
        Given a card with the subtype "(2H)"
        And the player has two empty weapon zones
        When the game checks if the two-hander can be equipped
        Then the two-hander can be equipped to two weapon zones

    Scenario: Two-hander cannot be equipped with only one empty weapon zone
        Given a card with the subtype "(2H)"
        And the player has only one empty weapon zone
        When the game checks if the two-hander can be equipped
        Then the two-hander cannot be equipped

    Scenario: Two-hander occupies either weapon zone but not both
        Given a card with the subtype "(2H)"
        And the two-hander is equipped to two weapon zones
        When the game checks which weapon zones the two-hander occupies
        Then the two-hander occupies one of the two weapon zones
        And the two-hander does not occupy both weapon zones simultaneously

    # ===== 8.2.3 Attack (subtype) =====

    Scenario: Attack card is considered an attack when on the stack
        Given a card with the subtype "Attack"
        And the card is on the stack
        When the game checks if the card is an attack
        Then the card is considered an attack

    Scenario: Attack card is considered an attack when on the combat chain
        Given a card with the subtype "Attack"
        And the card is on the combat chain as an attacking card
        When the game checks if the card is an attack
        Then the card is considered an attack

    Scenario: Playing an attack card opens the combat chain
        Given a card with the subtype "Attack"
        And the combat chain is closed
        When the player plays the attack card
        Then the combat chain opens
        And the layer step of combat begins

    # ===== 8.2.4 Aura =====

    Scenario: Aura enters the arena when it resolves as a layer
        Given a card with the subtype "Aura"
        And the aura is resolving as a layer on the stack
        When the resolution completes
        Then the aura enters the arena

    Scenario: Aura becomes a permanent when it enters the arena
        Given a card with the subtype "Aura"
        And the aura has entered the arena
        When the game checks the aura's status
        Then the aura is a permanent in the arena

    Scenario: Aura added as defending card does not become a permanent
        Given a card with the subtype "Aura"
        And the aura is added as a defending card to a chain link
        When the game checks the aura's status
        Then the aura is not considered a permanent

    # ===== 8.2.5 Item =====

    Scenario: Item enters the arena when it resolves as a layer
        Given a card with the subtype "Item"
        And the item is resolving as a layer on the stack
        When the resolution completes
        Then the item enters the arena

    Scenario: Item becomes a permanent when it enters the arena
        Given a card with the subtype "Item"
        And the item has entered the arena
        When the game checks the item's status
        Then the item is a permanent in the arena

    Scenario: Item added as defending card does not become a permanent
        Given a card with the subtype "Item"
        And the item is added as a defending card to a chain link
        When the game checks the item's status
        Then the item is not considered a permanent

    # ===== 8.2.6 Arrow =====

    Scenario: Arrow can be played from arsenal when player controls a bow
        Given a card with the subtype "Arrow"
        And the arrow is in the player's arsenal
        And the player controls a weapon with the subtype "Bow"
        When the game checks if the arrow can be played
        Then the arrow can be played

    Scenario: Arrow cannot be played from hand even with a bow
        Given a card with the subtype "Arrow"
        And the arrow is in the player's hand
        And the player controls a weapon with the subtype "Bow"
        When the game checks if the arrow can be played
        Then the arrow cannot be played because it is not in the arsenal

    Scenario: Arrow cannot be played without controlling a bow
        Given a card with the subtype "Arrow"
        And the arrow is in the player's arsenal
        And the player does not control a bow
        When the game checks if the arrow can be played
        Then the arrow cannot be played because the player does not control a bow

    # ===== 8.2.7 Trap =====

    Scenario: Trap is no longer a functional subtype keyword
        Given a card with the subtype "Trap"
        When the game checks if trap provides additional functional rules
        Then trap does not add additional rules to the object

    # ===== 8.2.8 Ally =====

    Scenario: Ally permanent ceasing to exist is considered to have died
        Given an ally permanent in the arena
        When the ally permanent ceases to exist
        Then the ally is considered to have died

    Scenario: Ally life total resets to base life during End Phase
        Given an ally permanent with a modified life total
        When the End Phase begins
        Then the ally's life total is reset to its base life

    Scenario: Ally attacking does not make controlling player an attacking hero
        Given an ally permanent that is attacking
        When the game checks who is the attacking hero for the chain link
        Then the controlling player is not considered the attacking hero
        And the controlling player's hero is not considered the attacking hero

    Scenario: Ally as attack target does not make controlling player a defending hero
        Given an ally permanent that is the target of an attack
        When the game checks who is the defending hero for the chain link
        Then the controlling player is not considered the defending hero
        And the controlling player's hero is not considered the defending hero

    Scenario: Controlling player cannot declare defenders when ally is attack target
        Given an ally permanent that is the target of an attack
        And the game is in the Defend Step of combat
        When the controlling player attempts to declare defending cards
        Then the controlling player cannot declare defending cards

    Scenario: Controlling player cannot play defense reactions when ally is attack target
        Given an ally permanent that is the target of an attack
        And the game is in the Reaction Step of combat
        When the controlling player attempts to play a defense reaction card
        Then the defense reaction cannot be played because the ally is the attack target

    Scenario: Ally dealing damage does not count as controlling player dealing damage
        Given an ally permanent that deals damage to an opposing hero
        When the game checks who dealt damage
        Then the controlling player is not considered to have dealt damage
        And the controlling player's hero is not considered to have dealt damage

    Scenario: Ally being dealt damage does not count as controlling player being dealt damage
        Given an ally permanent that is dealt damage
        When the game checks who was dealt damage
        Then the controlling player is not considered to have been dealt damage
        And the controlling player's hero is not considered to have been dealt damage

    # ===== 8.2.9 Landmark =====

    Scenario: Landmark enters the arena when it resolves as a layer
        Given a card with the subtype "Landmark"
        And the landmark is resolving as a layer on the stack
        When the resolution completes
        Then the landmark enters the arena

    Scenario: Landmark becomes a permanent and clears other landmarks
        Given a card with the subtype "Landmark"
        And there is already a landmark permanent in the arena
        When the new landmark enters the arena
        Then the new landmark becomes a permanent
        And the previous landmark permanent is cleared from the arena

    Scenario: Landmark added as defending card does not clear other landmarks
        Given a card with the subtype "Landmark"
        And the landmark is added as a defending card to a chain link
        And there is already a landmark permanent in the arena
        When the game processes the landmark as a defending card
        Then the existing landmark permanent is not cleared

    # ===== 8.2.10 Off-Hand =====

    Scenario: Off-hand requires an empty weapon zone to equip
        Given a card with the subtype "Off-Hand"
        And the player has an empty weapon zone
        When the game checks if the off-hand can be equipped
        Then the off-hand can be equipped to the weapon zone

    Scenario: Off-hand cannot be equipped without an empty weapon zone
        Given a card with the subtype "Off-Hand"
        And all of the player's weapon zones are occupied
        When the game checks if the off-hand can be equipped
        Then the off-hand cannot be equipped

    Scenario: Player cannot equip more than one off-hand
        Given a card with the subtype "Off-Hand"
        And the player already has an off-hand equipped
        And the player has an empty weapon zone
        When the game checks if the second off-hand can be equipped
        Then the second off-hand cannot be equipped because the player already has one

    # ===== 8.2.11 Affliction =====

    Scenario: Affliction enters the arena when it resolves as a layer
        Given a card with the subtype "Affliction"
        And the affliction is resolving as a layer on the stack
        When the resolution completes
        Then the affliction enters the arena

    Scenario: Affliction becomes a permanent under an opponent's control
        Given a card with the subtype "Affliction"
        And the affliction is controlled by a player with an opponent
        When the affliction enters the arena
        Then the controller declares an opponent
        And the affliction enters the arena under that opponent's control
        And the affliction is a permanent

    Scenario: Affliction owner declares opponent when affliction has no controller
        Given a card with the subtype "Affliction"
        And the affliction has no controller before entering the arena
        When the affliction enters the arena
        Then the affliction's owner declares an opponent
        And the affliction enters the arena under that opponent's control

    Scenario: Affliction is cleared if it cannot enter arena under opponent's control
        Given a card with the subtype "Affliction"
        And the affliction cannot enter the arena under any opponent's control
        When the affliction attempts to enter the arena
        Then the affliction is cleared
        And the affliction is not considered to have entered the arena

    Scenario: Affliction added as defending card does not become a permanent
        Given a card with the subtype "Affliction"
        And the affliction is added as a defending card to a chain link
        When the game checks the affliction's status
        Then the affliction is not considered a permanent

    # ===== 8.2.12 Ash =====

    Scenario: Ash enters the arena when it resolves as a layer
        Given a card with the subtype "Ash"
        And the ash is resolving as a layer on the stack
        When the resolution completes
        Then the ash enters the arena

    Scenario: Ash becomes a permanent when it enters the arena
        Given a card with the subtype "Ash"
        And the ash has entered the arena
        When the game checks the ash's status
        Then the ash is a permanent in the arena

    Scenario: Ash added as defending card does not become a permanent
        Given a card with the subtype "Ash"
        And the ash is added as a defending card to a chain link
        When the game checks the ash's status
        Then the ash is not considered a permanent

    # ===== 8.2.13 Invocation =====

    Scenario: Invocation enters arena with back-face active when it resolves
        Given a card with the subtype "Invocation"
        And the invocation is resolving as a layer on the stack
        When the resolution completes
        Then the invocation enters the arena with its back-face active
        And the invocation becomes a permanent

    # ===== 8.2.14 Construct =====

    Scenario: Construct enters arena with back-face active when it resolves
        Given a card with the subtype "Construct"
        And the construct is resolving as a layer on the stack
        When the resolution completes
        Then the construct enters the arena with its back-face active
        And the construct becomes a permanent

    # ===== 8.2.15 Quiver =====

    Scenario: Quiver requires an empty weapon zone to equip
        Given a card with the subtype "Quiver"
        And the player has an empty weapon zone
        When the game checks if the quiver can be equipped
        Then the quiver can be equipped to the weapon zone

    Scenario: Quiver can share weapon zone occupied by a two-hander bow
        Given a card with the subtype "Quiver"
        And the player has a two-hander bow equipped that does not occupy one of the weapon zones
        When the game checks if the quiver can be equipped to the unoccupied zone
        Then the quiver can be equipped to the weapon zone alongside the two-hander bow

    Scenario: Quiver cannot be equipped without an empty or bow-sharing weapon zone
        Given a card with the subtype "Quiver"
        And all of the player's weapon zones are occupied by non-bow permanents
        When the game checks if the quiver can be equipped
        Then the quiver cannot be equipped

    Scenario: Player cannot equip more than one quiver
        Given a card with the subtype "Quiver"
        And the player already has a quiver equipped
        And the player has an empty weapon zone
        When the game checks if the second quiver can be equipped
        Then the second quiver cannot be equipped because the player already has one

    # ===== 8.2.16 Figment =====

    Scenario: Figment enters the arena when it resolves as a layer
        Given a card with the subtype "Figment"
        And the figment is resolving as a layer on the stack
        When the resolution completes
        Then the figment enters the arena

    Scenario: Figment becomes a permanent when it enters the arena
        Given a card with the subtype "Figment"
        And the figment has entered the arena
        When the game checks the figment's status
        Then the figment is a permanent in the arena

    Scenario: Figment added as defending card does not become a permanent
        Given a card with the subtype "Figment"
        And the figment is added as a defending card to a chain link
        When the game checks the figment's status
        Then the figment is not considered a permanent
