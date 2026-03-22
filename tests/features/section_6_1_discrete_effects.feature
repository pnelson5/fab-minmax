# Feature file for Section 6.1: Discrete Effects
# Reference: Flesh and Blood Comprehensive Rules Section 6.1
#
# Rule 6.1.1: A discrete effect is an effect that changes the game state by producing
# an event. Discrete effects have no duration, and after the completion of their event,
# they have no further influence to the game state.
#
# Rule 6.1.2: Discrete effects are atomic. If two or more discrete effects would be
# generated, they are generated and produce their event one at a time.
#
# Example (6.1.2): Sand Sketched Plan has the text "Search your deck for a card, put it
# into your hand, discard a random card, then shuffle your deck," which is a resolution
# ability that generates four atomic discrete effects: search, put, discard, and shuffle.
# Each effect is generated and produces an event before the next one in order is generated.
#
# Rule 6.1.3: If a discrete effect is conditional, its condition is evaluated only once,
# at the time the effect would be generated. If the condition is met, the effect is
# generated - otherwise, it is not.

Feature: Section 6.1 - Discrete Effects
    As a game engine
    I need to correctly implement discrete effects
    So that game state changes are properly atomic and conditionally generated

    # ===== Rule 6.1.1: Discrete effects produce an event and have no duration =====

    # Test for Rule 6.1.1 - Discrete effect changes game state via an event
    Scenario: A discrete effect changes game state by producing an event
        Given a game is in progress
        And a player has a card that generates a discrete draw effect
        When the discrete draw effect is generated
        Then the game state changes as a result of the event
        And the player has drawn a card

    # Test for Rule 6.1.1 - Discrete effect has no lasting duration
    Scenario: A discrete effect has no duration after its event completes
        Given a game is in progress
        And a discrete effect has been generated and produced its event
        When the event from the discrete effect completes
        Then the discrete effect has no further influence on the game state
        And the effect is not tracked as an ongoing modifier

    # Test for Rule 6.1.1 - Discrete effect is not a continuous modifier
    Scenario: A discrete effect does not continuously modify objects or rules
        Given a game is in progress
        And a card generates a discrete deal damage effect
        When the discrete damage effect is generated and produces its event
        Then damage is dealt as a one-time event
        And no ongoing continuous modifier is left in the game state

    # ===== Rule 6.1.2: Discrete effects are atomic and sequential =====

    # Test for Rule 6.1.2 - Multiple discrete effects are generated one at a time
    Scenario: Multiple discrete effects from one ability are generated sequentially
        Given a game is in progress
        And a resolution ability generates multiple discrete effects in sequence
        When the ability resolves
        Then each discrete effect is generated and produces its event one at a time
        And the effects are processed in the order they were declared

    # Test for Rule 6.1.2 - Each discrete effect completes before the next is generated
    Scenario: Each discrete effect completes before the next is generated
        Given a game is in progress
        And a resolution ability generates a sequence of discrete effects
        When the first discrete effect is generated
        Then the first effect completes its event before the second effect is generated
        And the second discrete effect is generated only after the first event completes

    # Test for Rule 6.1.2 - Sand Sketched Plan style: search then put then discard then shuffle
    Scenario: A search-put-discard-shuffle sequence produces four sequential atomic events
        Given a player has a card that generates search, put, discard, and shuffle discrete effects
        When the card resolves on the stack
        Then a search event occurs first
        And after the search event a put event occurs
        And after the put event a discard event occurs
        And after the discard event a shuffle event occurs
        And each event is completed before the next begins

    # ===== Rule 6.1.3: Conditional discrete effects evaluate condition once at generation time =====

    # Test for Rule 6.1.3 - Condition evaluated at generation time, if met effect is generated
    Scenario: A conditional discrete effect is generated when its condition is met at generation time
        Given a game is in progress
        And the game state satisfies the condition for a conditional discrete effect
        When the conditional discrete effect would be generated
        Then the condition is evaluated once at the time the effect would be generated
        And since the condition is met the effect is generated
        And the effect produces its event

    # Test for Rule 6.1.3 - Condition not met, effect is not generated
    Scenario: A conditional discrete effect is not generated when its condition is not met at generation time
        Given a game is in progress
        And the game state does not satisfy the condition for a conditional discrete effect
        When the conditional discrete effect would be generated
        Then the condition is evaluated once at the time the effect would be generated
        And since the condition is not met the effect is not generated
        And no event is produced for that effect

    # Test for Rule 6.1.3 - Condition evaluated only once even if state changes after
    Scenario: A conditional discrete effect condition is evaluated only once at generation time
        Given a game is in progress
        And the game state satisfies the condition for a conditional discrete effect at generation time
        When the condition is evaluated and the effect is generated
        And the game state changes so that the condition would no longer be met
        Then the effect still produces its event because the condition was already evaluated as met
        And the condition is not re-evaluated after the effect has been generated

    # Test for Rule 6.1.3 - Condition not met means no event occurs
    Scenario: A conditional discrete effect that is not generated produces no event
        Given a game is in progress
        And a card has a conditional discrete effect requiring a specific board state
        And the required board state is absent
        When the conditional discrete effect would be generated
        Then the condition is evaluated as not met
        And the effect is skipped entirely with no event occurring
        And the game state is unchanged by that conditional effect
