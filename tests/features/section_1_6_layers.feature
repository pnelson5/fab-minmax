# Feature file for Section 1.6: Layers
# Reference: Flesh and Blood Comprehensive Rules Section 1.6
#
# 1.6.1 A layer is an object on the stack that is yet to be resolved.
#        Card-layers, activated-layers, and triggered-layers are layers.
#
# 1.6.1a The owner of a card-layer is the player who owns the card.
#         The owner of an activated-layer is the player who activated the activated ability.
#         The owner of a triggered-layer is the player who controlled the source of the
#         triggered effect when the triggered-layer was created.
#
# 1.6.1b The controller of a layer is the player that put it on the stack.
#
# 1.6.2  There are 3 categories of layers: card-, activated-, and triggered-layers.
#
# 1.6.2a A card-layer is a layer represented by a card on the stack.
#
# 1.6.2b An activated-layer is a layer created by an activated ability.
#         An activated-layer is created on the stack, and then can only exist on the stack.
#         Example: Energy Potion has "Instant – Destroy this: Gain {r}{r}."
#         When activated, creates an activated-layer on the stack with "Gain {r}{r}."
#
# 1.6.2c A triggered-layer is a layer created by a triggered effect.
#         A triggered-layer is created before it is put on the stack, and then can only
#         exist on the stack.
#         Example: Snatch has "When this hits, draw a card." When triggered, creates a
#         triggered-layer to be put on the stack with "Draw a card."

