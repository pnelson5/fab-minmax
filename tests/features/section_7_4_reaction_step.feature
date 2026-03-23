# Feature file for Section 7.4: Reaction Step
# Reference: Flesh and Blood Comprehensive Rules Section 7.4
#
# Rule 7.4.1: The Reaction Step is a game state where players may use
#   reactions related to combat.
#
# Rule 7.4.2: First, the turn-player gains priority.
#
#   Rule 7.4.2a: The player that controls the attack may play/activate attack
#     reaction cards/abilities when they have priority during the Reaction Step.
#
#   Rule 7.4.2b: A player that controls a hero as an attack-target (if any)
#     may play/activate defense reaction cards/abilities when they have priority
#     during the Reaction Step.
#
#   Rule 7.4.2c: A defense reaction card cannot be played if a rule or effect
#     would prevent the player from defending with that card.
#
#     > If an attack has dominate (can't be defended by more than 1 card from
#       hand) and is already defended by a card from hand, defence reaction
#       cards cannot be played from hand because dominate prevents it from
#       becoming a defending card.
#
#   Rule 7.4.2d: When a defense reaction card resolves it becomes a defending
#     card on the active chain link for its controller's hero. A defense
#     reaction card fails to resolve if it cannot become a defending card.
#
#     > If an attack has dominate and there are two defense reactions on the
#       stack, the first one will resolve and become a defending card, but the
#       second one will fail to resolve because dominate prevents it from
#       becoming a defending card.
#
# Rule 7.4.3: Second and finally, when the stack is empty and all players pass
#   in succession, the Reaction Step ends and the Damage Step begins.

Feature: Section 7.4 - Reaction Step
    As a game engine
    I need to correctly implement the Reaction Step of combat
    So that attack and defense reactions can be played and resolved correctly

    # -----------------------------------------------------------------------
    # Rule 7.4.1 — Reaction Step is a distinct game state
    # -----------------------------------------------------------------------

    Scenario: Reaction Step is a game state where reactions may be used
        Given the Defend Step has completed
        When the Reaction Step begins
        Then the current combat step is "reaction"
        And it is valid for players to use combat reactions

    Scenario: Reaction Step begins after the Defend Step ends
        Given a combat chain is active with an attack on the chain link
        And the Defend Step has ended
        When the game advances
        Then the Reaction Step begins

    # -----------------------------------------------------------------------
    # Rule 7.4.2 — Turn-player gains priority first
    # -----------------------------------------------------------------------

    Scenario: Turn-player gains priority first in the Reaction Step
        Given the Reaction Step begins
        When priority is granted at the start of the Reaction Step
        Then the turn-player has priority

    # -----------------------------------------------------------------------
    # Rule 7.4.2a — Attack controller may play attack reactions
    # -----------------------------------------------------------------------

    Scenario: Attack controller may play attack reaction cards during Reaction Step
        Given the Reaction Step is active
        And player A controls the attack
        And player A has an attack reaction card in hand
        When player A attempts to play the attack reaction card
        Then the play is legal

    Scenario: Attack controller may activate attack reaction abilities during Reaction Step
        Given the Reaction Step is active
        And player A controls the attack
        And player A controls a permanent with an attack reaction activated ability
        When player A attempts to activate the attack reaction ability
        Then the activation is legal

    Scenario: Non-attack-controller cannot play attack reaction cards
        Given the Reaction Step is active
        And player A controls the attack
        And player B does not control the attack
        And player B has an attack reaction card in hand
        When player B attempts to play the attack reaction card
        Then the play is illegal

    Scenario: Attack reaction cards cannot be played outside the Reaction Step
        Given the Defend Step is active
        And player A controls the attack
        And player A has an attack reaction card in hand
        When player A attempts to play the attack reaction card
        Then the play is illegal

    # -----------------------------------------------------------------------
    # Rule 7.4.2b — Defending hero controller may play defense reactions
    # -----------------------------------------------------------------------

    Scenario: Defending hero controller may play defense reaction cards during Reaction Step
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And player B has a defense reaction card in hand
        When player B attempts to play the defense reaction card
        Then the play is legal

    Scenario: Defending hero controller may activate defense reaction abilities during Reaction Step
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And player B controls a permanent with a defense reaction activated ability
        When player B attempts to activate the defense reaction ability
        Then the activation is legal

    Scenario: Player without hero as attack-target cannot play defense reaction cards
        Given the Reaction Step is active
        And player B does not control a hero that is an attack-target
        And player B has a defense reaction card in hand
        When player B attempts to play the defense reaction card
        Then the play is illegal

    # -----------------------------------------------------------------------
    # Rule 7.4.2c — Defense reaction blocked by defend restriction
    # -----------------------------------------------------------------------

    Scenario: Defense reaction cannot be played if a rule prevents defending with it
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And the active attack has dominate
        And the hero is already defended by a card from hand
        And player B has a defense reaction card in hand
        When player B attempts to play the defense reaction card from hand
        Then the play is illegal
        And the reason is "dominate prevents defending with an additional card from hand"

    Scenario: Defense reaction can be played when no defend restriction applies
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And the active attack does not have dominate
        And player B has a defense reaction card in hand
        When player B attempts to play the defense reaction card from hand
        Then the play is legal

    Scenario: Defense reaction can be played when dominate is present but no card from hand defends yet
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And the active attack has dominate
        And no cards from hand are defending yet
        And player B has a defense reaction card in hand
        When player B attempts to play the defense reaction card from hand
        Then the play is legal

    # -----------------------------------------------------------------------
    # Rule 7.4.2d — Defense reaction resolves as a defending card
    # -----------------------------------------------------------------------

    Scenario: Defense reaction card becomes a defending card when it resolves
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And a defense reaction card is on the stack
        When the defense reaction card resolves
        Then the defense reaction card becomes a defending card on the active chain link
        And the defending card is associated with player B's hero

    Scenario: Defense reaction card fails to resolve if it cannot become a defending card
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And the active attack has dominate
        And a defending card from hand is already on the chain link
        And a defense reaction card is on the stack
        When the defense reaction card resolves
        Then the defense reaction card fails to resolve
        And the defense reaction card does not become a defending card

    Scenario: Second defense reaction fails when dominate already satisfied by first
        Given the Reaction Step is active
        And player B controls a hero that is an attack-target
        And the active attack has dominate
        And two defense reaction cards are on the stack
        When the first defense reaction card resolves
        Then the first defense reaction card becomes a defending card on the active chain link
        When the second defense reaction card resolves
        Then the second defense reaction card fails to resolve
        And the second defense reaction card does not become a defending card

    # -----------------------------------------------------------------------
    # Rule 7.4.3 — Reaction Step ends, Damage Step begins
    # -----------------------------------------------------------------------

    Scenario: Reaction Step ends and Damage Step begins when stack is empty and all players pass
        Given the Reaction Step is active
        And the stack is empty
        When all players pass priority in succession
        Then the Reaction Step ends
        And the Damage Step begins

    Scenario: Reaction Step does not end while there are items on the stack
        Given the Reaction Step is active
        And a reaction card is on the stack
        When all players pass priority
        Then the Reaction Step has not ended

    Scenario: Reaction Step does not end if not all players have passed
        Given the Reaction Step is active
        And the stack is empty
        When only the turn-player passes priority
        Then the Reaction Step has not ended
