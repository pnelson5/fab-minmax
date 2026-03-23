# Feature file for Section 7.3: Defend Step
# Reference: Flesh and Blood Comprehensive Rules Section 7.3
#
# Rule 7.3.1: The Defend Step is a game state where defending cards may be
#   declared by a defending hero.
#
# Rule 7.3.2: First, defending cards are declared for the attack-target(s).
#   Cards declared this way become defending cards for the attack-target(s)
#   on the active chain link. Declaring a card this way is not considered
#   playing that card — it does not incur the cost of playing that card,
#   it does not add it as a layer on the stack, and it does not resolve
#   any resolution abilities on that card.
#
#   Rule 7.3.2a: If the attack-target is a hero (defending hero), their
#     controller may declare any number of non-defense-reaction cards from
#     their hand and/or public equipment permanents they control. Otherwise,
#     a player may only declare cards for an attack-target if a rule or
#     effect specifies it.
#
#   Rule 7.3.2b: A card cannot be declared if (A) it does not have the
#     defense property (0 is a value), (B) it is already a defending card
#     on a chain link, or (C) it would make the current set of declared
#     cards illegal to become defending.
#
#   Rule 7.3.2c: If a player declares two or more defending cards for an
#     attack-target, they decide the order those cards are declared and
#     become defending.
#
#   Rule 7.3.2d: All declared cards for an attack-target are put onto the
#     active chain link as a single compound event as defending cards for
#     that attack-target. The order in which the declared cards become
#     defending within the compound event is determined by the order in
#     which they were declared.
#
#   Rule 7.3.2e: If two or more players may declare defending cards for an
#     attack-target, they do so in clockwise order starting with the player
#     that controls the attack-target.
#
#   Rule 7.3.2f: If there are two or more attack-targets, defending cards
#     are declared for each attack-target in clockwise order of their
#     controller, starting from the player that controls the attack. Cards
#     only defend the attack-target they are declared for.
#
# Rule 7.3.3: Second, the turn-player gains priority.
#
# Rule 7.3.4: Third and finally, when the stack is empty and all players
#   pass in succession, the Defend Step ends and the Reaction Step begins.