Feature: Section 1.6 - Layers
    As a game engine
    I need to correctly implement layer rules
    So that cards, activated abilities, and triggered effects correctly resolve from the stack

    # =========================================================================
    # Rule 1.6.1: A layer is an object on the stack that is yet to be resolved
    # =========================================================================

    # Test for Rule 1.6.1 - Layers are objects on the stack awaiting resolution
    Scenario: A layer is an object on the stack yet to be resolved
        Given a game is in progress
        And a player has an action card in hand
        When the player plays the action card
        Then the card becomes a layer on the stack
        And the layer has not yet been resolved
        And the layer is recognized as a game object

    # Test for Rule 1.6.1 - Card-layers, activated-layers, and triggered-layers are layers
    Scenario: All three layer types are recognized as layers
        Given a game is in progress
        And a card-layer exists on the stack
        And an activated-layer exists on the stack
        And a triggered-layer exists on the stack
        Then all three are recognized as layers
        And each layer is an object on the stack

    # =========================================================================
    # Rule 1.6.1a: Owner determination for each layer type
    # =========================================================================

    # Test for Rule 1.6.1a - Owner of card-layer is the card owner
    Scenario: Card-layer owner is the player who owns the card
        Given a game is in progress
        And player 0 owns an action card
        When player 0 plays the action card onto the stack
        Then a card-layer is created on the stack
        And the card-layer owner is player 0

    # Test for Rule 1.6.1a - Owner of activated-layer is activating player
    Scenario: Activated-layer owner is the player who activated the ability
        Given a game is in progress
        And player 0 has a card with an activated ability
        When player 0 activates the activated ability
        Then an activated-layer is created on the stack
        And the activated-layer owner is player 0

    # Test for Rule 1.6.1a - Owner of triggered-layer is controller of source when triggered
    Scenario: Triggered-layer owner is the controller of the source at trigger time
        Given a game is in progress
        And player 0 controls a card with a triggered effect
        When the triggered effect fires
        Then a triggered-layer is created on the stack
        And the triggered-layer owner is player 0

    # Test for Rule 1.6.1a - Triggered-layer owner differs from who puts it on stack
    Scenario: Triggered-layer owner is based on who controlled source when it triggered
        Given a game is in progress
        And player 0 originally controlled a card with a triggered effect
        And the source card changed controller to player 1 before triggering
        When the triggered effect fires while player 1 controls the source
        Then a triggered-layer is created on the stack
        And the triggered-layer owner is player 1

    # =========================================================================
    # Rule 1.6.1b: Controller of a layer is the player that put it on the stack
    # =========================================================================

    # Test for Rule 1.6.1b - Controller of card-layer is the player who played it
    Scenario: Controller of a card-layer is the player who put it on the stack
        Given a game is in progress
        And player 0 has an action card in hand
        When player 0 plays the action card onto the stack
        Then a card-layer is on the stack
        And the card-layer controller is player 0

    # Test for Rule 1.6.1b - Controller of activated-layer is the activating player
    Scenario: Controller of an activated-layer is the player who activated it
        Given a game is in progress
        And player 0 has a card with an activated ability
        When player 0 activates the activated ability putting a layer on the stack
        Then the activated-layer controller is player 0

    # Test for Rule 1.6.1b - Controller of triggered-layer is the player who put it on stack
    Scenario: Controller of a triggered-layer is the player who put it on the stack
        Given a game is in progress
        And player 0 controls a card with a triggered effect
        When the triggered effect fires and the triggered-layer is put on the stack
        Then the triggered-layer controller is player 0

    # =========================================================================
    # Rule 1.6.2: The three layer categories
    # =========================================================================

    # Test for Rule 1.6.2 - There are exactly 3 layer categories
    Scenario: There are exactly 3 categories of layers
        Given a game engine with layer support
        When the layer categories are queried
        Then there are exactly 3 layer categories
        And the categories are card-layer, activated-layer, and triggered-layer

    # =========================================================================
    # Rule 1.6.2a: A card-layer is a layer represented by a card on the stack
    # =========================================================================

    # Test for Rule 1.6.2a - Card on stack is a card-layer
    Scenario: A card played to the stack becomes a card-layer
        Given a game is in progress
        And player 0 has an action card in hand
        When player 0 plays the action card onto the stack
        Then a card-layer exists on the stack
        And the layer is categorized as a card-layer
        And the card-layer is represented by the action card

    # Test for Rule 1.6.2a - Card-layer is the card itself on the stack
    Scenario: A card-layer retains the card's properties
        Given a game is in progress
        And player 0 has an action card named "Lunging Press" in hand
        When player 0 plays "Lunging Press" onto the stack
        Then the card-layer on the stack has name "Lunging Press"
        And the card-layer is the card itself on the stack

    # =========================================================================
    # Rule 1.6.2b: An activated-layer is a layer created by an activated ability
    # =========================================================================

    # Test for Rule 1.6.2b - Activated ability creates activated-layer (Energy Potion example)
    Scenario: Activating an ability creates an activated-layer on the stack
        Given a game is in progress
        And player 0 has an "Energy Potion" card with activated ability "Destroy this: Gain 2 resources"
        When player 0 activates the ability of "Energy Potion"
        Then an activated-layer is created on the stack
        And the activated-layer has resolution ability "Gain 2 resources"
        And the activated-layer category is "activated-layer"

    # Test for Rule 1.6.2b - Activated-layer can only exist on the stack
    Scenario: An activated-layer can only exist on the stack
        Given a game is in progress
        And player 0 activates an ability creating an activated-layer
        When the activated-layer is queried for its valid zones
        Then the activated-layer can only exist on the stack
        And it cannot exist in hand, graveyard, banished, or arena zones

    # =========================================================================
    # Rule 1.6.2c: A triggered-layer is a layer created by a triggered effect
    # =========================================================================

    # Test for Rule 1.6.2c - Triggered effect creates triggered-layer (Snatch example)
    Scenario: A triggered effect creates a triggered-layer when it fires
        Given a game is in progress
        And a "Snatch" card with triggered effect "When this hits, draw a card" is on the combat chain
        When "Snatch" hits the defending player
        Then a triggered-layer is created
        And the triggered-layer is put on the stack
        And the triggered-layer has resolution ability "Draw a card"
        And the triggered-layer category is "triggered-layer"

    # Test for Rule 1.6.2c - Triggered-layer is created before being put on stack
    Scenario: A triggered-layer is created before it is put on the stack
        Given a game is in progress
        And a card with a triggered effect is on the combat chain
        When the triggered effect fires
        Then the triggered-layer is first created as an object
        And then the triggered-layer is put on the stack
        And the triggered-layer can only exist on the stack once placed

    # Test for Rule 1.6.2c - Triggered-layer can only exist on the stack
    Scenario: A triggered-layer can only exist on the stack
        Given a game is in progress
        And a triggered-layer has been created by a triggered effect
        When the triggered-layer is queried for its valid zones
        Then the triggered-layer can only exist on the stack
        And it cannot exist outside the stack

    # =========================================================================
    # Rule 1.6.1 + 1.6.2: Layer interaction - source independence
    # =========================================================================

    # Test for Rule 1.7.1a cross-reference - Layers exist independently of their source
    Scenario: An activated-layer continues to exist even if its source is destroyed
        Given a game is in progress
        And player 0 activates an ability creating an activated-layer
        And "Energy Potion" is destroyed after the activated-layer is created
        When the activated-layer is on the stack awaiting resolution
        Then the activated-layer still exists on the stack
        And the absence of "Energy Potion" does not prevent resolution

    # Test for Rule 1.7.1a cross-reference - Triggered-layer exists independently
    Scenario: A triggered-layer continues to exist even if its source leaves play
        Given a game is in progress
        And a card with a triggered effect fires creating a triggered-layer
        And the source card moves to the graveyard after the triggered-layer is created
        When the triggered-layer is on the stack awaiting resolution
        Then the triggered-layer still exists on the stack
        And the source being gone does not prevent the triggered-layer from resolving
