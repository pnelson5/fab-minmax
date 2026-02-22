# Feature file for Section 1.0: General (Rule Hierarchy)
# Reference: Flesh and Blood Comprehensive Rules Section 1.0
#
# Rule 1.0.1: The rules in this document apply to any game of Flesh and Blood.
#
# Rule 1.0.1a: If an effect directly contradicts a rule contained in this document,
#   the effect supersedes that rule.
#
# Rule 1.0.1b: If a tournament rule contradicts a rule contained in this document
#   or an effect, the tournament rule supersedes that rule or that effect.
#
# NOTE: Section 1.0.2 (Restrictions/Requirements/Allowances) is covered separately
# in section_1_0_2_precedence.feature

Feature: Section 1.0 - General Rule Hierarchy
    As a game engine
    I need to correctly implement the rule hierarchy
    So that rules, effects, and tournament rules are applied in the correct order

    # Test for Rule 1.0.1 - Comprehensive rules apply to any game
    Scenario: Comprehensive rules apply to all games of Flesh and Blood
        Given a game of Flesh and Blood is in progress
        When the comprehensive rules are consulted
        Then the rules should govern the game

    # Test for Rule 1.0.1 - Comprehensive rules establish default behavior
    Scenario: Comprehensive rules define default game behavior
        Given a game of Flesh and Blood is in progress
        And no card effects are active
        When a game action is evaluated
        Then the comprehensive rules determine whether the action is legal

    # Test for Rule 1.0.1a - Effect supersedes rule
    Scenario: Card effect supersedes a comprehensive rule
        Given a comprehensive rule states an action is not normally allowed
        And a card effect directly contradicts that rule by allowing the action
        When the action is attempted
        Then the card effect takes precedence over the comprehensive rule
        And the action is permitted

    # Test for Rule 1.0.1a - Effect supersedes rule preventing an action
    Scenario: Card effect can override a default restriction from the rules
        Given a player has a card with an effect "you may play this from your graveyard"
        And the default rules state cards cannot be played from the graveyard
        When the player attempts to play the card from the graveyard
        Then the card effect supersedes the default rule
        And the play attempt is permitted by the effect

    # Test for Rule 1.0.1a - Higher hierarchy still wins over contradicting effect
    Scenario: Effect supersedes rule but tournament rule supersedes effect
        Given a card effect grants an allowance
        And a tournament rule prohibits that action
        When the action is attempted
        Then the tournament rule takes precedence over both the card effect and rule

    # Test for Rule 1.0.1b - Tournament rule supersedes comprehensive rule
    Scenario: Tournament rule supersedes comprehensive rule
        Given a comprehensive rule permits a certain action
        And a tournament rule prohibits that action
        When the action is attempted
        Then the tournament rule takes precedence
        And the action is prohibited

    # Test for Rule 1.0.1b - Tournament rule supersedes card effect
    Scenario: Tournament rule supersedes card effect
        Given a card effect permits a certain action
        And a tournament rule prohibits that action
        When the action is attempted under tournament conditions
        Then the tournament rule takes precedence over the card effect
        And the action is prohibited

    # Test for Rule 1.0.1 - Rules hierarchy ordering
    Scenario: Rule hierarchy has correct priority ordering
        Given the game engine has a rule hierarchy
        When the hierarchy levels are examined
        Then tournament rules should have the highest priority
        And card effects should have the second highest priority
        And comprehensive rules should have the base priority
