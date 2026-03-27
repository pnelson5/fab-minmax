# Feature file for Section 8.3.34: Guardwell (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.34
#
# Rule 8.3.34: Guardwell is a static ability that means "When the combat chain
# closes, if this defended, put -1{d} counters on it equal to its {d}."
#
# Key aspects of Guardwell:
# - It is a STATIC ability (always active while card is in play)
# - Triggers when the combat chain closes
# - Condition: the Guardwell card must have defended in that chain
# - Effect: put -1{d} counters equal to the card's current {d} value
# - A card that did NOT defend receives no counters
# - A card with 0 defense gets 0 counters (no effect)
# - Each combat chain close is a separate trigger event

Feature: Section 8.3.34 - Guardwell Ability Keyword
    As a game engine
    I need to correctly implement the Guardwell ability keyword
    So that equipment that defends loses defense value equal to the damage it blocked

    # Rule 8.3.34: Guardwell is recognized as a keyword
    Scenario: Guardwell is recognized as an ability keyword
        Given a card with the Guardwell keyword
        When I inspect the card's keywords
        Then the card has the Guardwell keyword

    # Rule 8.3.34: Guardwell is a static ability
    Scenario: Guardwell is a static ability
        Given a card with the Guardwell keyword
        When I check the ability type of Guardwell
        Then Guardwell is a static ability

    # Rule 8.3.34: Guardwell ability meaning matches comprehensive rules text
    Scenario: Guardwell ability meaning matches comprehensive rules text
        Given a card with the Guardwell keyword
        When I inspect the Guardwell ability's meaning
        Then the Guardwell meaning is "When the combat chain closes, if this defended, put -1{d} counters on it equal to its {d}"

    # Rule 8.3.34: Card with Guardwell gets -1{d} counters when it defended
    Scenario: Card with Guardwell gets minus defense counters when it defended
        Given a card with the Guardwell keyword and 3 defense
        And the card is in play as equipment
        When the card defends in a combat chain
        And the combat chain closes
        Then the card has 3 minus-defense counters on it

    # Rule 8.3.34: Number of counters equals current defense value
    Scenario: Number of minus-defense counters equals the card's defense value
        Given a card with the Guardwell keyword and 2 defense
        And the card is in play as equipment
        When the card defends in a combat chain
        And the combat chain closes
        Then the card has 2 minus-defense counters on it

    # Rule 8.3.34: Card with Guardwell gets NO counters if it did not defend
    Scenario: Card with Guardwell gets no counters if it did not defend
        Given a card with the Guardwell keyword and 3 defense
        And the card is in play as equipment
        When the combat chain closes without the card defending
        Then the card has 0 minus-defense counters on it

    # Rule 8.3.34: Card with 0 defense gets 0 counters
    Scenario: Card with Guardwell and zero defense gets no counters when it defended
        Given a card with the Guardwell keyword and 0 defense
        And the card is in play as equipment
        When the card defends in a combat chain
        And the combat chain closes
        Then the card has 0 minus-defense counters on it

    # Rule 8.3.34: Guardwell triggers on each combat chain close
    Scenario: Guardwell triggers on each separate combat chain close
        Given a card with the Guardwell keyword and 4 defense
        And the card is in play as equipment
        When the card defends in the first combat chain
        And the first combat chain closes
        Then the card has 4 minus-defense counters on it
        When the card defends in a second combat chain
        And the second combat chain closes
        Then the card has 8 minus-defense counters on it

    # Rule 8.3.34: Guardwell is classified as a static ability (not triggered)
    Scenario: Guardwell is not classified as a triggered ability
        Given a card with the Guardwell keyword
        When I check if Guardwell is a triggered ability
        Then Guardwell is not a triggered ability
