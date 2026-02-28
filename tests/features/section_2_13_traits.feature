# Feature file for Section 2.13: Traits
# Reference: Flesh and Blood Comprehensive Rules Section 2.13
#
# 2.13.1 Trait is a property of an object, which represents one of its
#         object identities. [1.2.2]
#
# 2.13.2 The printed traits of a card are typically located at the top of
#         the card, under the card name. The printed traits define the traits
#         of a card.
#
# 2.13.3 Traits are non-functional keywords or phrases and do not add
#         additional rules to an object.
#
# 2.13.3a The trait keywords and phrases are Agents of Chaos.
#
# 2.13.4 If an effect refers to a group of cards by a trait, it refers to
#         all cards with that trait.
#
#         Example: Arakni, Web of Deceit has the text "At the beginning of
#         your end phase, if an opponent is marked, you become a random
#         Agent of Chaos." This refers to a group which includes all cards
#         with the Agent of Chaos trait, and selecting one at random from
#         that group.

Feature: Section 2.13 - Traits
    As a game engine
    I need to correctly implement the traits property rules
    So that trait-based object identities and effect groupings resolve correctly

    # Test for Rule 2.13.1 - Trait is a property that represents an object identity
    Scenario: Trait is a property of an object representing its identity
        Given a card with the trait "Agents of Chaos"
        When the engine reads the card's traits
        Then the card has the trait "Agents of Chaos"
        And "Agents of Chaos" is an object identity of the card

    # Test for Rule 2.13.1 - Trait is recognized as a property
    Scenario: Trait is recognized as an object property
        Given a card with the trait "Agents of Chaos"
        When the engine reads the card's properties
        Then the card has a traits property
        And the traits property contains "Agents of Chaos"

    # Test for Rule 2.13.1 - Cross-reference with Rule 1.2.2 (object identities)
    Scenario: Card without a trait has no trait object identity
        Given a card with no printed traits
        When the engine reads the card's traits
        Then the card has zero traits
        And no trait appears in the card's object identities

    # Test for Rule 2.13.2 - Printed traits define the traits of a card
    Scenario: Printed traits define the card traits
        Given a card whose printed traits include "Agents of Chaos"
        When the engine reads the printed traits
        Then the base traits of the card include "Agents of Chaos"

    # Test for Rule 2.13.2 - Traits are located at the top of the card under the card name
    Scenario: Card can have exactly one printed trait
        Given a card with exactly one printed trait "Agents of Chaos"
        When the engine counts the card's traits
        Then the card has exactly 1 trait

    # Test for Rule 2.13.2 - A card can have zero traits
    Scenario: Card can have zero traits
        Given a card with no printed traits
        When the engine counts the card's traits
        Then the card has exactly 0 traits

    # Test for Rule 2.13.3 - Traits are non-functional keywords
    Scenario: Traits are non-functional and do not add additional rules
        Given a card with the trait "Agents of Chaos"
        When the engine evaluates whether traits add additional rules
        Then the trait "Agents of Chaos" is non-functional
        And the trait does not add additional rules to the card

    # Test for Rule 2.13.3 - Non-functional trait does not affect gameplay
    Scenario: Non-functional trait has no gameplay effect on its own
        Given a card with no traits
        And a card with the trait "Agents of Chaos"
        When both cards are evaluated for additional rules added by traits
        Then neither card gains additional rules from traits

    # Test for Rule 2.13.3a - The only defined trait keyword is Agents of Chaos
    Scenario: Agents of Chaos is a recognized trait keyword
        Given the trait keyword "Agents of Chaos"
        When the engine checks the recognized trait keywords
        Then "Agents of Chaos" is a valid trait keyword
        And the total number of defined trait keywords is 1

    # Test for Rule 2.13.4 - Effect refers to group of cards by trait
    Scenario: Effect using a trait refers to all cards with that trait
        Given a group of cards in the arena
        And one card has the trait "Agents of Chaos"
        And another card does not have the trait "Agents of Chaos"
        When an effect targets "all cards with the Agents of Chaos trait"
        Then only the card with the trait "Agents of Chaos" is in the target group
        And the card without the trait is not in the target group

    # Test for Rule 2.13.4 - Arakni, Web of Deceit example: random selection from group
    Scenario: Effect selects a random card from the Agents of Chaos group
        Given multiple cards each with the trait "Agents of Chaos"
        When an effect selects a random "Agent of Chaos" card from the group
        Then the selected card has the trait "Agents of Chaos"
        And the selected card is one of the cards in the Agents of Chaos group

    # Test for Rule 2.13.4 - Empty group when no cards have the trait
    Scenario: Effect targets empty group when no cards have the trait
        Given a group of cards in the arena with no Agents of Chaos trait
        When an effect targets "all cards with the Agents of Chaos trait"
        Then the target group is empty

    # Test for Rule 2.13.1 cross-ref Rule 1.2.2b - Trait as identity
    Scenario: Trait contributes to object identity alongside name
        Given a card named "Test Agent" with the trait "Agents of Chaos"
        When the engine retrieves all object identities of the card
        Then the object identities include "Agents of Chaos"
        And the object identities also include "Test Agent"

    # Test for Rule 2.13.2 - Multiple copies with same trait are all in trait group
    Scenario: Multiple card instances with same trait all belong to the trait group
        Given three cards each with the trait "Agents of Chaos"
        When an effect targets all cards with the trait "Agents of Chaos"
        Then all three cards are in the target group
