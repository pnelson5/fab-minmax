# Feature file for Section 8.3.36: Cloaked (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.36
#
# Rule 8.3.36: Cloaked is a static ability that means "Equip this face-down."
#
# Key aspects of Cloaked:
# - Cloaked is a STATIC ability
# - Cloaked means the card is equipped face-down (private) into its zone
# - Equipment zones (arms, chest, head, legs, weapon) are public zones by default (Rule 3.0.4a)
# - A card equipped face-down is a private object in a public zone (Rule 3.0.4c)
# - A private object's properties are not available to all players (Rule 3.0.3)
# - A card with Cloaked is equipped private; a card without Cloaked is equipped public by default
# - Turning a card face-down makes it private (Rule 8.5: Turn)

Feature: Section 8.3.36 - Cloaked Ability Keyword
    As a game engine
    I need to correctly implement the Cloaked ability keyword
    So that cards with Cloaked are equipped face-down (private) in their equipment zones

    # Rule 8.3.36: Cloaked is recognized as an ability keyword
    Scenario: Cloaked is recognized as an ability keyword
        Given a card with the Cloaked keyword
        When I inspect the card's keywords
        Then the card has the Cloaked keyword

    # Rule 8.3.36: Cloaked is a static ability
    Scenario: Cloaked is a static ability
        Given a card with the Cloaked keyword
        When I check the ability type of Cloaked
        Then Cloaked is a static ability

    # Rule 8.3.36: Cloaked ability meaning matches comprehensive rules text
    Scenario: Cloaked ability meaning matches comprehensive rules text
        Given a card with the Cloaked keyword
        When I inspect the Cloaked ability's meaning
        Then the Cloaked meaning is "Equip this face-down"

    # Rule 8.3.36: A card with Cloaked is equipped face-down (private)
    Scenario: A card with Cloaked is equipped face-down in an equipment zone
        Given an equipment card with the Cloaked keyword
        When the card is equipped to the player's equipment zone
        Then the equipped card is face-down
        And the equipped card is private

    # Rule 8.3.36: A card without Cloaked is equipped face-up (public) by default
    Scenario: A card without Cloaked is equipped face-up in an equipment zone
        Given an equipment card without the Cloaked keyword
        When the card is equipped to the player's equipment zone
        Then the equipped card is face-up
        And the equipped card is public

    # Rule 8.3.36: A Cloaked card in a public equipment zone remains private
    # (Public zones can contain private objects per Rule 3.0.4c)
    Scenario: A Cloaked card in a public equipment zone is a private object in a public zone
        Given an equipment card with the Cloaked keyword
        When the card is equipped to the player's equipment zone
        Then the equipment zone is a public zone
        And the equipped Cloaked card is private within that public zone

    # Rule 8.3.36: Cloaked causes the card to be private on equip
    # (distinct from being in a private zone — this is a private object in a public zone)
    Scenario: Cloaked card properties are hidden from opponents when equipped
        Given an equipment card with the Cloaked keyword
        And a second player as the opponent
        When the card is equipped to the player's equipment zone
        Then the opponent cannot determine the properties of the equipped card
