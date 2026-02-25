# Feature file for Section 1.5: Macros
# Reference: Flesh and Blood Comprehensive Rules Section 1.5
#
# 1.5 Macros
#
# 1.5.1 A macro is a non-card object in the arena.
#   Note: A macro is not a card, even if it is represented by an official
#   Flesh and Blood card. Macros are determined by tournament rules for
#   specific formats.
#   Example: Sanctuary of Aria is a macro with the text "Instant -- {r}{r}:
#   Prevent the next 1 damage that would be dealt to you this turn by a source
#   of your choice. Destroy this at the beginning of the end phase."
#
# 1.5.1a A macro has no owner.
#
# 1.5.1b The controller of a macro is determined by the tournament rule that
#   created it.
#
# 1.5.2 A macro cannot be and is not considered part of a player's card-pool.
#   (ref 1.1.3)
#
# 1.5.3 If a macro leaves the arena, it is removed from the game.
#
# 8.1.13 Macro
#   A macro is not a card.
# 8.1.13a Only macro objects have the macro type. (ref 1.5)

Feature: Section 1.5 - Macros
    As a game engine
    I need to correctly implement macro objects
    So that tournament format macros like Sanctuary of Aria behave properly

    # ===========================================================
    # Rule 1.5.1: A macro is a non-card object in the arena
    # ===========================================================

    # Test for Rule 1.5.1 - Macro is a non-card object
    Scenario: Macro is a non-card game object in the arena
        Given a macro named "Sanctuary of Aria" exists in the arena
        When the engine evaluates the macro as a game object
        Then the macro should be recognized as a game object
        And the macro should NOT be recognized as a card

    # Test for Rule 1.5.1 - Macro is in the arena (not other zones)
    Scenario: Macro exists in the arena zone
        Given a macro named "Sanctuary of Aria" exists in the arena
        When checking the macro's location
        Then the macro should be in the arena
        And the macro should not be in any other zone

    # Test for Rule 1.5.1a - Macro has no owner
    Scenario: Macro has no owner
        Given a macro named "Sanctuary of Aria" exists in the arena
        When checking the macro's ownership
        Then the macro should have no owner
        And the macro owner_id should be None

    # Test for Rule 1.5.1b - Controller determined by tournament rule
    Scenario: Macro controller is determined by the tournament rule that created it
        Given a macro named "Sanctuary of Aria" exists in the arena
        And the macro was created by a tournament rule assigning controller player 0
        When checking the macro's controller
        Then the macro should have a controller
        And the macro controller_id should be 0

    # Test for Rule 1.5.1b - Different tournament rule assigns different controller
    Scenario: Macro controller can be assigned to any player by tournament rule
        Given a macro named "Sanctuary of Aria" exists in the arena
        And the macro was created by a tournament rule assigning controller player 1
        When checking the macro's controller
        Then the macro controller_id should be 1

    # ===========================================================
    # Rule 1.5.2: Macro is not part of a player's card-pool
    # ===========================================================

    # Test for Rule 1.5.2 - Macro excluded from card-pool
    Scenario: Macro is not part of any player's card-pool
        Given a macro named "Sanctuary of Aria" exists in the arena
        When validating if the macro is part of player 0's card-pool
        Then the macro should not be part of the card-pool

    # Test for Rule 1.5.2 - Macro is excluded even if represented by a physical card
    Scenario: Macro represented by a physical card is still not in card-pool
        Given a macro named "Sanctuary of Aria" exists in the arena
        And the macro is represented by a physical Flesh and Blood card
        When validating if the macro is part of player 0's card-pool
        Then the macro should not be part of the card-pool

    # ===========================================================
    # Rule 1.5.3: Macro leaving arena is removed from the game
    # ===========================================================

    # Test for Rule 1.5.3 - Macro leaving arena is removed
    Scenario: Macro leaving the arena is removed from the game
        Given a macro named "Sanctuary of Aria" exists in the arena
        When the macro leaves the arena
        Then the macro should be removed from the game
        And the macro should not exist in any zone

    # Test for Rule 1.5.3 - Unlike cards, macro doesn't go to graveyard
    Scenario: Macro is removed from game when destroyed, not sent to graveyard
        Given a macro named "Sanctuary of Aria" exists in the arena
        When the macro is destroyed
        Then the macro should be removed from the game
        And the macro should not appear in any graveyard

    # ===========================================================
    # Rule 8.1.13: Macro type keyword
    # ===========================================================

    # Test for Rule 8.1.13a - Only macros have the macro type
    Scenario: Only macro objects have the macro type
        Given a macro named "Sanctuary of Aria" exists in the arena
        And a regular card named "Bolt of Courage" exists in the hand
        When checking object types
        Then the macro should have the macro type
        And the regular card should not have the macro type

    # Test for Rule 1.5.1 / 8.1.13 - Macro has abilities defined by tournament rule
    Scenario: Macro can have abilities defined by the rule or effect that created it
        Given a macro named "Sanctuary of Aria" exists in the arena
        And the macro has the text "Instant -- {r}{r}: Prevent the next 1 damage"
        When the engine reads the macro's abilities
        Then the macro should have at least one ability
        And the abilities should be defined by the creating rule or effect
