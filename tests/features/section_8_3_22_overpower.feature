# Feature file for Section 8.3.22: Overpower (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.22
#
# Rule 8.3.22: Overpower is a static ability that means "This can't be
# defended by more than one action card."
#
# Rule 8.3.22a: If an attack with overpower is currently defended by an action
# card, an additional action card cannot be added as a defending card to the
# attack's chain link. [8.5.32]
#
# Rule 8.3.22b: If an attack is defended by two or more action cards and then
# the attack gains overpower, no cards are retroactively removed from defending.

Feature: Section 8.3.22 - Overpower Ability Keyword
    As a game engine
    I need to correctly implement the Overpower ability keyword
    So that attacks with Overpower cannot be defended by more than one action card

    # Rule 8.3.22: Overpower is a static ability
    Scenario: Overpower is a static ability
        Given a card with Overpower ability
        When I inspect the Overpower ability
        Then the Overpower ability is a static ability

    # Rule 8.3.22: Overpower means "This can't be defended by more than one action card"
    Scenario: Overpower ability has correct meaning
        Given a card with Overpower ability
        When I inspect the Overpower ability
        Then the Overpower meaning is "This can't be defended by more than one action card"

    # Rule 8.3.22a: First action card defender is allowed
    Scenario: First action card can defend an Overpower attack
        Given an attack with Overpower
        And the defending player has an action card in hand
        When the defending player defends with the action card
        Then the defense is successful

    # Rule 8.3.22a: Second action card defender is blocked
    Scenario: Second action card cannot defend an Overpower attack
        Given an attack with Overpower
        And the attack is already defended by one action card
        And the defending player has another action card
        When the defending player tries to add a second action card as defender
        Then the defense is blocked
        And the block reason is "overpower restriction"

    # Rule 8.3.22a: Equipment can still defend alongside an action card
    Scenario: Equipment can defend an Overpower attack alongside one action card
        Given an attack with Overpower
        And the attack is already defended by one action card
        And the defending player has an equipment card
        When the defending player defends with the equipment card
        Then the defense is successful

    # Rule 8.3.22a: Equipment is not blocked by Overpower (only action cards are counted)
    Scenario: Multiple equipment cards can defend an Overpower attack
        Given an attack with Overpower
        And the defending player has two equipment cards
        When the defending player defends with both equipment cards
        Then the defense is successful

    # Rule 8.3.22b: No retroactive removal when Overpower is gained
    Scenario: Gaining Overpower does not remove existing action card defenders
        Given an attack without Overpower
        And the attack is defended by two action cards
        When the attack gains Overpower
        Then both action cards remain as defenders
        And the number of defenders is 2

    # Rule 8.3.22b: After gaining Overpower, a third action card is still blocked
    Scenario: After gaining Overpower additional action card defenders are blocked
        Given an attack without Overpower
        And the attack is defended by two action cards
        When the attack gains Overpower
        And the defending player tries to add a third action card as defender
        Then the defense is blocked

    # Rule 8.3.22a: No defenders yet - first action card is allowed
    Scenario: Overpower attack with no defenders allows first action card
        Given an attack with Overpower
        And the attack has no defenders yet
        And the defending player has an action card in hand
        When the defending player defends with the action card
        Then the defense is successful
        And the number of defenders is 1
