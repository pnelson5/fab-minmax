# Feature file for Section 8.1: Type Keywords
# Reference: Flesh and Blood Comprehensive Rules Section 8.1
#
# 8.1.1 Action
#   An action card is a deck-card.
#   8.1.1a An action card/activated ability can only be played/activated when the stack is empty.
#   8.1.1b An action card/activated ability cannot be played/activated during combat, except
#           during the Resolution Step of combat.
#   8.1.1c An action card/activated ability has the additional asset-cost of one action point
#           to play/activate.
#   8.1.1d If an action card/activated ability is played/activated as though it were an instant,
#           it is still considered an action, but it can be played/activated any time the player
#           has priority and does not cost an action point.
#
# 8.1.2 Attack Reaction
#   An attack reaction card is a deck-card.
#   8.1.2a An attack reaction card/activated ability can only be played/activated by a player
#           who controls the attack during the Reaction Step of combat.
#   8.1.2b When an attack reaction card resolves as a layer on the stack, it is cleared.
#   8.1.2c An attack reaction card/activated ability is considered to be a reaction card/ability.
#
# 8.1.3 Defense Reaction
#   A defense reaction card is a deck-card.
#   8.1.3a A defense reaction card/activated ability can only be played/activated by a player
#           who controls a hero as an attack-target during the Reaction Step of combat.
#   8.1.3b When a defense reaction card resolves as a layer on the stack, it becomes a defending
#           card on the active chain link.
#   8.1.3c A defense reaction card/activated ability is considered to be a reaction card/ability.
#
# 8.1.4 Equipment
#   An equipment card (without any other types) is an arena-card.
#   8.1.4a As an arena-card, a player may equip an equipment card from their card-pool during
#           the start-of-game procedure to its respective zone.
#   8.1.4b An equipment permanent may be declared as a defending card during the Defend Step.
#
# 8.1.5 Hero
#   A hero card is a hero-card.
#   8.1.5a A player starts the game with their hero card as a permanent in their hero zone.
#   8.1.5b A hero card is separate from, and cannot be included in a player's, card-pool.
#
# 8.1.6 Instant
#   An instant card is a deck-card.
#   8.1.6a A card/activated ability with the type instant can be played/activated any time the
#           player has priority.
#
# 8.1.7 Resource
#   A resource card is a deck-card.
#   8.1.7a A resource card cannot be played.
#
# 8.1.8 Token
#   A token card is a token-card.
#   8.1.8a Tokens only exist in the arena or as sub-cards. If a token leaves the arena and it
#           is not a sub-card, it ceases to exist.
#
# 8.1.9 Weapon
#   A weapon card is an arena-card.
#   8.1.9a As an arena-card, a player may equip a weapon card from their card-pool during the
#           start-of-game procedure to its respective zone.
#
# 8.1.10 Mentor
#   A mentor card is a deck-card.
#   8.1.10a A mentor card can only be included in a player's card-pool if they have a young
#            (subtype) hero.
#
# 8.1.11 Demi-Hero
#   A demi-hero card is an arena-card.
#   8.1.11a A demi-hero card is distinct from a hero-card. It is included as part of a player's
#            card-pool and it cannot be used in place of a player's hero at the start of the game.
#   8.1.11b If a demi-hero becomes a permanent in the arena and the controlling player does not
#            control a hero, the demi-hero is considered to be that player's hero and has the
#            hero type for the rest of the game. Otherwise, if the player already controls a
#            hero, the demi-hero is cleared from the arena.
#
# 8.1.12 Block
#   A block card is a deck-card.
#   8.1.12a A block card cannot be played.
#
# 8.1.13 Macro
#   A macro is not a card.
#   8.1.13a Only macro objects have the macro type.
#
# 8.1.14 Companion
#   A companion card is an arena-card.