Feature: Section 7.3 - Defend Step
    As a game engine
    I need to correctly implement the Defend Step of combat
    So that defending cards are correctly declared and placed on the combat chain

    # -----------------------------------------------------------------------
    # Rule 7.3.1 — Defend Step is a distinct game state
    # -----------------------------------------------------------------------

    Scenario: Defend Step is a game state where defending cards may be declared
        Given the Attack Step has completed
        When the Defend Step begins
        Then the Defend Step is the active game state
        And defending cards may be declared by the defending hero

    Scenario: Defend Step begins after the Attack Step ends
        Given a combat chain is open
        And the Attack Step is active
        When the stack is empty and all players pass priority in succession
        Then the Attack Step ends
        And the Defend Step begins

    # -----------------------------------------------------------------------
    # Rule 7.3.2 — Declaring defending cards
    # -----------------------------------------------------------------------

    Scenario: Declaring a card as defending does not count as playing it
        Given the Defend Step is active
        And the defending hero has a card with defense value 3 in hand
        When the defending hero declares that card as a defending card
        Then the card is added to the chain link as a defending card
        And the card does not incur any resource cost
        And no layer is added to the stack
        And no resolution abilities of that card are triggered

    Scenario: Defending hero may declare zero defending cards
        Given the Defend Step is active
        And the defending hero has cards in hand
        When the defending hero declares no defending cards
        Then no cards are added as defending cards on the chain link
        And the Defend Step proceeds normally

    Scenario: Defending hero may declare one defending card from hand
        Given the Defend Step is active
        And the defending hero has a card with defense value 2 in hand
        When the defending hero declares that hand card as a defending card
        Then that card is on the active chain link as a defending card

    Scenario: Defending hero may declare multiple defending cards from hand
        Given the Defend Step is active
        And the defending hero has two cards with defense values in hand
        When the defending hero declares both cards as defending cards
        Then both cards are on the active chain link as defending cards

    Scenario: Defending hero may declare a public equipment permanent as defending
        Given the Defend Step is active
        And the defending hero controls a public equipment permanent with defense value 2
        When the defending hero declares that equipment as a defending card
        Then that equipment is on the active chain link as a defending card

    Scenario: Defending hero may declare both hand cards and equipment as defending
        Given the Defend Step is active
        And the defending hero has a card with defense value 2 in hand
        And the defending hero controls a public equipment permanent with defense value 1
        When the defending hero declares both the hand card and the equipment as defending cards
        Then both the hand card and the equipment are on the active chain link as defending cards

    # -----------------------------------------------------------------------
    # Rule 7.3.2a — Who may declare defending cards
    # -----------------------------------------------------------------------

    Scenario: Only the defending hero's controller declares defending cards by default
        Given the Defend Step is active
        And player 1 is the defending hero's controller
        And player 2 has no rule or effect allowing them to declare defending cards
        When the Defend Step resolves defending declarations
        Then only player 1 may declare defending cards for their hero

    Scenario: Defense reaction cards cannot be declared during the Defend Step
        Given the Defend Step is active
        And the defending hero has a defense reaction card in hand
        When the defending hero attempts to declare that defense reaction card as a defending card
        Then the declaration is rejected
        And the defense reaction card is not added as a defending card

    Scenario: Non-defense-reaction cards from hand may be declared as defending
        Given the Defend Step is active
        And the defending hero has a non-defense-reaction card with defense value 2 in hand
        When the defending hero declares that card as a defending card
        Then the card is successfully added as a defending card

    # -----------------------------------------------------------------------
    # Rule 7.3.2b — Restrictions on declaring cards
    # -----------------------------------------------------------------------

    Scenario: A card without the defense property cannot be declared as defending
        Given the Defend Step is active
        And the defending hero has a card with no defense property in hand
        When the defending hero attempts to declare that card as a defending card
        Then the declaration is rejected
        And that card is not added as a defending card

    Scenario: A card with defense value of 0 can be declared as defending
        Given the Defend Step is active
        And the defending hero has a card with defense value 0 in hand
        When the defending hero declares that card as a defending card
        Then the card is successfully added as a defending card

    Scenario: A card already defending on a chain link cannot be declared again
        Given the Defend Step is active
        And a card is already a defending card on the active chain link
        When the defending hero attempts to declare that same card again as a defending card
        Then the declaration is rejected
        And the card remains as a defending card exactly once

    Scenario: A card that would make the declared set illegal cannot be declared
        Given the Defend Step is active
        And the attack has the overpower keyword
        And an action card is already declared as a defending card
        When the defending hero attempts to declare a second action card as a defending card
        Then the declaration is rejected because it would make the set of declared cards illegal

    # -----------------------------------------------------------------------
    # Rule 7.3.2c — Order of declaring multiple defending cards
    # -----------------------------------------------------------------------

    Scenario: Player decides the order in which multiple declared cards become defending
        Given the Defend Step is active
        And the defending hero has two cards with defense values in hand
        When the defending hero declares both cards with card A declared before card B
        Then card A becomes a defending card before card B
        And effects that care about the order of defending resolve accordingly

    Scenario: Order of defending matters for triggered effects dependent on order
        Given the Defend Step is active
        And the defending hero has a card with a "next card defended with" effect in play
        And the defending hero has two hand cards with defense values
        When the defending hero declares both cards with the trigger-relevant card declared second
        Then the triggered effect applies to the second card declared

    # -----------------------------------------------------------------------
    # Rule 7.3.2d — All declared cards become defending in a single compound event
    # -----------------------------------------------------------------------

    Scenario: All declared defending cards for an attack-target enter as a single compound event
        Given the Defend Step is active
        And the defending hero declares two cards as defending cards
        When the declared cards are put onto the chain link
        Then both cards are added as a single compound event
        And effects that trigger from defending together are triggered for both cards

    Scenario: Cards defending together in the same compound event trigger unity effects
        Given the Defend Step is active
        And the defending hero has a card with the unity keyword in hand
        And the defending hero has another card from hand to declare
        When the defending hero declares both the unity card and the other card together
        Then the unity card triggers its unity effect because both defended together

    Scenario: A defense reaction played later defends alone not together with previously declared cards
        Given the Defend Step is active
        And the defending hero has already declared a hand card as a defending card
        And the defending hero plays a defense reaction after the initial declaration
        When the defense reaction resolves onto the chain link
        Then the defense reaction is considered to defend alone
        And the defense reaction does not defend together with the previously declared card

    # -----------------------------------------------------------------------
    # Rule 7.3.2e — Clockwise order when multiple players may declare
    # -----------------------------------------------------------------------

    Scenario: Multiple players declare defending cards in clockwise order from attack-target controller
        Given the Defend Step is active
        And player 1 controls the attack-target
        And player 2 has an effect allowing them to declare defending cards for player 1's hero
        When defending cards are declared
        Then player 1 declares defending cards first
        And player 2 declares defending cards second in clockwise order

    # -----------------------------------------------------------------------
    # Rule 7.3.2f — Multiple attack-targets declare separately
    # -----------------------------------------------------------------------

    Scenario: With multiple attack-targets defending cards are declared for each in clockwise order
        Given the Defend Step is active
        And the attack targets two heroes controlled by player 1 and player 2
        When the defending declarations begin
        Then defending cards for the attack-target closest clockwise to the attacking player are declared first
        And defending cards for the second attack-target are declared second

    Scenario: Cards declared for one attack-target only defend that attack-target
        Given the Defend Step is active
        And the attack targets two heroes
        And player 1 declares a card to defend their hero
        When the declared cards become defending cards
        Then player 1's declared card only defends player 1's hero
        And player 1's declared card does not defend player 2's hero

    Scenario: Each attack-target's defending cards become a separate event when multiple targets exist
        Given the Defend Step is active
        And the attack targets two heroes
        And player 1 declares one card for their hero
        And player 2 declares one card for their hero
        When the declared cards become defending cards
        Then player 1's card and player 2's card become defending cards in separate events

    # -----------------------------------------------------------------------
    # Rule 7.3.3 — Turn-player gains priority
    # -----------------------------------------------------------------------

    Scenario: Turn-player gains priority after defending cards are declared
        Given the Defend Step is active
        And defending cards have been declared
        When the defending card declarations are complete
        Then the turn-player gains priority

    Scenario: Turn-player gains priority even if no defending cards are declared
        Given the Defend Step is active
        And the defending hero declares no defending cards
        When the defending card declarations are complete
        Then the turn-player gains priority

    # -----------------------------------------------------------------------
    # Rule 7.3.4 — Defend Step ends when stack is empty and all players pass
    # -----------------------------------------------------------------------

    Scenario: Defend Step ends when the stack is empty and all players pass in succession
        Given the Defend Step is active
        And the stack is empty
        When all players pass priority in succession
        Then the Defend Step ends
        And the Reaction Step begins

    Scenario: Defend Step does not end while the stack is not empty
        Given the Defend Step is active
        And a layer is on the stack
        When all players would pass priority
        Then the Defend Step does not end
        And the Reaction Step does not begin

    Scenario: Defend Step does not end if a player does not pass priority
        Given the Defend Step is active
        And the stack is empty
        And a player plays an instant during the Defend Step
        When not all players have passed priority in succession
        Then the Defend Step does not end

    Scenario: Defend Step transitions to Reaction Step once all pass with empty stack
        Given the Defend Step is active
        And a layer was on the stack but has now resolved
        And the stack is now empty
        When all players pass priority in succession
        Then the Defend Step ends
        And the Reaction Step begins
