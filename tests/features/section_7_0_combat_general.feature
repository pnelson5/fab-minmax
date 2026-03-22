# Feature file for Section 7.0: General (Combat)
# Reference: Flesh and Blood Comprehensive Rules Section 7.0
#
# Rule 7.0.1: Combat is a game state where the combat chain is open and attacks undergo
# resolution in steps on the stack and combat chain. The resolution of a chain link
# consists of seven steps in order: Layer, Attack, Defend, Reaction, Damage, Resolution, and Close.
#
# Rule 7.0.1a: During combat, while the combat chain is open, a player cannot play cards
# or activate activated abilities with the type action, except for attacks during the
# Resolution Step. Action cards/abilities can still be played/activated as instants.
#
# Rule 7.0.2: The combat chain is a zone that is open during combat and closed otherwise.
# It comprises chain links when open, and is empty when closed.
#
# Rule 7.0.2a: The combat chain starts closed. When an attack is added to the stack while
# the combat chain is closed, the combat chain opens and the Layer Step begins immediately.
# It remains open until closed again (7.7.2).
#
# Rule 7.0.2b: "This combat chain" refers to the current combat chain if it is open.
# If the combat chain is closed, the effect fails to be generated.
#
# Rule 7.0.3: A chain link is an element of the combat chain representing the resolution
# of an attack. A chain link is neither an object nor a zone. It comprises an active-attack,
# an attack-source (if any), and any number of defending cards.
#
# Rule 7.0.3a: A chain link is created when an attack is added to the combat chain.
# The attack becomes the active-attack of chain link N+1.
#
# Rule 7.0.3b: The active chain link is the most recent chain link being resolved.
#
# Rule 7.0.3c: The properties, control, and ownership of a chain link equal those of its
# active-attack. If the active-attack ceases to exist, LKI is used.
#
# Rule 7.0.3d: "This chain link" refers to the active chain link. If there is no active
# chain link, the effect fails to be generated.
#
# Rule 7.0.3e: Any layer played/activated/triggered during combat (while a chain link is
# active) is considered to be on the active chain link.
#
# Rule 7.0.3f: Cards on a chain link are considered to be on the combat chain and in the arena.
#
# Rule 7.0.4: An active-attack is an attack that has been put onto the combat chain as a chain link.
#
# Rule 7.0.4a: If a card is put onto a chain link as an attacking card, the existing
# active-attack (if any) is cleared, and the new card becomes the active-attack.
# It is considered a new attack, but attack target(s) remain the same.
#
# Rule 7.0.5: A defending card is a card designated as defending on a chain link for an
# attack-target by a rule or effect.
#
# Rule 7.0.5a: To be added as a defending card, the card is put on the chain link.
# The card is considered defending until it leaves the combat chain. The "defend" event
# then occurs, triggering effects from defending.
#
# Rule 7.0.5b: If an effect would add a card as a defending card, but the card is already
# defending on that chain link or cannot become a defending card, the effect fails,
# no defend event occurs, and the card does not move zones.
#
# Rule 7.0.5c: A defending card defends against the active-attack. If the active-attack
# ceases to exist, LKI is used.
#
# Rule 7.0.5d: A card can only defend on one chain link for one attack-target at a time.
#
# Rule 7.0.5e: If exactly one card is put onto a chain link as a defending card, it
# defends alone. If two or more cards are added in the same event, they defend together.

