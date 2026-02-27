# Feature file for Section 2.5: Life
# Reference: Flesh and Blood Comprehensive Rules Section 2.5
#
# 2.5.1 Life is a numeric property of an object, which represents the starting
#        life total of that object.
#
# 2.5.1a A permanent with the life property is a living object. [1.3.3]
#
# 2.5.2 The printed life of a card is typically located at the bottom right
#        corner of a card next to the {h} symbol. The printed life defines the
#        base life of a card. If a card does not have a printed life, it does
#        not have the life property (0 is a valid printed life).
#
# 2.5.3 The life of a permanent can be modified. The term "life total" or the
#        symbol {h} refers to the modified life of an object.
#
# 2.5.3a A permanent's life total is equal to the permanent's base life, plus
#         life gained and minus life lost, as recorded by the players of the game.
#
# 2.5.3b Life gained and life lost are not continuous effects - they are discrete
#         effects that apply once, and they permanently modify the life total. [8.5.7]
#
# 2.5.3c If the base life of a permanent changes, then the life total is
#         recalculated using the new base life value of the object.
#         Example: Shiyana has 20 base life and copies Kano (15 base life).
#         If Shiyana lost 5 life, the new total is 10 (15 - 5).
#
# 2.5.3d A permanent's life total can be greater than its base life.
#
# 2.5.3e A permanent cannot have a negative life total. If the life total is
#         calculated to be less than zero, instead it is considered zero.
#
# 2.5.3f If a permanent's life total is reduced to zero, it is cleared as a
#         game state action; or if the permanent is a hero, their player loses
#         or the game is a draw as a game state action. [1.10.2][4.5]
#
# 2.5.3g If a living object ceases to exist, it is considered to have died.

