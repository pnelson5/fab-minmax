# Feature file for Section 2.12: Text Box
# Reference: Flesh and Blood Comprehensive Rules Section 2.12
#
# 2.12.1 The text box of a card contains the card text of a card, typically
#         located on the lower half of a card beneath the illustration.
#
# 2.12.2 The card text of a card contains the rules text, reminder text, and
#         flavor text of the card (if any). Rules text is printed in roman and
#         boldface. Reminder text is printed in parenthesized italics. Flavor
#         text is separated vertically from the rules and reminder text (if any)
#         by a horizontal bar and is printed in italics.
#
# 2.12.3 The rules text of a card defines the base abilities of the card. A
#         paragraph of rules text typically defines a single ability. Reminder
#         and flavor text do not affect the game.
#
# 2.12.3a If the rules text specifies the name and/or moniker of its source
#          object in the third-person it is a self-reference. A self-reference
#          can be interpreted as "this" and it refers to its source object and
#          not other cards with the same name.
#
# 2.12.3b If the rules text specifies the name and/or moniker of another object
#          in the context of creating it, it refers to a hypothetical object with
#          defined properties, including that name. Otherwise, if the rules text
#          specifies the name and/or moniker of another object it refers to any
#          existing object with that name and/or moniker.

Feature: Section 2.12 - Text Box
    As a game engine
    I need to correctly implement the text box rules
    So that card abilities, self-references, and name references resolve correctly

    # Test for Rule 2.12.1 - Text box contains card text
    Scenario: Card has a text box containing card text
        Given a card with text box rules text "Go again."
        When the engine reads the text box card text
        Then the card has a text box
        And the text box contains card text

    # Test for Rule 2.12.1 - Card without rules text has empty card text
    Scenario: Card without rules text has an empty text box
        Given a card with no text box rules text
        When the engine reads the empty text box
        Then the card text is empty or absent

    # Test for Rule 2.12.2 - Card text includes rules text component
    Scenario: Card text includes rules text component
        Given a card with only rules text "Go again."
        When the engine reads the rules text component
        Then the rules text is "Go again."

    # Test for Rule 2.12.2 - Card text contains reminder text in parenthesized italics
    Scenario: Card text can include reminder text
        Given a card with rules text and reminder text "(If you play this card before your action phase ends, you may play another card.)"
        When the engine reads the reminder text component
        Then the card has reminder text "(If you play this card before your action phase ends, you may play another card.)"

    # Test for Rule 2.12.2 - Card text contains flavor text
    Scenario: Card text can include flavor text
        Given a card with rules text and flavor text "The true warrior never tires."
        When the engine reads the flavor text component
        Then the card has flavor text "The true warrior never tires."

    # Test for Rule 2.12.2 - Card text without reminder text
    Scenario: Card text may have no reminder text
        Given a card with only rules text and no reminder text
        When the engine reads the reminder text field
        Then the card has no reminder text

    # Test for Rule 2.12.2 - Card text without flavor text
    Scenario: Card text may have no flavor text
        Given a card with only rules text and no flavor text
        When the engine reads the flavor text field
        Then the card has no flavor text

    # Test for Rule 2.12.3 - Rules text defines base abilities
    Scenario: Rules text defines the base abilities of a card
        Given a card whose rules text is "Go again."
        When the engine evaluates the rules text for base abilities
        Then the card has base ability "go again"

    # Test for Rule 2.12.3 - A paragraph of rules text defines a single ability
    Scenario: Each paragraph of rules text defines a single ability
        Given a card with two ability paragraphs "Go again." and "Draw a card."
        When the engine counts abilities from rules text paragraphs
        Then the card has 2 base abilities

    # Test for Rule 2.12.3 - Reminder text does not affect the game
    Scenario: Reminder text does not contribute to base abilities
        Given a card with go again rules text and a reminder text paragraph
        When the engine evaluates abilities excluding reminder text
        Then the reminder text does not add any abilities to the card

    # Test for Rule 2.12.3 - Flavor text does not affect the game
    Scenario: Flavor text does not contribute to base abilities
        Given a card with go again rules text and a flavor text paragraph
        When the engine evaluates abilities excluding flavor text
        Then the flavor text does not add any abilities to the card

    # Test for Rule 2.12.3a - Self-reference means "this" object
    Scenario: Card name in rules text is a self-reference
        Given a card named "Pummel" with self-referencing rules text
        When the engine resolves the name reference "Pummel" in the rules text
        Then the reference resolves to the card itself
        And it does not refer to any other card with the same name

    # Test for Rule 2.12.3a - Self-reference via moniker
    Scenario: Card moniker in rules text is a self-reference
        Given a hero card named "Bravo, Showstopper" with moniker self-referencing rules text
        When the engine resolves the moniker reference "Bravo" in the rules text
        Then the reference resolves to the hero card itself

    # Test for Rule 2.12.3a - Self-reference does not match other same-named cards
    Scenario: Self-reference does not match other same-named card instances
        Given a primary Pummel card with self-referencing rules text
        And another separate Pummel card instance in play
        When the engine resolves the Pummel self-reference in the first card's context
        Then the reference refers only to the first card, not the second

    # Test for Rule 2.12.3b - Reference to named object being created is a hypothetical
    Scenario: Creating a named token refers to a hypothetical object
        Given a card whose rules text creates a Runechant token
        When the engine checks whether the Runechant reference is a creation context
        Then the "Runechant" reference is to a hypothetical object being created
        And the hypothetical object has the name "Runechant"

    # Test for Rule 2.12.3b - Reference to an existing named object
    Scenario: Reference to named object not being created refers to existing objects
        Given a card whose rules text destroys a target Runechant
        And a Runechant token currently in the arena
        When the engine checks whether the Runechant reference is a non-creation context
        Then the "Runechant" reference refers to the existing Runechant token in play

    # Test for Rule 2.12.3b - Creating named object with defined properties
    Scenario: Hypothetical named object has properties defined by creating instruction
        Given a card whose rules text creates a Runechant token with go again
        When the engine constructs the hypothetical Runechant object
        Then the hypothetical Runechant has property "go again"
        And the hypothetical Runechant has name "Runechant"
