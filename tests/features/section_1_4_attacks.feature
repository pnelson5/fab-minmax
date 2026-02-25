# Feature file for Section 1.4: Attacks
# Reference: Flesh and Blood Comprehensive Rules Section 1.4
#
# Rule 1.4.1: An attack is an object on the stack or combat chain that represents
#   an act of combat. Attack-cards, attack-layers, and attack-proxies are attacks.
# Rule 1.4.1a: The owner of an attack is the same as the owner of the card or
#   activated ability that represents it.
# Rule 1.4.1b: The controller of an attack is the same as the controller of the
#   object that represents it.
# Rule 1.4.2: An attack-card is a card with the subtype attack that is on the
#   stack or that is attacking on the combat chain.
# Rule 1.4.2a: A card with the subtype attack is only considered an attack if it
#   is on the stack or if it was put onto the combat chain as an attack. Otherwise,
#   it is not considered an attack.
# Rule 1.4.3: An attack-proxy is a non-card object with the attack ability that
#   represents the attack of another object (attack-source).
# Rule 1.4.3a: An attack-proxy is a separate object that acts as an extension of
#   its attack-source. It can only be referenced by effects using the object identity
#   "attack", but is considered to inherit the properties of its attack-source in
#   addition to any existing properties it has, with the exception of the activated
#   and resolution abilities of its attack-source. An attack-proxy is not a copy of
#   its source and does not have a copy of its source's properties.
# Rule 1.4.3b: An attack-source is an object that is represented by an attack-proxy.
# Rule 1.4.3c: An attack-proxy exists as long as its attack-source exists, and as
#   long as the attack-source is on the same chain link. If the attack-source ceases
#   to exist or is on a different chain link, the attack-proxy ceases to exist.
# Rule 1.4.3d: Effects that apply to the attack-source do not directly apply to its
#   attack-proxy. Modified properties of the attack-source ARE inherited by the proxy.
#   Replacement effects that modify effects on attacks do not modify effects on source.
# Rule 1.4.3e: Effects that reference or apply specifically to an attack-proxy do not
#   reference or apply to its attack-source.
# Rule 1.4.4: An attack-layer is a layer with the attack effect that represents an
#   attack with no properties on the stack.
# Rule 1.4.4a: An attack-layer is not an extension of its attack-source. It is either
#   a typical layer or an attack with no properties, but not both.
# Rule 1.4.4b: An attack-layer is a separate object from its attack-source for effects
#   that apply specifically to attacks.
# Rule 1.4.5: An attack-target is the target of an attack declared when the attack is
#   put onto the stack. Players must declare an attackable object controlled by an
#   opponent as the attack-target.
# Rule 1.4.5a: An object is attackable if it is a living object, or if it is made
#   attackable by an effect.
# Rule 1.4.5b: An attack-target remains the target until the combat chain closes.
#   Declaring a different target does not close the combat chain.
# Rule 1.4.5c: If an effect modifies an attack to have multiple targets, all targets
#   must be separate and legal to declare.
# Rule 1.4.6: An attack cannot be played or activated if a rule or effect would
#   prevent the player from attacking with that card or ability.