Feature: Section 2.5 - Life
    As a game engine
    I need to correctly implement life rules
    So that life totals are tracked, modified, and enforced correctly

    # Rule 2.5.1 - Life is a numeric property
    Scenario: Life is a numeric property of an object
        Given a hero card named numeric hero with a printed life of 20
        When the engine checks the life property of the numeric hero
        Then the numeric hero should have the life property
        And the life of the numeric hero should be 20
        And the life of the numeric hero should be numeric

    # Rule 2.5.1 - Life represents the starting life total
    Scenario: Life property represents the starting life total
        Given a hero card named starting total hero with a printed life of 40
        When the engine checks the starting life total of the starting total hero
        Then the starting life total of the starting total hero should be 40

    # Rule 2.5.1a - Permanent with life property is a living object
    Scenario: Permanent with life property is a living object
        Given a permanent card named living ally with a printed life of 3
        And the living ally permanent is placed in the arena
        When the engine checks if the living ally is a living object
        Then the living ally should be a living object

    # Rule 2.5.1a - Permanent without life property is not a living object
    Scenario: Permanent without life property is not a living object
        Given a permanent card named lifeless equipment with no life property
        And the lifeless equipment permanent is placed in the arena
        When the engine checks if the lifeless equipment is a living object
        Then the lifeless equipment should not be a living object

    # Rule 2.5.1a - Non-permanent card is not a living object even with life
    Scenario: Non-permanent card is not a living object even if it has a life property
        Given a non-permanent card named temporary creature with a printed life of 5
        When the engine checks if the temporary creature is a living object
        Then the temporary creature should not be a living object

    # Rule 2.5.2 - Printed life defines base life
    Scenario: Printed life defines the base life of a card
        Given a hero card named base life hero with a printed life of 20
        When the engine checks the base life of the base life hero
        Then the base life of the base life hero should be 20

    # Rule 2.5.2 - Zero is a valid printed life
    Scenario: Zero is a valid printed life
        Given a card named zero life card with a printed life of 0
        When the engine checks the life property of the zero life card
        Then the zero life card should have the life property
        And the life of the zero life card should be 0

    # Rule 2.5.2 - No printed life means no life property
    Scenario: Card without a printed life lacks the life property
        Given a card named no life card with no printed life
        When the engine checks the life property of the no life card
        Then the no life card should not have the life property

    # Rule 2.5.3 - Life of a permanent can be modified
    Scenario: Life of a hero can be modified by effects
        Given a hero card named modify test hero with a printed life of 20
        And a life loss effect of 5 is applied to the modify test hero
        When the engine checks the modified life total of the modify test hero
        Then the modified life total of the modify test hero should be 15

    # Rule 2.5.3 - "life total" refers to modified life
    Scenario: The term life total refers to the modified life not base life
        Given a hero card named life total term hero with a printed life of 20
        And a life gain effect of 3 is applied to the life total term hero
        When the engine resolves the term life total for the life total term hero
        Then the resolved life total of the life total term hero should be 23
        And the base life of the life total term hero should remain 20

    # Rule 2.5.3 - {h} symbol refers to modified life
    Scenario: The symbol h refers to the modified life total of an object
        Given a hero card named h symbol hero with a printed life of 20
        And a life loss effect of 5 is applied to the h symbol hero
        When the engine resolves the h symbol for the h symbol hero
        Then the resolved h symbol value for h symbol hero should be 15

    # Rule 2.5.3a - Life total equals base life plus gained minus lost
    Scenario: Life total equals base life plus life gained minus life lost
        Given a hero card named formula hero with a printed life of 20
        And the formula hero gains 5 life
        And the formula hero loses 3 life
        When the engine calculates the life total of the formula hero
        Then the formula hero life total should be 22

    # Rule 2.5.3a - Multiple life events accumulate
    Scenario: Multiple life gain and loss events accumulate in the life total
        Given a hero card named accumulate hero with a printed life of 20
        And the accumulate hero gains 2 life in a first event
        And the accumulate hero gains 4 life in a second event
        And the accumulate hero loses 1 life in a third event
        When the engine calculates the accumulated life total of the accumulate hero
        Then the accumulate hero life total should be 25

    # Rule 2.5.3b - Life gained and lost are discrete effects (not continuous)
    Scenario: Life gained and life lost are discrete effects not continuous
        Given a hero card named discrete hero with a printed life of 20
        And a discrete life gain of 5 is applied to the discrete hero
        When the discrete hero life gain source is removed
        Then the discrete hero life total should remain 25

    # Rule 2.5.3b - Discrete life effects permanently modify life total
    Scenario: Discrete life effects permanently modify life total
        Given a hero card named permanent mod hero with a printed life of 20
        And a permanent life gain of 3 is applied to the permanent mod hero
        When the engine checks the permanent mod hero life total
        Then the permanent mod hero life total should be 23

    # Rule 2.5.3c - Base life change recalculates life total (Shiyana example)
    Scenario: Changing base life recalculates life total preserving life lost
        Given a hero card named Shiyana with a printed life of 20
        And the Shiyana hero loses 5 life
        And the Shiyana hero base life changes to 15 via copy
        When the engine recalculates the Shiyana hero life total
        Then the Shiyana hero life total should be 10

    # Rule 2.5.3c - Base life change with life gained preserves gained
    Scenario: Changing base life recalculates life total preserving life gained
        Given a hero card named Copycat with a printed life of 20
        And the Copycat hero gains 3 life
        And the Copycat hero base life changes to 10 via copy
        When the engine recalculates the Copycat hero life total
        Then the Copycat hero life total should be 13

    # Rule 2.5.3d - Life total can exceed base life
    Scenario: Life total can be greater than base life
        Given a hero card named exceed hero with a printed life of 20
        And a life gain effect of 5 is applied to the exceed hero
        When the engine checks if the exceed hero life total exceeds base life
        Then the exceed hero life total of 25 should exceed base life of 20

    # Rule 2.5.3e - Life total cannot be negative
    Scenario: Life total cannot be negative and is capped at zero
        Given a hero card named low life hero with a printed life of 5
        And a life loss effect of 10 is applied to the low life hero
        When the engine calculates the low life hero capped life total
        Then the low life hero capped life total should be 0

    # Rule 2.5.3e - Life total exactly at zero remains zero
    Scenario: Life total reduced to exactly zero is zero not negative
        Given a hero card named exact zero hero with a printed life of 5
        And a life loss effect of 5 is applied to the exact zero hero
        When the engine checks the exact zero hero life total
        Then the exact zero hero life total should be exactly 0

    # Rule 2.5.3f - Hero reaching zero life causes loss or draw
    Scenario: Hero reaching zero life is handled as a game state action
        Given a hero card named dying hero with a printed life of 20
        And a life loss effect of 20 is applied to the dying hero
        When the engine transitions to priority state with dying hero at zero life
        Then a game state action should fire for the dying hero at zero life

    # Rule 2.5.3f - Non-hero permanent reaching zero life is cleared
    Scenario: Non-hero permanent with zero life total is cleared from arena
        Given an ally permanent named zero ally with a printed life of 3
        And the zero ally is placed in the arena
        And a life loss effect of 3 is applied to the zero ally
        When the engine transitions to priority state with zero ally at zero life
        Then a game state action should fire to clear the zero ally

    # Rule 2.5.3g - Living object ceasing to exist is considered to have died
    Scenario: Living object ceasing to exist is considered dead
        Given a permanent card named ceasing permanent with a printed life of 5
        And the ceasing permanent is in the arena as a living object
        When the ceasing permanent ceases to exist
        Then the ceasing permanent should be considered to have died

    # Rule 2.5.3g - Death distinction (ceasing to exist vs losing life)
    Scenario: Card dying is distinct from card merely losing life
        Given a permanent card named surviving permanent with a printed life of 5
        And the surviving permanent loses 2 life but remains in the arena
        When the engine checks the surviving permanent death status
        Then the surviving permanent should not be considered dead

    # Independence: Multiple objects have independent life totals
    Scenario: Multiple cards maintain independent life totals
        Given a hero card named independent hero A with a printed life of 20
        And a hero card named independent hero B with a printed life of 40
        When a life loss of 5 is applied to independent hero A only
        Then independent hero A life total should be 15
        And independent hero B life total should be 40
