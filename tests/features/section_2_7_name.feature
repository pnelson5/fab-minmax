# Feature file for Section 2.7: Name
# Reference: Flesh and Blood Comprehensive Rules Section 2.7
#
# 2.7.1 Name is a property of an object, which represents one of its object
#        identities and determines the object's uniqueness (along with the pitch
#        property). [1.2.2][1.3.4]
#
# 2.7.2 The printed name of a card is typically located at the top of the card.
#        The printed name defines the name of a card.
#
# 2.7.3 If an object has a name that is a personal name, that name determines
#        the object's moniker - the most significant identifier of the object's
#        name. A personal name is typically written in the format
#        "[HONORIFIC?] [MONIKER] [LAST?] [, SUFFIX?]," where HONORIFIC (if any)
#        is one or more name honorifics, MONIKER is the moniker of the name,
#        LAST (if any) is one or more middle and/or last names, and SUFFIX (if
#        any) is a title or nickname written after a comma.
#
#        Examples of monikers:
#          - Bravo -> moniker: "Bravo"
#          - Dorinthea Ironsong -> moniker: "Dorinthea"
#          - Data Doll MKII -> moniker: "Data Doll"
#          - Ser Boltyn, Breaker of Dawn -> moniker: "Boltyn"
#          - Blasmophet, the Soul Harvester -> moniker: "Blasmophet"
#          - The Librarian -> moniker: "The Librarian"
#          - Dawnblade -> moniker: "Dawnblade"
#          - Stalagmite, Bastion of Isenloft -> moniker: "Stalagmite"
#
# 2.7.3a If an object does not have a name that is a personal name, it does not
#         have a moniker.
#
# 2.7.3b If two objects have different names, they may have the same moniker.
#         An effect that refers to an object using a moniker may refer to two or
#         more objects with different names but the same moniker.
#         Example: "Bravo," "Bravo, Showstopper," and "Bravo, Star of the Show"
#         all have the moniker "Bravo."
#
# 2.7.3c A moniker is not considered a name. If an effect identifies an object
#         by a name, it does not identify objects with a moniker that is the
#         same as that name.
#         Example: If an effect names "Dawnblade," it would NOT match
#         "Dawnblade, Resplendent" even though both have the moniker "Dawnblade."
#
# 2.7.4 An object's printed name is always considered to be the English
#        language version of its name, regardless of the printed language.
#
# 2.7.5 A name or part of a name is equal to another name or part of a name
#        only if it is an exact case-insensitive match of each whole word in
#        order.
#        Example: "Blazing Aether" is NOT matched by "Trailblazing Aether."
#        Example: "Breaker Helm Protos" does NOT match "Proto" because "Protos"
#        is not a whole word match for "Proto."