Feature: Section 1.4 - Attacks
    As a game engine
    I need to correctly implement attack objects, attack-proxies, attack-layers, and attack targets
    So that combat is resolved according to the comprehensive rules

    # =========================================================
    # Rule 1.4.1: Attacks as objects on the stack/combat chain
    # =========================================================

    # Test for Rule 1.4.1 - Attack-card on stack is an attack
    Scenario: Attack-card on stack is an attack object
        Given a player has an attack-card "Lunging Press" in hand
        When the player plays the attack-card onto the stack
        Then the card on the stack is recognized as an attack

    # Test for Rule 1.4.1 - Attack-card on combat chain is an attack
    Scenario: Attack-card on combat chain is an attack object
        Given a player has an attack-card "Lunging Press" in hand
        When the player puts the attack-card onto the combat chain
        Then the card on the combat chain is recognized as an attack

    # Test for Rule 1.4.1a - Attack owner matches card owner
    Scenario: Attack owner is the same as the card owner
        Given player 0 has an attack-card "Scar for a Scar"
        When the player plays the attack-card onto the stack
        Then the attack's owner is player 0

    # Test for Rule 1.4.1b - Attack controller matches object controller
    Scenario: Attack controller is the same as the card controller
        Given player 0 has an attack-card "Scar for a Scar"
        When the player plays the attack-card onto the stack
        Then the attack's controller is the player who played it

    # =========================================================
    # Rule 1.4.2: Attack-cards
    # =========================================================

    # Test for Rule 1.4.2 - Card with attack subtype on stack is an attack-card
    Scenario: Card with attack subtype on stack is an attack-card
        Given a card has the subtype "attack"
        When the card is placed on the stack
        Then the card is recognized as an attack-card

    # Test for Rule 1.4.2a - Attack-subtype card in hand is NOT an attack
    Scenario: Card with attack subtype in hand is not an attack
        Given a card has the subtype "attack"
        When the card is in the player's hand
        Then the card is not considered an attack

    # Test for Rule 1.4.2a - Attack-subtype card in graveyard is NOT an attack
    Scenario: Card with attack subtype in graveyard is not an attack
        Given a card has the subtype "attack"
        When the card is in the player's graveyard
        Then the card is not considered an attack

    # Test for Rule 1.4.2a - Card put on combat chain as attack IS an attack
    Scenario: Card put onto combat chain as an attack is an attack-card
        Given a card has the subtype "attack"
        When the card is put onto the combat chain as an attack
        Then the card is recognized as an attack-card

    # =========================================================
    # Rule 1.4.3: Attack-proxies
    # =========================================================

    # Test for Rule 1.4.3 - Attack-proxy represents attack-source (Bone Basher example)
    Scenario: Attack-proxy represents the attack of its attack-source
        Given a weapon card "Bone Basher" with an attack ability
        When the weapon's attack ability is activated
        Then an attack-proxy is created on the stack
        And the attack-proxy's attack-source is "Bone Basher"

    # Test for Rule 1.4.3a - Attack-proxy inherits properties from attack-source
    Scenario: Attack-proxy inherits properties from its attack-source
        Given a weapon card "Edge of Autumn" with power 1 and supertype "Ninja"
        When the weapon's attack ability is activated
        Then an attack-proxy is created
        And the attack-proxy inherits the power value 1 from "Edge of Autumn"
        And the attack-proxy inherits the supertype "Ninja" from "Edge of Autumn"

    # Test for Rule 1.4.3a - Attack-proxy does NOT inherit resolution abilities
    Scenario: Attack-proxy does not inherit resolution abilities from its attack-source
        Given a weapon card with a "go again" resolution ability
        When the weapon's attack ability is activated
        Then an attack-proxy is created
        And the attack-proxy does not inherit the "go again" resolution ability

    # Test for Rule 1.4.3a - Attack-proxy is not a copy of its source
    Scenario: Attack-proxy is a separate object and not a copy of its source
        Given a weapon card "Edge of Autumn" with an attack ability
        When the weapon's attack ability is activated
        Then an attack-proxy is created
        And the attack-proxy is a separate object from "Edge of Autumn"
        And the attack-proxy is not a copy of "Edge of Autumn"

    # Test for Rule 1.4.3b - Attack-source is the object represented by attack-proxy
    Scenario: Attack-source is the object represented by the attack-proxy
        Given a weapon card "Cintari Sellsword" with an attack ability
        When the weapon activates its attack ability
        Then an attack-proxy is created on the stack
        And "Cintari Sellsword" is identified as the attack-source of the proxy

    # Test for Rule 1.4.3c - Attack-proxy ceases to exist when attack-source leaves same chain link
    Scenario: Attack-proxy ceases to exist when attack-source moves to different chain link
        Given a weapon attack-proxy exists on chain link 1 with its attack-source
        When the weapon attacks again and moves to chain link 2
        Then the first attack-proxy ceases to exist
        And last known information is used for the first attack-proxy

    # Test for Rule 1.4.3c - Attack-proxy persists when Iris of Reality ceases to exist
    Scenario: Attack-proxy persists even if the ability creator ceases to exist
        Given an aura weapon created an attack-proxy with attack ability
        When the card granting the attack ability "Iris of Reality" ceases to exist
        Then the attack-proxy does not cease to exist

    # Test for Rule 1.4.3d - Effect on attack-source with modified properties is inherited by proxy
    Scenario: Modified properties of attack-source are inherited by attack-proxy
        Given a weapon card "Ironsong Determination" with base power 3
        And an effect gives the weapon "+1 power"
        When the weapon creates an attack-proxy
        Then the attack-proxy has power 4 inherited from the weapon's modified value

    # Test for Rule 1.4.3d - Effect on attack-source does not directly apply to proxy
    Scenario: Effect applying to attack-source does not directly apply to attack-proxy
        Given a weapon card that is a non-attack action card
        And an effect "Fog Down" applies to non-attack action cards
        When the weapon creates an attack-proxy
        Then the "Fog Down" effect does not directly apply to the attack-proxy

    # Test for Rule 1.4.3e - Effect on attack-proxy does not apply to attack-source
    Scenario: Effect on attack-proxy does not apply to its attack-source
        Given a weapon creates an attack-proxy
        And an effect "Sharpen Steel" gives "+3 power" to the next weapon attack
        When the effect is applied to the attack-proxy
        Then the effect does not carry over to the weapon after the attack resolves

    # =========================================================
    # Rule 1.4.4: Attack-layers
    # =========================================================

    # Test for Rule 1.4.4 - Attack-layer represents attack with no properties
    Scenario: Attack-layer represents an attack with no properties on the stack
        Given an activated ability creates an attack-layer on the stack
        When examining the attack-layer
        Then it is considered an attack with no properties

    # Test for Rule 1.4.4a - Attack-layer is not an extension of its attack-source
    Scenario: Attack-layer is either a typical layer or an attack but not both
        Given an activated ability creates an attack-layer on the stack
        When a continuous effect applies to "Draconic attacks"
        Then the effect does not apply to the attack-layer because it is not a Draconic attack

    # Test for Rule 1.4.4b - Attack-layer is separate from attack-source for attack effects
    Scenario: Attack-layer is a separate object for effects that apply specifically to attacks
        Given an activated ability creates an attack-layer on the stack
        When an effect applies specifically to attacks
        Then the effect applies to the attack-layer and not to the attack-source
        And if the effect does not apply to the attack-layer it may apply to the attack-source

    # =========================================================
    # Rule 1.4.5: Attack-targets
    # =========================================================

    # Test for Rule 1.4.5 - Player must declare an attackable target
    Scenario: Player must declare an attackable target when playing an attack
        Given a player plays an attack card
        When the attack is put onto the stack
        Then the player must declare a legal attack-target

    # Test for Rule 1.4.5 - Attack-target must be controlled by an opponent
    Scenario: Attack-target must be controlled by an opponent
        Given player 0 plays an attack card
        When declaring an attack-target
        Then the target must be controlled by player 1 or another opponent

    # Test for Rule 1.4.5a - Living objects are attackable
    Scenario: A living object is a valid attack-target
        Given player 1 has a hero card that is a living object
        When player 0 declares the attack
        Then the hero is a valid attack-target

    # Test for Rule 1.4.5a - Non-living object is not attackable by default
    Scenario: A non-living object is not attackable unless made so by an effect
        Given player 1 has an equipment card in the arena
        When player 0 attempts to declare the equipment as an attack-target
        Then the equipment is not a valid attack-target by default

    # Test for Rule 1.4.5a - Effect can make object attackable (Spectra example)
    Scenario: An effect can make a non-living object attackable
        Given player 1 has a card that is not a living object
        And the card has the "Spectra" ability making it a legal attack-target
        When player 0 declares the card as an attack-target
        Then the card is a valid attack-target

    # Test for Rule 1.4.5b - Attack-target persists until combat chain closes
    Scenario: Attack-target remains the target until the combat chain closes
        Given an attack is on the combat chain targeting player 1's hero
        When a subsequent attack is made targeting a different opponent object
        Then the combat chain does not close
        And the first attack's target remains unchanged

    # Test for Rule 1.4.5b - Different target on new attack does not close chain
    Scenario: Declaring a different target on a new attack does not close the combat chain
        Given an attack on chain link 1 targets player 1's hero
        When a second attack on chain link 2 targets player 1's equipment
        Then the combat chain remains open
        And the second attack has the equipment as its target

    # Test for Rule 1.4.5c - Multiple targets must be separate and legal
    Scenario: Multiple attack-targets must all be separate and legal
        Given an effect modifies an attack to have two targets
        When player 0 declares the attack-targets
        Then both targets must be separate legal attackable objects

    # Test for Rule 1.4.5c - Cannot declare the same object as multiple targets
    Scenario: Cannot declare the same object as two different attack-targets
        Given an effect modifies an attack to have two targets
        When player 0 tries to declare the same hero as both targets
        Then the declaration is invalid because targets must be separate

    # =========================================================
    # Rule 1.4.6: Attack prevention
    # =========================================================

    # Test for Rule 1.4.6 - Attack cannot be played if prevented by rule or effect
    Scenario: Attack cannot be played if a rule prevents it
        Given a player has an attack card in hand
        And an effect says the player "cannot attack" this turn
        When the player attempts to play the attack card
        Then the attack is prevented and cannot be played

    # Test for Rule 1.4.6 - Attack cannot be activated if prevented by effect
    Scenario: Attack cannot be activated if an effect prevents it
        Given a player has a weapon with an attack ability
        And an effect says the player "cannot attack with weapons" this turn
        When the player attempts to activate the weapon's attack ability
        Then the attack activation is prevented
