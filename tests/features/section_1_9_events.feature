# Feature file for Section 1.9: Events
# Reference: Flesh and Blood Comprehensive Rules Section 1.9
#
# 1.9.1 An event is a change in the game state produced by the resolution of a layer,
# the result of an effect, a transition of turn phase or combat step, or an action taken
# by a player. An event may involve physically changing the game state through one or
# more instructions - it can be modified by replacement effects (6.4) and can trigger
# triggered effects (5.5).
#
# 1.9.1a If an event comprises an instruction that involves elements outside the game,
# that event cannot be modified by replacement effects or trigger triggered effects within
# the game, unless the event directly interacts with the game.
#
# > Go Bananas has the text "Open and reveal a booster pack of Flesh and Blood and put all
# > cards with the chosen name into your hand," which creates a 'reveal' event and a 'put'
# > event as part of its resolution. The 'reveal' event only operates outside of the game,
# > so any replacement effects and triggered effects within the game do not interact with
# > it. The 'put' event directly interacts with the game by putting an object into a game
# > zone, so replacement effects and triggered effects within the game may interact with it.
#
# 1.9.1b If an event comprises an instruction to do nothing, the event does not occur.
# It cannot be modified by replacement effects and does not trigger effects.
#
# > Blazing Aether has the text "Deal X arcane damage to target hero, where X is the
# > amount of arcane damage you have dealt to that hero this turn." If the player has
# > dealt 0 arcane damage this turn, the resolution of Blazing Aether produces an event
# > that deals 0 arcane damage. Because dealing 0 arcane damage is an instruction to do
# > nothing, it simply does not occur. It cannot be modified to deal more arcane damage
# > by replacement effects, and it does not trigger effects for dealing arcane damage.
#
# 1.9.1c If an event comprises an instruction where failure cannot be verified by an
# opponent based on the current game state, that player may choose to fail to complete
# that instruction. If they do, the event simply fails as if that instruction cannot
# be completed.
#
# > Moon Wish has the text "When this hits, search your deck for a card named Sun Kiss."
# > The opponent cannot verify that a Sun Kiss is in the player's because the deck is
# > private to the player, so the player may choose to fail to find a card named
# > Sun Kiss even if there is one in their deck.
#
# 1.9.2 A compound event is an event that involves performing the same instructions more
# than once. An effect that produces a compound event is typically written in a compact
# format, where the effect specifies to repeat an instruction a number of times. When a
# compound event occurs, it is expanded, and the instructions occur as individual events.
#
# > Tome of Harvests has the text "Draw 3 cards," which is an effect written in compact
# > form, that produces a compound event that involves drawing a card three times.
# > Each draw is performed as an individual event: draw a card, draw a card, draw a card.
#
# 1.9.2a If a triggered effect triggers from a compound event, it does not trigger again
# for any of the individual events of that compound event.
#
# > Korshem, Crossroads of the Elements, has the text "Whenever a hero reveals 1 or more
# > cards," which is a triggered effect that triggers on the compound event of revealing
# > one or more cards, but does not then trigger on any of the individual events from
# > that compound event.
#
# 1.9.2b If a replacement effect replaces a compound event, it cannot replace any of
# the individual events of that compound event.
#
# > Mordred Tide has the text "Until end of turn, if you would create one or more
# > Runechant tokens, instead create that many plus 1," which replaces the compound event
# > that creates X Runechant tokens with a compound event that creates X+1 Runechant
# > tokens. It does not then replace each of the X individual "create a Runechant token"
# > event with "create 2 Runechant tokens."
#
# 1.9.2c If an event involves two or more players performing an instruction, it is a
# compound event where each player performs that instruction in clockwise order as an
# individual event, starting with the turn-player. (1.1.6) If the event was produced by
# an effect, each player performs that instruction starting with the controller of
# the effect instead.
#
# > This Round's on Me has the text "Each hero draws a card," which when resolved produces
# > a compound event that instructs each player to draw a card. This starts with the player
# > who controls This Round's on Me as it resolves on the stack.
#
# 1.9.3 A composite event is an event that is made up of one or more internal events.
# An effect that produces a composite event typically uses an effect keyword. (8.5)
#
# > Discard is a composite event that involves moving a card from a player's hand
# > to their graveyard.
#
# 1.9.3a If a composite event occurs, and the composite event and/or internal event(s)
# would trigger the triggered effect, the triggered effect only triggers once on the
# composite event.
#
# 1.9.3b If a rule or effect prevents a triggered effect from triggering on a composite
# event and/or its internal event(s), then the triggered effect does not trigger on
# the composite event.
#
# 1.9.3c Replacement effects that partially modify internal events, do not modify the
# composite event that contains it, and therefore the composite event still occurs.
#
# > Discard is a composite event that involves moving a card from the hand to the
# > graveyard. If a replacement effect replaces the destination of the move event, then
# > the discard event is still considered to occur.
#
# 1.9.3d If no internal events of a composite event occur, then the composite event is
# considered not to have occurred, and triggered effects that trigger on the composite
# event and/or internal event(s) do not trigger.
#
# > Discard is a composite event that involves moving a card from the hand to the
# > graveyard. If a replacement effect replaces the move event entirely, then the discard
# > event is considered not to occur and abilities that trigger on discard are not
# > triggered.