Feature: Section 8.1 - Type Keywords
    As a game engine
    I need to correctly implement type keyword rules for each card type
    So that cards behave according to their type's specific restrictions and abilities

    # ===== 8.1.1 Action =====

    Scenario: Action card is a deck-card
        Given a card with the type "Action"
        When the game categorizes the card
        Then the card is categorized as a deck-card

    Scenario: Action card can only be played when the stack is empty
        Given a card with the type "Action"
        And the stack is empty
        When the player attempts to play the action card
        Then the play attempt is allowed by the type restriction

    Scenario: Action card cannot be played when the stack is not empty
        Given a card with the type "Action"
        And another layer is on the stack
        When the player attempts to play the action card
        Then the play attempt is denied because the stack is not empty

    Scenario: Action card cannot be played during combat outside Resolution Step
        Given a card with the type "Action"
        And the game is in the Reaction Step of combat
        When the player attempts to play the action card
        Then the play attempt is denied because it is during combat

    Scenario: Action card can be played during the Resolution Step of combat
        Given a card with the type "Action"
        And the game is in the Resolution Step of combat
        When the player attempts to play the action card
        Then the play attempt is allowed during the Resolution Step

    Scenario: Action card requires one action point as additional asset-cost
        Given a card with the type "Action"
        And the player has one action point
        When the game evaluates the action card's cost
        Then one action point is required as an additional asset-cost

    Scenario: Action card played as instant is still considered an action
        Given a card with the type "Action"
        And an effect allows playing the action card as though it were an instant
        When the player plays the action card as an instant
        Then the card is still considered an action card
        And the card does not cost an action point to play
        And the card can be played any time the player has priority

    # ===== 8.1.2 Attack Reaction =====

    Scenario: Attack reaction card is a deck-card
        Given a card with the type "Attack Reaction"
        When the game categorizes the card
        Then the card is categorized as a deck-card

    Scenario: Attack reaction can only be played by attack controller during Reaction Step
        Given a card with the type "Attack Reaction"
        And the game is in the Reaction Step of combat
        And the player controls the current attack
        When the player attempts to play the attack reaction card
        Then the play attempt is allowed by the type restriction

    Scenario: Attack reaction cannot be played by non-attack-controller
        Given a card with the type "Attack Reaction"
        And the game is in the Reaction Step of combat
        And the player does not control the current attack
        When the player attempts to play the attack reaction card
        Then the play attempt is denied because the player does not control the attack

    Scenario: Attack reaction card is cleared when it resolves as a layer
        Given an attack reaction card that has resolved as a layer on the stack
        When the resolution step processes the layer
        Then the attack reaction card is cleared from the game

    Scenario: Attack reaction card is considered a reaction card
        Given a card with the type "Attack Reaction"
        When the game checks whether the card is a reaction card
        Then the card is considered a reaction card

    # ===== 8.1.3 Defense Reaction =====

    Scenario: Defense reaction card is a deck-card
        Given a card with the type "Defense Reaction"
        When the game categorizes the card
        Then the card is categorized as a deck-card

    Scenario: Defense reaction can only be played by hero attack-target controller during Reaction Step
        Given a card with the type "Defense Reaction"
        And the game is in the Reaction Step of combat
        And the player controls a hero that is an attack-target
        When the player attempts to play the defense reaction card
        Then the play attempt is allowed by the type restriction

    Scenario: Defense reaction cannot be played by player who does not control attack-target hero
        Given a card with the type "Defense Reaction"
        And the game is in the Reaction Step of combat
        And the player does not control a hero that is an attack-target
        When the player attempts to play the defense reaction card
        Then the play attempt is denied because the player's hero is not an attack-target

    Scenario: Defense reaction card becomes a defending card when it resolves
        Given a defense reaction card that has resolved as a layer on the stack
        When the resolution step processes the layer
        Then the defense reaction card becomes a defending card on the active chain link

    Scenario: Defense reaction card is considered a reaction card
        Given a card with the type "Defense Reaction"
        When the game checks whether the card is a reaction card
        Then the card is considered a reaction card

    # ===== 8.1.4 Equipment =====

    Scenario: Equipment card is an arena-card
        Given a card with the type "Equipment"
        When the game categorizes the card
        Then the card is categorized as an arena-card

    Scenario: Equipment card can be equipped from card-pool at game start
        Given a card with the type "Equipment"
        And the card is in the player's card-pool
        And the game is in the start-of-game procedure
        When the player equips the equipment card
        Then the equipment is placed in its respective equipment zone

    Scenario: Equipment permanent can be declared as a defending card
        Given an equipment permanent in a player's equipment zone
        And the game is in the Defend Step of combat
        When the player declares the equipment as a defending card
        Then the declaration is allowed for the equipment permanent

    # ===== 8.1.5 Hero =====

    Scenario: Hero card is a hero-card
        Given a card with the type "Hero"
        When the game categorizes the card
        Then the card is categorized as a hero-card

    Scenario: Hero card starts as a permanent in the hero zone
        Given a player has a hero card
        When the game starts
        Then the hero card is a permanent in the player's hero zone

    Scenario: Hero card cannot be included in a player's card-pool
        Given a card with the type "Hero"
        When the game checks if the hero card can be included in a card-pool
        Then the hero card cannot be included in a player's card-pool

    # ===== 8.1.6 Instant =====

    Scenario: Instant card is a deck-card
        Given a card with the type "Instant"
        When the game categorizes the card
        Then the card is categorized as a deck-card

    Scenario: Instant card can be played any time player has priority
        Given a card with the type "Instant"
        And the player has priority
        When the game checks when the instant card can be played
        Then the instant can be played at any time the player has priority

    # ===== 8.1.7 Resource =====

    Scenario: Resource card is a deck-card
        Given a card with the type "Resource"
        When the game categorizes the card
        Then the card is categorized as a deck-card

    Scenario: Resource card cannot be played
        Given a card with the type "Resource"
        When the player attempts to play the resource card
        Then the play attempt is denied because resource cards cannot be played

    # ===== 8.1.8 Token =====

    Scenario: Token card is a token-card
        Given a card with the type "Token"
        When the game categorizes the card
        Then the card is categorized as a token-card

    Scenario: Token only exists in the arena or as a sub-card
        Given a token permanent in the arena
        When the game checks the token's valid locations
        Then the token can exist in the arena
        And the token can exist as a sub-card

    Scenario: Token ceases to exist when it leaves the arena and is not a sub-card
        Given a token permanent in the arena
        And the token is not a sub-card
        When the token leaves the arena
        Then the token ceases to exist

    # ===== 8.1.9 Weapon =====

    Scenario: Weapon card is an arena-card
        Given a card with the type "Weapon"
        When the game categorizes the card
        Then the card is categorized as an arena-card

    Scenario: Weapon card can be equipped from card-pool at game start
        Given a card with the type "Weapon"
        And the card is in the player's card-pool
        And the game is in the start-of-game procedure
        When the player equips the weapon card
        Then the weapon is placed in its respective weapon zone

    # ===== 8.1.10 Mentor =====

    Scenario: Mentor card is a deck-card
        Given a card with the type "Mentor"
        When the game categorizes the card
        Then the card is categorized as a deck-card

    Scenario: Mentor card can only be in card-pool with a young hero
        Given a card with the type "Mentor"
        And the player's hero has the young subtype
        When the game checks if the mentor card can be included in the card-pool
        Then the mentor card is allowed in the card-pool

    Scenario: Mentor card cannot be in card-pool without a young hero
        Given a card with the type "Mentor"
        And the player's hero does not have the young subtype
        When the game checks if the mentor card can be included in the card-pool
        Then the mentor card is not allowed in the card-pool

    # ===== 8.1.11 Demi-Hero =====

    Scenario: Demi-hero card is an arena-card
        Given a card with the type "Demi-Hero"
        When the game categorizes the card
        Then the card is categorized as an arena-card

    Scenario: Demi-hero card is included in the player's card-pool
        Given a card with the type "Demi-Hero"
        When the game checks the demi-hero's card classification
        Then the demi-hero is included as part of the player's card-pool
        And the demi-hero cannot be used in place of a player's hero at game start

    Scenario: Demi-hero becomes player's hero when no hero is controlled
        Given a demi-hero permanent in the arena
        And the controlling player does not control a hero
        When the demi-hero becomes a permanent in the arena
        Then the demi-hero is considered to be that player's hero
        And the demi-hero has the hero type for the rest of the game

    Scenario: Demi-hero is cleared when player already controls a hero
        Given a demi-hero that has just become a permanent in the arena
        And the controlling player already controls a hero
        When the game resolves the demi-hero's arrival
        Then the demi-hero is cleared from the arena

    # ===== 8.1.12 Block =====

    Scenario: Block card is a deck-card
        Given a card with the type "Block"
        When the game categorizes the card
        Then the card is categorized as a deck-card

    Scenario: Block card cannot be played
        Given a card with the type "Block"
        When the player attempts to play the block card
        Then the play attempt is denied because block cards cannot be played

    # ===== 8.1.13 Macro =====

    Scenario: Macro objects have the macro type
        Given a macro object exists in the game
        When the game checks the macro object's type
        Then the macro object has the macro type

    Scenario: Only macro objects have the macro type
        Given a card that is not a macro object
        When the game checks if the card has the macro type
        Then the card does not have the macro type

    # ===== 8.1.14 Companion =====

    Scenario: Companion card is an arena-card
        Given a card with the type "Companion"
        When the game categorizes the card
        Then the card is categorized as an arena-card
