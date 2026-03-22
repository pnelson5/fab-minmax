# Feature file for Section 5.0: General (Layers, Cards, & Abilities)
# Reference: Flesh and Blood Comprehensive Rules Section 5.0
#
# Section 5.0 General is an introductory header for Chapter 5: Layers, Cards, & Abilities.
# There are no specific numbered rules in section 5.0; detailed rules are in:
#   - 5.1: Playing Cards
#   - 5.2: Activated Abilities
#   - 5.3: Resolution Abilities & Resolving Layers
#   - 5.4: Static Abilities
#
# Chapter 5 governs how cards are played onto the stack, how abilities are activated
# and resolved, and how static abilities apply. The stack is the mechanism through
# which cards and abilities are placed and then resolved in LIFO (last-in, first-out)
# order. Layers on the stack can be card-layers, activated-layers, or triggered-layers.

Feature: Section 5.0 - Layers, Cards, and Abilities General
    As a game engine
    I need to correctly model the chapter 5 concepts of layers, cards, and abilities
    So that card play, ability activation, and resolution work correctly

    # ===== Chapter 5 Introduction: Layers concept =====

    # Test for Chapter 5 introduction - The stack holds layers
    Scenario: The stack holds layers representing played cards and abilities
        Given a game is in progress
        When a player plays a card or activates an ability
        Then a layer is placed on the stack
        And the layer is the topmost element of the stack

    # Test for Chapter 5 introduction - Layers resolve in LIFO order
    Scenario: Layers on the stack resolve in last-in first-out order
        Given a game is in progress
        And a card layer is on the stack
        When a player plays a second card placing another layer on the stack
        Then the second layer is on top
        And if priority is passed by all players the second layer resolves first

    # Test for Chapter 5 introduction - Engine tracks card play steps
    Scenario: Playing a card involves multiple ordered steps
        Given a player has a card in hand
        When the player initiates playing that card
        Then the engine initiates the card play step sequence
        And the steps include announce, declare costs, declare modes and targets, check legal play, calculate asset-costs, pay asset-costs, calculate effect-costs, pay effect-costs, and play

    # Test for Chapter 5 introduction - Abilities exist on cards
    Scenario: Cards have abilities that define their interactions with the game
        Given a player has a card with an activated ability
        When the player examines the card
        Then the card has at least one ability
        And abilities are a property of the card

    # Test for Chapter 5 introduction - Static abilities apply continuously
    Scenario: Static abilities apply continuously without being placed on the stack
        Given a permanent with a static ability is in play
        When the game state is evaluated
        Then the static ability applies continuously
        And the static ability does not go on the stack to apply