Feature: Section 1.9 - Events
    As a game engine
    I need to correctly implement event rules
    So that game state changes, compound events, and composite events behave correctly

    # -------------------------------------------------------------------------
    # Rule 1.9.1 - Events as game state changes
    # -------------------------------------------------------------------------

    Scenario: layer resolution produces an event
        Given a player has a card "Sigil of Solace" on the stack
        When the layer resolves
        Then a layer resolution event is produced that changes the game state
        And the event has an event type of "layer_resolution"

    Scenario: player action produces an event
        Given a player is taking a turn
        When the player performs a draw action
        Then a player action event is produced that changes the game state
        And the event has an event type of "player_action"

    Scenario: turn phase transition produces an event
        Given a game is in the start phase
        When the game transitions to the action phase
        Then a phase transition event is produced that changes the game state
        And the event has an event type of "phase_transition"

    Scenario: event can be modified by replacement effect
        Given a player has a card being drawn
        And a replacement effect that replaces draw events with two draws
        When the draw event occurs
        Then the replacement effect modifies the event
        And two cards are drawn instead of one

    Scenario: event can trigger a triggered effect
        Given a player has a triggered effect that triggers on discard
        And a player has a card to discard
        When the player discards that card
        Then the triggered effect is triggered by the discard event

    # -------------------------------------------------------------------------
    # Rule 1.9.1a - Events outside the game
    # -------------------------------------------------------------------------

    Scenario: outside-game event cannot be modified by replacement effects
        Given an effect would open and reveal a booster pack outside the game
        And a replacement effect exists that would normally modify reveal events
        When the outside-game reveal event occurs
        Then the replacement effect does not modify the outside-game reveal event

    Scenario: outside-game event that interacts with game can be modified
        Given an effect would open a booster pack and put cards into hand
        And a replacement effect exists that modifies zone-entry events
        When the put-into-hand event from the outside-game effect occurs
        Then the replacement effect can modify the put-into-hand event

    # -------------------------------------------------------------------------
    # Rule 1.9.1b - Null instruction events
    # -------------------------------------------------------------------------

    Scenario: zero damage event does not occur
        Given a card "Blazing Aether" has dealt 0 arcane damage to a hero this turn
        When the player plays Blazing Aether
        Then the event to deal 0 arcane damage does not occur
        And the event is marked as not_occurred

    Scenario: non-occurring event cannot be modified by replacement effects
        Given a null event comprising an instruction to do nothing
        And a replacement effect that would modify that null event
        When the null draw event would occur
        Then the replacement effect does not apply to the null draw event

    Scenario: non-occurring event does not trigger effects
        Given a null damage event comprising an instruction to do nothing
        And a triggered effect that triggers on that damage event type
        When the null damage event would occur
        Then the triggered damage effect is not triggered

    # -------------------------------------------------------------------------
    # Rule 1.9.1c - Unverifiable instruction events
    # -------------------------------------------------------------------------

    Scenario: player may fail unverifiable instruction
        Given a player has a "Moon Wish" card that hit
        And the player's deck is private to the opponent
        When the player must search their deck for Sun Kiss
        Then the player may choose to fail to find Sun Kiss
        And the event fails as if Sun Kiss could not be found

    Scenario: player cannot fail verifiable instruction
        Given a player must draw from their deck
        And the opponent can verify there are cards in the deck
        When the player performs the draw
        Then the player cannot choose to fail to draw a card

    # -------------------------------------------------------------------------
    # Rule 1.9.2 - Compound events
    # -------------------------------------------------------------------------

    Scenario: draw three cards is a compound event
        Given a card "Tome of Harvests" with the effect "Draw 3 cards"
        When the card resolves
        Then a compound event is created
        And the compound event contains 3 individual draw events
        And the individual events occur in sequence

    Scenario: compound event is expanded into individual events
        Given a compact effect "Create 2 Runechant tokens"
        When the compact compound event occurs
        Then the effect is expanded into 2 individual token creation events
        And each individual token creation event occurs separately

    # -------------------------------------------------------------------------
    # Rule 1.9.2a - Triggered effects on compound events
    # -------------------------------------------------------------------------

    Scenario: triggered effect on compound event fires only once
        Given a card "Korshem" with the triggered effect "Whenever a hero reveals 1 or more cards"
        And an effect that reveals 3 cards as a compound event
        When the compound reveal event occurs
        Then Korshem's triggered effect triggers exactly once
        And the triggered effect does not trigger again for each individual reveal event

    Scenario: triggered effect does not re-trigger on individual events of compound
        Given a triggered effect that triggers when a card is drawn
        And a compound event that draws 3 cards
        When the compound draw event occurs
        Then the triggered draw effect triggers exactly once on the compound event
        And the triggered draw effect does not trigger 3 more times for individual events

    # -------------------------------------------------------------------------
    # Rule 1.9.2b - Replacement effects on compound events
    # -------------------------------------------------------------------------

    Scenario: replacement effect on compound event cannot replace individual events
        Given a card "Mordred Tide" with the effect "if you would create 1 or more Runechant tokens, instead create that many plus 1"
        And an effect that creates 3 Runechant tokens
        When the compound token creation event occurs
        Then Mordred Tide replaces the compound event to create 4 tokens
        And Mordred Tide does not also replace each individual token creation with 2 tokens
        And exactly 4 Runechant tokens are created

    Scenario: replacement of compound event does not cascade to individual events
        Given a replacement effect that replaces a compound draw event
        And a compound event that draws 2 cards
        When the replacement effect replaces the compound draw event
        Then the replacement only applies to the compound draw event once
        And the individual draw events are not also replaced

    # -------------------------------------------------------------------------
    # Rule 1.9.2c - Multi-player compound events
    # -------------------------------------------------------------------------

    Scenario: multi-player event is a compound event in clockwise order from turn player
        Given a 2-player game with player 0 as the turn player
        And an effect "Each hero draws a card" that is not controlled by either player
        When the multi-player draw event occurs
        Then the multi-player event is a compound event
        And player 0 draws first as the turn player
        And player 1 draws second in clockwise order from turn player

    Scenario: multi-player event from effect starts with effect controller
        Given a 2-player game with player 1 as the turn player
        And player 0 controls the effect "Each hero draws a card" as it resolves
        When the multi-player draw event from the effect occurs
        Then the effect multi-player event is a compound event
        And player 0 draws first as the effect controller
        And player 1 draws second in clockwise order from effect controller

    # -------------------------------------------------------------------------
    # Rule 1.9.3 - Composite events
    # -------------------------------------------------------------------------

    Scenario: discard is a composite event with internal events
        Given a player has a card in hand for discarding
        When the card in hand is discarded
        Then a composite discard event occurs
        And the composite event contains an internal move event from hand to graveyard

    Scenario: composite event is made up of one or more internal events
        Given an effect keyword produces a composite event
        When the composite keyword event occurs
        Then the composite event is tracked with its internal events

    # -------------------------------------------------------------------------
    # Rule 1.9.3a - Composite event triggering
    # -------------------------------------------------------------------------

    Scenario: triggered effect only triggers once on composite event
        Given a triggered effect that triggers on discard events
        And a player has a card to discard once
        When the composite discard event occurs along with its internal move event
        Then the discard triggered effect triggers exactly once
        And the triggered effect does not trigger a second time from the internal move event

    Scenario: triggered effect on composite event does not double-trigger
        Given a triggered effect that would trigger on both discard and card-moved-to-graveyard
        And a player has a card for the double trigger check
        When the composite discard event and its internal move event both would trigger the effect
        Then the triggered effect triggers only once

    # -------------------------------------------------------------------------
    # Rule 1.9.3b - Prevented triggering on composite events
    # -------------------------------------------------------------------------

    Scenario: preventing trigger on composite event also prevents on internal events
        Given a triggered effect that would trigger on discard
        And a rule prevents the triggered effect from triggering on the discard event
        When the composite discard event occurs
        Then the triggered effect does not trigger on the composite event
        And the triggered effect does not trigger from any internal event either

    # -------------------------------------------------------------------------
    # Rule 1.9.3c - Partial replacement of composite events
    # -------------------------------------------------------------------------

    Scenario: replacing internal event destination does not prevent composite event
        Given a player has a card to discard with destination replacement
        And a replacement effect that changes the destination of move events to banished zone
        When the player discards the card with replacement active
        Then the replacement effect modifies the internal move event destination to banished
        And the composite discard event still occurs
        And the card ends up in the banished zone not the graveyard

    Scenario: partial modification of internal event leaves composite event intact
        Given a replacement effect that partially modifies an internal event
        When the composite event containing the modified internal event occurs
        Then the composite event is not replaced or cancelled
        And the composite event still occurs with the modified internal event

    # -------------------------------------------------------------------------
    # Rule 1.9.3d - All internal events fail
    # -------------------------------------------------------------------------

    Scenario: composite event does not occur if all internal events are replaced
        Given a player has a card to discard with full replacement
        And a replacement effect that completely replaces the move event in a discard
        When the player attempts to discard the card with full replacement
        Then the internal move event is replaced entirely and does not occur
        And the composite discard event is considered not to have occurred
        And triggered effects on discard do not trigger

    Scenario: all-internal-events-fail prevents composite event triggering
        Given a triggered effect that triggers on discard
        And a replacement effect that fully replaces the move-to-graveyard internal event
        When the player discards a card with the full replacement active
        Then the composite discard event does not occur
        And the triggered effect on discard is not triggered