Feature: Section 7.0 - Combat General Rules
    As a game engine
    I need to correctly implement combat fundamentals
    So that the combat chain, chain links, active-attacks, and defending cards work per the rules

    # -----------------------------------------------------------------------
    # Rule 7.0.1 - Combat is a game state with an open combat chain
    # -----------------------------------------------------------------------

    Scenario: Combat is a game state where the combat chain is open
        Given a game state is initialized
        And the combat chain is open
        When we check the game state
        Then the game is in combat

    Scenario: Combat resolution proceeds through seven ordered steps
        Given a game state is initialized
        When we list the combat chain resolution steps
        Then the steps are "Layer, Attack, Defend, Reaction, Damage, Resolution, Close" in order

    # -----------------------------------------------------------------------
    # Rule 7.0.1a - Action cards cannot be played during combat (non-instant)
    # -----------------------------------------------------------------------

    Scenario: Action cards cannot be played during combat except as instants
        Given a game state is initialized
        And the combat chain is open
        And a player has an action card in hand
        When the player attempts to play the action card as a non-instant
        Then the play attempt fails
        And the reason is "action cards cannot be played as non-instants during combat"

    Scenario: Action cards can be played as instants during combat
        Given a game state is initialized
        And the combat chain is open
        And a player has an action card in hand
        When the player attempts to play the action card as an instant
        Then the play attempt is not blocked by the combat restriction

    Scenario: Activated abilities with type action cannot be activated during combat as non-instants
        Given a game state is initialized
        And the combat chain is open
        And a player has an activated ability with type action
        When the player attempts to activate the ability as a non-instant
        Then the activation attempt fails
        And the reason is "action abilities cannot be activated as non-instants during combat"

    # -----------------------------------------------------------------------
    # Rule 7.0.2 - Combat chain as a zone
    # -----------------------------------------------------------------------

    Scenario: The combat chain is a zone
        Given a game state is initialized
        When we check the combat chain zone type
        Then the combat chain is recognized as a zone

    Scenario: The combat chain starts the game closed
        Given a new game is initialized
        When we check whether the combat chain is open
        Then the combat chain is closed

    Scenario: The combat chain is empty when closed
        Given a game state is initialized
        And the combat chain is closed
        When we check the combat chain contents
        Then the combat chain has no chain links

    Scenario: The combat chain contains chain links when open
        Given a game state is initialized
        And the combat chain is open
        And an attack has been placed on the combat chain as a chain link
        When we check the combat chain contents
        Then the combat chain has at least one chain link

    # -----------------------------------------------------------------------
    # Rule 7.0.2a - Combat chain opens when attack is added to stack
    # -----------------------------------------------------------------------

    Scenario: Combat chain opens when an attack is added to the stack
        Given a game state is initialized
        And the combat chain is closed
        When an attack is added to the stack
        Then the combat chain opens
        And the Layer Step begins

    Scenario: Combat chain remains open through subsequent chain links
        Given a game state is initialized
        And the combat chain is open with one chain link
        When a second attack is added to the stack
        Then the combat chain remains open

    # -----------------------------------------------------------------------
    # Rule 7.0.2b - "This combat chain" refers to the current open chain
    # -----------------------------------------------------------------------

    Scenario: Effect referencing this combat chain works when chain is open
        Given a game state is initialized
        And the combat chain is open
        And there is an effect that references "this combat chain"
        When we check if the effect can be generated
        Then the effect can be generated referencing the current combat chain

    Scenario: Effect referencing this combat chain fails when chain is closed
        Given a game state is initialized
        And the combat chain is closed
        And there is an effect that references "this combat chain"
        When we check if the effect can be generated
        Then the effect fails to be generated

    # -----------------------------------------------------------------------
    # Rule 7.0.3 - Chain link structure
    # -----------------------------------------------------------------------

    Scenario: A chain link is neither an object nor a zone
        Given a game state is initialized
        And a chain link exists on the combat chain
        When we check the type of the chain link
        Then the chain link is not an object
        And the chain link is not a zone

    Scenario: A chain link comprises an active-attack and optional defending cards
        Given a game state is initialized
        And a chain link exists on the combat chain with an attack card
        When we inspect the chain link components
        Then the chain link has an active-attack
        And the chain link has zero or more defending cards

    # -----------------------------------------------------------------------
    # Rule 7.0.3a - Chain link creation and numbering
    # -----------------------------------------------------------------------

    Scenario: Chain link is created when attack is added to combat chain
        Given a game state is initialized
        And the combat chain is open with zero chain links
        When an attack is added to the combat chain as a chain link
        Then chain link 1 exists on the combat chain
        And the attack is the active-attack of chain link 1

    Scenario: Second attack creates chain link N+1
        Given a game state is initialized
        And the combat chain is open with one chain link
        When a second attack is added to the combat chain as a chain link
        Then chain link 2 exists on the combat chain
        And the second attack is the active-attack of chain link 2

    # -----------------------------------------------------------------------
    # Rule 7.0.3b - Active chain link
    # -----------------------------------------------------------------------

    Scenario: The most recent chain link is the active chain link
        Given a game state is initialized
        And the combat chain has two chain links
        When we check the active chain link
        Then the active chain link is chain link 2

    Scenario: The active chain link remains until it resolves or combat chain closes
        Given a game state is initialized
        And chain link 1 is the active chain link
        When chain link 1 resolves
        Then chain link 1 is no longer the active chain link

    # -----------------------------------------------------------------------
    # Rule 7.0.3c - Chain link properties from active-attack (+ LKI)
    # -----------------------------------------------------------------------

    Scenario: Chain link properties match the active-attack properties
        Given a game state is initialized
        And a chain link exists with an attack card controlled by player 0
        When we check the chain link properties
        Then the chain link controller matches the active-attack controller
        And the chain link owner matches the active-attack owner

    Scenario: Chain link uses last-known information when active-attack ceases to exist
        Given a game state is initialized
        And a chain link exists with an attack card controlled by player 0
        When the active-attack ceases to exist
        Then the chain link properties still reference the last-known controller
        And the chain link properties still reference the last-known owner

    # -----------------------------------------------------------------------
    # Rule 7.0.3d - "This chain link" effect reference
    # -----------------------------------------------------------------------

    Scenario: Effect referencing this chain link works when active chain link exists
        Given a game state is initialized
        And the combat chain is open with an active chain link
        And there is an effect that references "this chain link"
        When we check if the effect can be generated
        Then the effect references the active chain link

    Scenario: Effect referencing this chain link fails when no active chain link exists
        Given a game state is initialized
        And there is no active chain link
        And there is an effect that references "this chain link"
        When we check if the effect can be generated
        Then the effect fails to be generated

    # -----------------------------------------------------------------------
    # Rule 7.0.3e - Layers during combat are on the active chain link
    # -----------------------------------------------------------------------

    Scenario: A layer played during combat is associated with the active chain link
        Given a game state is initialized
        And the combat chain is open with an active chain link
        When a layer is played during combat
        Then the layer is associated with the active chain link

    # -----------------------------------------------------------------------
    # Rule 7.0.3f - Cards on chain link are on combat chain and in arena
    # -----------------------------------------------------------------------

    Scenario: A card on a chain link is considered to be on the combat chain
        Given a game state is initialized
        And an attack card is on a chain link
        When we check the card's zone membership
        Then the card is on the combat chain

    Scenario: A card on a chain link is also considered to be in the arena
        Given a game state is initialized
        And an attack card is on a chain link
        When we check the card's zone membership
        Then the card is in the arena

    # -----------------------------------------------------------------------
    # Rule 7.0.4 - Active-attack definition
    # -----------------------------------------------------------------------

    Scenario: The active-attack is an attack put onto the combat chain as a chain link
        Given a game state is initialized
        And an attack is put onto the combat chain
        When we check the active-attack
        Then the attack is the active-attack of the chain link

    # -----------------------------------------------------------------------
    # Rule 7.0.4a - Replacing the active-attack on a chain link
    # -----------------------------------------------------------------------

    Scenario: Putting a new attacking card clears the existing active-attack
        Given a game state is initialized
        And a chain link exists with attack card A as the active-attack
        When card B is put onto the chain link as the new attacking card
        Then card A is no longer the active-attack
        And card B is the new active-attack for that chain link

    Scenario: Replacing the active-attack preserves the attack target
        Given a game state is initialized
        And a chain link exists with attack card A targeting player 1
        When card B is put onto the chain link as the new attacking card
        Then card B's attack target is still player 1

    Scenario: The replacement attacking card is considered a new attack
        Given a game state is initialized
        And a chain link exists with attack card A as the active-attack
        When card B is put onto the chain link as the new attacking card
        Then card B is considered a new attack for rules and effects

    # -----------------------------------------------------------------------
    # Rule 7.0.5 - Defending cards
    # -----------------------------------------------------------------------

    Scenario: A defending card is designated as defending on a chain link by a rule or effect
        Given a game state is initialized
        And a chain link exists with an active-attack
        When a card is designated as a defending card on that chain link
        Then the card is a defending card

    Scenario: A defending card remains defending until it leaves the combat chain
        Given a game state is initialized
        And a card is a defending card on the active chain link
        When we check the card's status
        Then the card is still defending
        When the card leaves the combat chain
        Then the card is no longer defending

    # -----------------------------------------------------------------------
    # Rule 7.0.5a - Adding a defending card causes the defend event
    # -----------------------------------------------------------------------

    Scenario: The defend event occurs after a defending card is added
        Given a game state is initialized
        And a chain link exists with an active-attack
        When a card is put onto the chain link as a defending card
        Then the defend event occurs
        And effects that trigger from defending are triggered

    Scenario: The controller at defend time is considered to have defended with the card
        Given a game state is initialized
        And a chain link exists with an active-attack
        And a card is controlled by player 0
        When player 0 puts the card onto the chain link as a defending card
        Then player 0 is considered to have defended with that card

    # -----------------------------------------------------------------------
    # Rule 7.0.5b - Failed defend addition
    # -----------------------------------------------------------------------

    Scenario: Adding a card already defending on the chain link fails
        Given a game state is initialized
        And a chain link exists with an active-attack
        And card X is already defending on that chain link
        When an effect tries to add card X as a defending card again on the same chain link
        Then the effect fails
        And no defend event occurs
        And card X remains on the chain link unchanged

    Scenario: Adding a card blocked by another effect from defending fails
        Given a game state is initialized
        And a chain link exists with an active-attack
        And an effect prevents card Y from becoming a defending card
        When an effect tries to add card Y as a defending card on that chain link
        Then the effect fails
        And no defend event occurs
        And card Y does not move zones

    # -----------------------------------------------------------------------
    # Rule 7.0.5c - Defending against active-attack (+ LKI)
    # -----------------------------------------------------------------------

    Scenario: A defending card defends against the active-attack
        Given a game state is initialized
        And a chain link exists with attack card A as the active-attack
        And card D is a defending card on that chain link
        When we check what card D is defending against
        Then card D is defending against attack card A

    Scenario: Defending card uses last-known information if active-attack ceases to exist
        Given a game state is initialized
        And a chain link exists with attack card A as the active-attack
        And card D is a defending card on that chain link
        When attack card A ceases to exist
        Then card D still references last-known information about attack card A

    # -----------------------------------------------------------------------
    # Rule 7.0.5d - Card can only defend on one chain link at a time
    # -----------------------------------------------------------------------

    Scenario: A card can only defend on one chain link for one attack-target at a time
        Given a game state is initialized
        And card Z is already defending on chain link 1 for attack-target player 1
        When an effect tries to add card Z as a defending card on chain link 2
        Then the second defend attempt fails
        And card Z remains defending only on chain link 1

    # -----------------------------------------------------------------------
    # Rule 7.0.5e - Defend alone vs defend together
    # -----------------------------------------------------------------------

    Scenario: Exactly one defending card added is considered to defend alone
        Given a game state is initialized
        And a chain link exists with an active-attack
        When exactly one card is put onto the chain link as a defending card
        Then that card defends alone

    Scenario: Two cards added in the same event defend together
        Given a game state is initialized
        And a chain link exists with an active-attack
        When two cards are put onto the chain link as defending cards in the same event
        Then those cards defend together

    Scenario: A defense reaction added after declared defenders defends alone
        Given a game state is initialized
        And a chain link exists with an active-attack
        And two cards were declared as defenders together
        When a defense reaction is played adding one more card as a defending card
        Then the defense reaction card defends alone despite other defenders already being present