Feature: Section 2.7 - Name
    As a game engine
    I need to correctly implement the name property rules
    So that card identity, uniqueness, monikers, and name matching are handled correctly

    # Rule 2.7.1 - Name is a property representing object identity
    Scenario: Name is a property of a card object
        Given a card named "Pummel" is created
        When the engine checks the name property of the Pummel card
        Then the Pummel card should have the name property
        And the name of the Pummel card should be "Pummel"
        And the name should be one of the card's object identities

    # Rule 2.7.1 - Name determines uniqueness along with pitch
    Scenario: Name determines card uniqueness along with pitch value
        Given a Sink Below card with pitch value 1 is created
        And a Sink Below card with pitch value 2 is created
        When the engine checks the uniqueness of the two Sink Below cards
        Then the two Sink Below cards should be distinct because they have different pitch values

    # Rule 2.7.1 - Same name and pitch means not distinct
    Scenario: Cards with same name and pitch are not distinct
        Given a Pummel card with pitch value 1 is created as card A
        And a Pummel card with pitch value 1 is created as card B
        When the engine checks the uniqueness of the two Pummel cards
        Then the two Pummel cards should not be distinct because they have the same name and pitch

    # Rule 2.7.2 - Printed name defines the name of a card
    Scenario: Printed name defines the card name
        Given a card with the printed name "Lunging Press" is created
        When the engine retrieves the name of the Lunging Press card
        Then the name of the Lunging Press card should be "Lunging Press"
        And the name should match the printed name exactly

    # Rule 2.7.3 - Personal name determines a moniker
    Scenario: A personal name determines a moniker
        Given a Bravo hero card with personal name is created
        When the engine checks the moniker of the Bravo hero
        Then the moniker of the Bravo hero should be "Bravo"

    # Rule 2.7.3 - Dorinthea Ironsong moniker extraction
    Scenario: Dorinthea Ironsong has moniker Dorinthea
        Given a hero card with the personal name "Dorinthea Ironsong" is created
        When the engine checks the moniker of the Dorinthea Ironsong hero
        Then the moniker of the Dorinthea Ironsong hero should be "Dorinthea"

    # Rule 2.7.3 - Honorific and suffix handling
    Scenario: Name with honorific and suffix extracts the correct moniker
        Given a hero card with the personal name "Ser Boltyn, Breaker of Dawn" is created
        When the engine checks the moniker of the Ser Boltyn hero
        Then the moniker of the Ser Boltyn hero should be "Boltyn"

    # Rule 2.7.3 - Multi-word moniker (The Librarian)
    Scenario: The Librarian has moniker The Librarian
        Given a hero card with the personal name "The Librarian" is created
        When the engine checks the moniker of The Librarian hero
        Then the moniker of The Librarian hero should be "The Librarian"

    # Rule 2.7.3a - Non-personal names have no moniker
    Scenario: A non-personal name has no moniker
        Given a card named "Pummel" that is not a personal name is created
        When the engine checks the moniker of the Pummel card
        Then the Pummel card should have no moniker

    # Rule 2.7.3a - Action card has no moniker
    Scenario: A non-hero action card has no moniker
        Given a card named "Lunging Press" is created as an action card
        When the engine checks the moniker of the Lunging Press action card
        Then the Lunging Press action card should have no moniker

    # Rule 2.7.3b - Different names may have the same moniker
    Scenario: Bravo Showstopper has the same moniker as Bravo
        Given a Bravo hero card is created for moniker comparison
        And a Bravo Showstopper hero card is created for moniker comparison
        When the engine checks the monikers of both Bravo cards
        Then both Bravo cards should have the moniker "Bravo"
        And the two Bravo cards should have different names

    # Rule 2.7.3b - Effect using moniker matches multiple cards
    Scenario: Effect using a moniker matches all cards with that moniker
        Given Bravo card 1 with personal name "Bravo" is created for moniker effect test
        And Bravo card 2 with personal name "Bravo, Showstopper" is created for moniker effect test
        And Bravo card 3 with personal name "Bravo, Star of the Show" is created for moniker effect test
        When an effect refers to objects by the moniker "Bravo"
        Then all three Bravo-moniker cards should be matched by the effect
        And the effect should match 3 objects

    # Rule 2.7.3c - Moniker is not considered a name for name-based effects
    Scenario: Effect naming Dawnblade does not match Dawnblade Resplendent
        Given a card named "Dawnblade" with moniker "Dawnblade" is created
        And a card named "Dawnblade, Resplendent" with moniker "Dawnblade" is created
        When an effect identifies an object by the name "Dawnblade"
        Then the effect should match the card named "Dawnblade"
        But the effect should not match the card named "Dawnblade, Resplendent"

    # Rule 2.7.3c - Moniker match is not a name match
    Scenario: A moniker is not considered a name for identification purposes
        Given a card named "Bravo" with moniker "Bravo" is created
        And a card named "Bravo, Showstopper" with moniker "Bravo" is created
        When an effect identifies an object by the name "Bravo"
        Then the name-based identification should match only the card named "Bravo"
        And the name-based identification should not match "Bravo, Showstopper"

    # Rule 2.7.4 - Printed name is considered the English version
    Scenario: Printed name always considered English version
        Given a card with the English name "Pummel" has a Japanese printed card
        When the engine determines the name of the Japanese Pummel card
        Then the name of the Japanese Pummel card should be "Pummel"
        And the name should be the English version regardless of the printed language

    # Rule 2.7.5 - Name matching requires exact case-insensitive whole word match
    Scenario: Name matching is case-insensitive but requires whole word match
        Given "Blazing Aether" and "Trailblazing Aether" cards are in the game for whole word test
        When an effect searches for cards matching the name "Blazing Aether"
        Then the search should find the card named "Blazing Aether"
        But the search should not find the card named "Trailblazing Aether"

    # Rule 2.7.5 - Case-insensitive matching
    Scenario: Name matching is case-insensitive
        Given a "Blazing Aether" card is in the game for case test
        When an effect searches for cards matching the name "blazing aether"
        Then the search should find the card named "Blazing Aether" using case-insensitive match

    # Rule 2.7.5 - Partial word is not a match
    Scenario: Proto does not match Protos in name matching
        Given a "Breaker Helm Protos" card is in the game for proto test
        When an effect searches for cards with "Proto" in their name
        Then the search should not find the card named "Breaker Helm Protos"
        And the non-match reason should be that "Protos" is not a whole word match for "Proto"

    # Rule 2.7.5 - Exact word match is required
    Scenario: Full word match finds the correct cards
        Given a "Proto Helm" card is in the game for exact match test
        When an effect searches for cards with "Proto" in their name for exact test
        Then the search should find the card named "Proto Helm"
