# Feature file for Section 8.3.14: Spectra (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.14
#
# 8.3.14 Spectra
#   Spectra is a static ability and a triggered-static ability that respectively
#   mean "this can be attacked" and "When this becomes the target of an attack,
#   destroy this."
#
# 8.3.14a
#   An object with Spectra can be the target of an attack, even if it is not a
#   living object.[1.4.5a]
#
# 8.3.14b
#   When an object with Spectra becomes the target of an attack, a triggered-layer
#   is put on the stack. When the triggered-layer resolves, the object with Spectra
#   is destroyed. If there are no other legal attack-targets, the combat chain
#   closes.[7.7.2]

Feature: Section 8.3.14 - Spectra Ability Keyword
    As a game engine
    I need to correctly implement the Spectra ability keyword
    So that Spectra objects can be attacked and are destroyed when targeted

    # ===== Rule 8.3.14: Spectra is classified as an ability keyword =====

    Scenario: Spectra is classified as an ability keyword
        Given the engine's list of ability keywords
        When I check if "Spectra" is in the list of ability keywords
        Then "Spectra" is recognized as an ability keyword

    # ===== Rule 8.3.14a: A non-living object with Spectra can be attacked =====

    Scenario: A non-living object with Spectra can be the target of an attack
        Given a non-living object with the Spectra keyword
        When a player attempts to declare it as the target of an attack
        Then the non-living Spectra object is a legal attack target

    # ===== Rule 8.3.14a: A non-living object without Spectra cannot be attacked =====

    Scenario: A non-living object without Spectra cannot be the target of an attack
        Given a non-living object without the Spectra keyword
        When a player attempts to declare it as the target of an attack
        Then the non-living object is not a legal attack target

    # ===== Rule 8.3.14b: A triggered-layer is placed on the stack when Spectra is attacked =====

    Scenario: A triggered-layer is placed on the stack when a Spectra object becomes the target of an attack
        Given a non-living object with the Spectra keyword
        When the object becomes the target of an attack
        Then a triggered-layer is placed on the stack to destroy the Spectra object

    # ===== Rule 8.3.14b: Spectra object is destroyed when triggered-layer resolves =====

    Scenario: A Spectra object is destroyed when the triggered-layer resolves
        Given a non-living object with the Spectra keyword
        And the object has become the target of an attack
        When the triggered-layer resolves
        Then the Spectra object is destroyed

    # ===== Rule 8.3.14b: Combat chain closes when there are no other legal attack targets =====

    Scenario: Combat chain closes when Spectra object is destroyed and there are no other legal attack targets
        Given a non-living object with the Spectra keyword
        And there are no other legal attack targets
        When the Spectra object is destroyed by Spectra
        Then the combat chain closes

    # ===== Rule 8.3.14b: Combat chain does not close when there are other legal attack targets =====

    Scenario: Combat chain does not close when Spectra object is destroyed and there are other legal attack targets
        Given a non-living object with the Spectra keyword
        And there are other legal attack targets
        When the Spectra object is destroyed by Spectra
        Then the combat chain does not close
