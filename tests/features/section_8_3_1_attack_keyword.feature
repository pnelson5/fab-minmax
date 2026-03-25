# Feature file for Section 8.3.1: Attack (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.1
#
# 8.3.1 Attack
#   Attack is a static ability. A layer with the attack ability is an attack-proxy.
#
# 8.3.1a When an attack-proxy resolves on the stack, it and its source move onto the
#         combat chain as a chain link.
#
# 8.3.1b If an attack-proxy is added to the stack, the combat chain opens (if it is
#         closed) and the Layer Step of combat begins.
#
# 8.3.1c To add an attack-proxy onto the stack, a legal attackable target must be
#         declared as the target of the attack.
#
# Related rules used in scenarios:
# 1.4.3  An attack-proxy is a non-card object with the attack ability that represents
#         the attack of another object (attack-source).
# 1.4.3a An attack-proxy inherits the properties of its attack-source (except
#         activated and resolution abilities of the source).
# 1.4.3c An attack-proxy exists as long as its attack-source exists and is on the
#         same chain link. If the source ceases to exist, the proxy ceases to exist.
# 1.4.3d Effects on the attack-source do not directly apply to its attack-proxy.
# 1.4.3e Effects on the attack-proxy do not apply to its attack-source.
# 1.4.5a An object is attackable if it is a living object, or if made attackable
#         by an effect.

Feature: Section 8.3.1 - Attack Ability Keyword
    As a game engine
    I need to correctly implement the Attack ability keyword
    So that weapon attacks and attack-proxies function according to the rules

    # ===== Rule 8.3.1: Attack is a static ability; layer with attack = attack-proxy =====

    Scenario: Attack keyword is a static ability on a layer
        Given a weapon card with the "Attack" ability
        When I inspect the attack ability on the weapon
        Then the attack ability is a static ability

    Scenario: A layer with the attack ability is an attack-proxy
        Given a weapon card with the "Attack" ability
        When the weapon activates its attack ability to create a layer on the stack
        Then the layer on the stack is an attack-proxy

    Scenario: An attack-proxy is a non-card object
        Given a weapon card with the "Attack" ability
        When the weapon activates its attack ability to create a layer on the stack
        Then the attack-proxy on the stack is not a card object
        And the attack-proxy represents the weapon as its attack-source

    # ===== Rule 8.3.1a: Attack-proxy and source move to combat chain on resolution =====

    Scenario: Attack-proxy and source move to combat chain when proxy resolves
        Given a weapon card with the "Attack" ability
        And an attack-proxy for the weapon is on the stack
        When the attack-proxy resolves from the stack
        Then the attack-proxy is on the combat chain as the active-attack
        And the weapon is on the same chain link as the attack-proxy

    Scenario: Attack-proxy becomes the active-attack on resolution
        Given a weapon card with the "Attack" ability
        And an attack-proxy for the weapon is on the stack
        When the attack-proxy resolves from the stack
        Then the attack-proxy is the active-attack for that chain link
        And the weapon is in the attacking state

    # ===== Rule 8.3.1b: Combat chain opens and Layer Step begins when proxy added =====

    Scenario: Combat chain opens when attack-proxy is added to a closed stack
        Given the combat chain is closed
        And a player controls a weapon with an attack ability
        When the player adds an attack-proxy to the stack
        Then the combat chain is open

    Scenario: Layer Step of combat begins when attack-proxy is added to stack
        Given the combat chain is closed
        And a player controls a weapon with an attack ability
        When the player adds an attack-proxy to the stack
        Then the Layer Step of combat has begun

    Scenario: Adding second attack-proxy does not close and reopen combat chain
        Given the combat chain is open with one chain link
        And a player controls a weapon with an attack ability
        When the player adds a second attack-proxy to the stack
        Then the combat chain remains open

    # ===== Rule 8.3.1c: Legal attackable target must be declared =====

    Scenario: A legal attackable target must be declared to add attack-proxy to stack
        Given a player controls a weapon with an attack ability
        And there is a living opponent hero that is a legal attackable target
        When the player declares the opponent hero as the attack target
        And the player adds an attack-proxy to the stack
        Then the attack-proxy is on the stack with the declared target

    Scenario: Cannot add attack-proxy to stack without declaring a target
        Given a player controls a weapon with an attack ability
        When the player attempts to add an attack-proxy without declaring a target
        Then the attack-proxy cannot be added to the stack

    Scenario: Cannot add attack-proxy to stack when no legal attackable target exists
        Given a player controls a weapon with an attack ability
        And there are no legal attackable targets
        When the player attempts to add an attack-proxy to the stack
        Then the attack-proxy cannot be added to the stack

    # ===== Rule 1.4.3a: Attack-proxy inherits source properties =====

    Scenario: Attack-proxy inherits name and type properties from its source
        Given a weapon named "Bone Basher" with 2 power and the "Attack" ability
        When the weapon activates its attack ability to create an attack-proxy
        Then the attack-proxy inherits the name "Bone Basher" from its source
        And the attack-proxy inherits the power value 2 from its source

    Scenario: Attack-proxy does not inherit activated abilities from its source
        Given a weapon with an activated ability and an attack ability
        When the weapon activates its attack ability to create an attack-proxy
        Then the attack-proxy does not have the source's activated abilities

    Scenario: Attack-proxy does not inherit resolution abilities from its source
        Given a weapon with a resolution ability "When this hits" and an attack ability
        When the weapon activates its attack ability to create an attack-proxy
        Then the attack-proxy does not inherit the resolution abilities from its source

    # ===== Rule 1.4.3c: Attack-proxy ceases to exist if source leaves chain link =====

    Scenario: Attack-proxy ceases to exist when its source ceases to exist on the stack
        Given a weapon card with the "Attack" ability
        And an attack-proxy for the weapon is on the stack
        When the weapon (attack-source) ceases to exist
        Then the attack-proxy also ceases to exist

    # ===== Rule 1.4.3d/e: Effect isolation between proxy and source =====

    Scenario: Effects on attack-source do not directly apply to its attack-proxy
        Given a weapon with a continuous effect that modifies the weapon's power
        And an attack-proxy for the weapon is on the combat chain
        When a separate effect directly modifies the weapon's power property
        Then the power modification does not directly apply to the attack-proxy

    Scenario: Effects on attack-proxy do not apply to its attack-source
        Given a weapon card with an attack-proxy on the combat chain
        When an effect specifically targets the attack-proxy and modifies its power
        Then that power modification does not apply to the weapon (attack-source)
