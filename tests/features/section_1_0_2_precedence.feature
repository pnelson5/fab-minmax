# Feature file for Section 1.0.2: Restriction, Requirement, and Allowance Precedence
# Reference: Flesh and Blood Comprehensive Rules Section 1.0.2
#
# Rule 1.0.2: A restriction is a rule or effect that states something cannot happen. 
# A requirement is a rule or effect that states that something should happen if possible. 
# An allowance is a rule or effect that states something can happen. 
# A restriction takes precedence over any requirement or allowance, and a requirement 
# takes precedence over any allowance, subject to [1.0.1a].

Feature: Section 1.0.2 - Restriction, Requirement, and Allowance Precedence
    As a game engine
    I need to correctly apply precedence rules between restrictions, requirements, and allowances
    So that game effects resolve in the proper order according to the comprehensive rules

    # Test for Rule 1.0.2 - Restriction takes precedence over Allowance
    Scenario: Restriction overrides allowance for playing cards from banished zone
        Given a player has a restriction effect "You can't play cards from your banished zone"
        And the player has an allowance effect "You may play cards from your banished zone"
        And the player has a card in their banished zone
        When the player attempts to play a card from their banished zone
        Then the play should be prevented
        And the card should remain in the banished zone

    # Test for Rule 1.0.2 - Restriction takes precedence over Requirement
    Scenario: Restriction overrides requirement for defending with equipment
        Given an attack has the restriction "This can't be defended by equipment"
        And a defender has a requirement "You must defend with equipment if able"
        And the defender controls equipment that could defend
        When the defender attempts to defend with equipment
        Then the defense should be prevented
        And the equipment should not be used to defend

    # Test for Rule 1.0.2 - Requirement takes precedence over Allowance
    Scenario: Requirement overrides allowance for card selection
        Given a player has a requirement "You must play your next card from hand if able"
        And the player has an allowance "You may play your next card from arsenal"
        And the player has playable cards in hand
        And the player has a playable card in arsenal
        When the player attempts to play a card
        Then the player must play from hand
        And the player cannot choose to play from arsenal

    # Test for Rule 1.0.2a - "Only" restriction is equivalent to restricting everything else
    Scenario: "Only" restriction functions as restriction on all other options
        Given a player has a restriction "You may only play cards from arsenal"
        And the player has a card in hand
        And the player has a card in arsenal
        When the player attempts to play the card from hand
        Then the play should be prevented
        And only arsenal cards should be playable

    # Test for Rule 1.0.2b - Restrictions do not retroactively change game state
    Scenario: Overpower gained after defenders declared does not remove existing defenders
        Given an attack is being defended by 2 action cards
        And the attack gains overpower (can't be defended by more than 1 action card)
        When the overpower effect is applied
        Then both defending action cards remain defending
        And the game state is not retroactively changed

    # Test for Rule 1.0.2 with multiple restrictions
    Scenario: Multiple restrictions all apply simultaneously
        Given a player has a restriction "You can't play red cards"
        And the player has a restriction "You can't play cards with cost 3 or greater"
        And the player has a red card with cost 1 in hand
        And the player has a blue card with cost 3 in hand
        When the player attempts to play either card
        Then both cards should be unplayable
        And all restrictions should be enforced

    # Test for Rule 1.0.2 - Allowance alone permits action
    Scenario: Allowance permits action when no restriction or requirement exists
        Given a player has an allowance "You may play this card from your banished zone"
        And the player has no restriction effects active
        And the player has no requirement effects active
        And the player has the card in their banished zone
        When the player plays the card from their banished zone
        Then the play should succeed
        And the card should move to the appropriate zone
