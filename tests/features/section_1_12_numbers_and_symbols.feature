# Feature file for Section 1.12: Numbers and Symbols
# Reference: Flesh and Blood Comprehensive Rules Section 1.12
#
# Rule 1.12.1: Numbers are always integers.
# Rule 1.12.1a: If a rule or effect would calculate a fractional number and
#   does not specify to round up or down, the number is rounded towards zero.
#   (e.g., 3.5 rounds to 3, -3.5 rounds to -3)
# Rule 1.12.1b: If a rule or effect requires a player to choose a number, the
#   number selected must be a non-negative integer - zero and above. If it
#   requires the player to choose "up to" a number, the number selected must be
#   between zero and the specified number, inclusive.
#
# Rule 1.12.2: The letter X is used to represent a value that starts undefined
#   and is defined later by a rule or effect.
# Rule 1.12.2a: If an object has a property with the value X, and the value of
#   X is undefined, the object is still considered to have that property and the
#   value of X is evaluated to be zero.
# Rule 1.12.2b: If an object has a property with the value X, and the value of
#   X is defined, it remains defined until the object ceases to exist.
# Rule 1.12.2c: If there are two or more undefined values in the same context,
#   the letters Y and Z may also be used to represent those undefined values.
#
# Rule 1.12.3: The asterisk symbol (*) is used to represent a value that is
#   defined by a meta-static ability or continuous effect.
# Rule 1.12.3a: If * is undefined, the object is still considered to have that
#   property and the value of * is evaluated to be zero.
#   (Example: Mutated Mass outside a game has power/defense = 0)
# Rule 1.12.3b: If a meta-static ability can be used to define the value of *,
#   then it is evaluated according to the ability. Otherwise, if an effect
#   defines the value of *, it is evaluated according to the effect.
#   (Example: Arakni, Marionette + Agent of Chaos cards with * life)
#
# Rule 1.12.4: Symbols are typically used to represent the value of specified
#   properties.
# Rule 1.12.4a: The defense symbol is {d} and represents a defense value.
# Rule 1.12.4b: The intellect symbol is {i} and represents an intellect value.
# Rule 1.12.4c: The life symbol is {h} and represents a life value.
# Rule 1.12.4d: The power symbol is {p} and represents a power value. It is
#   also used to refer to physical damage.
# Rule 1.12.4e: The resource symbol is {r} and represents a resource value.
# Rule 1.12.4f: The chi symbol is {c} and represents a chi value.
# Rule 1.12.4g: The tap symbol is {t} and represents the tap effect.
# Rule 1.12.4h: The untap symbol is {u} and represents the untap effect.

Feature: Section 1.12 - Numbers and Symbols
    As a game engine
    I need to correctly handle numbers and symbols in Flesh and Blood
    So that numeric calculations, variable values, and symbols behave as per the rules

    # =====================================================================
    # Rule 1.12.1: Numbers are always integers
    # =====================================================================

    # Test for Rule 1.12.1a - Fractional numbers rounded toward zero (positive)
    Scenario: Positive fractional calculation rounded toward zero
        Given the game engine is initialized
        When an effect calculates the value 3.5
        Then the result is rounded to 3

    # Test for Rule 1.12.1a - Fractional numbers rounded toward zero (negative)
    Scenario: Negative fractional calculation rounded toward zero
        Given the game engine is initialized
        When an effect calculates the value -3.5
        Then the result is rounded to -3

    # Test for Rule 1.12.1a - Effect specifying "round up" overrides default
    Scenario: Effect specifying round up uses upward rounding
        Given the game engine is initialized
        When an effect calculates the value 2.5 and specifies to round up
        Then the result of the round-up calculation is 3

    # Test for Rule 1.12.1b - Player must choose a non-negative integer
    Scenario: Player choosing a number must choose non-negative integer
        Given the game engine is initialized
        And a player must choose a number for an effect
        When the player attempts to choose the value -1 from an open choice
        Then the open choice is rejected as invalid

    # Test for Rule 1.12.1b - Player can choose zero as their number
    Scenario: Player can choose zero as their number
        Given the game engine is initialized
        And a player must choose a number for an effect
        When the player attempts to choose the value 0 from an open choice
        Then the open choice is accepted as valid

    # Test for Rule 1.12.1b - Player can choose any positive integer
    Scenario: Player can choose any positive integer
        Given the game engine is initialized
        And a player must choose a number for an effect
        When the player attempts to choose the value 5 from an open choice
        Then the open choice is accepted as valid

    # Test for Rule 1.12.1b - "Up to N" constraint: zero is valid
    Scenario: Up to N allows choosing zero
        Given the game engine is initialized
        And a player must choose "up to" 3 for an effect
        When the player attempts to choose the value 0 from an up-to-3 range
        Then the up-to-3 choice is accepted as valid

    # Test for Rule 1.12.1b - "Up to N" constraint: maximum is valid
    Scenario: Up to N allows choosing the maximum
        Given the game engine is initialized
        And a player must choose "up to" 3 for an effect
        When the player attempts to choose the value 3 from an up-to-3 range
        Then the up-to-3 choice is accepted as valid

    # Test for Rule 1.12.1b - "Up to N" constraint: exceeding maximum is invalid
    Scenario: Up to N rejects exceeding the maximum
        Given the game engine is initialized
        And a player must choose "up to" 3 for an effect
        When the player attempts to choose the value 4 from an up-to-3 range
        Then the up-to-3 choice is rejected as invalid

    # =====================================================================
    # Rule 1.12.2: X is used to represent an undefined value
    # =====================================================================

    # Test for Rule 1.12.2 - Object with X property still has that property
    Scenario: Object with undefined X value still has that property
        Given the game engine is initialized
        And a card with variable power X is created
        And the X variable for that card is undefined
        Then the variable-power card is considered to have the power property
        And the variable-power card's power evaluates to 0

    # Test for Rule 1.12.2a - Undefined X evaluates to zero
    Scenario: Undefined X evaluates to zero when checking cost
        Given the game engine is initialized
        And a card with variable cost X is created
        When the cost X is evaluated while undefined
        Then the variable-cost card still has the cost property
        And the cost X value evaluates to 0

    # Test for Rule 1.12.2b - Once X is defined it remains defined until object ceases
    Scenario: Defined X value persists until the object ceases to exist
        Given the game engine is initialized
        And a card with variable power X is created
        When X is defined as 4 for the variable-power card
        Then the variable-power card's power evaluates to 4
        And the X value persists for the lifetime of the variable-power card

    # Test for Rule 1.12.2b - X value does not reset mid-game while object exists
    Scenario: X value does not change after being defined while object exists
        Given the game engine is initialized
        And a card with variable power X is created
        And X is pre-defined as 3 for the variable-power card
        When another effect would try to reset the X variable to undefined
        Then the variable-power card's power still evaluates to 3

    # Test for Rule 1.12.2c - Multiple undefined values use Y and Z
    Scenario: Two or more undefined values in same context use Y and Z
        Given the game engine is initialized
        And a context has two undefined values labeled X and Y
        Then X and Y represent distinct undefined values
        And X and Y each evaluate to 0 while undefined

    # =====================================================================
    # Rule 1.12.3: Asterisk (*) represents a value defined by meta-static ability
    # =====================================================================

    # Test for Rule 1.12.3 - Object with * property still has that property
    Scenario: Object with asterisk value still has that property
        Given the game engine is initialized
        And a card with asterisk power is created
        Then the asterisk-power card is considered to have the power property

    # Test for Rule 1.12.3a - Undefined * evaluates to zero (Mutated Mass outside game)
    Scenario: Undefined asterisk value evaluates to zero
        Given the game engine is initialized
        And a card with asterisk power is created
        And no meta-static ability or continuous effect defines the asterisk power
        Then the asterisk power evaluates to 0

    # Test for Rule 1.12.3a - Mutated Mass example: outside game * = zero
    Scenario: Mutated Mass power and defense outside game evaluate to zero
        Given the game engine is initialized
        And a Mutated Mass card with asterisk power and defense is created
        And no game context exists to define Mutated Mass's asterisk values
        Then Mutated Mass power evaluates to 0
        And Mutated Mass defense evaluates to 0

    # Test for Rule 1.12.3b - Meta-static ability defines * first
    Scenario: Meta-static ability takes priority over continuous effect for asterisk
        Given the game engine is initialized
        And a card with asterisk power is created
        And a meta-static ability defines the asterisk power as 5
        And a continuous effect also defines the asterisk power as 3
        Then the asterisk-power card's power evaluates to 5

    # Test for Rule 1.12.3b - Continuous effect defines * when no meta-static
    Scenario: Continuous effect defines asterisk when no meta-static ability applies
        Given the game engine is initialized
        And a card with asterisk power is created
        And no meta-static ability defines the asterisk power
        And a continuous effect defines the asterisk power as 4
        Then the asterisk-power card's power evaluates to 4

    # Test for Rule 1.12.3b - Arakni, Marionette example: become/copy defines *
    Scenario: Become copy effect defines asterisk as printed life of original
        Given the game engine is initialized
        And an Agent of Chaos card with asterisk life is created
        And a become-copy effect defines the life asterisk as the printed life of Arakni
        Then the Agent of Chaos card's life evaluates to Arakni's printed life

    # =====================================================================
    # Rule 1.12.4: Symbols represent property values
    # =====================================================================

    # Test for Rule 1.12.4a - {d} represents defense value
    Scenario: Defense symbol represents defense value
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "d"
        Then the symbol represents the property "defense"

    # Test for Rule 1.12.4b - {i} represents intellect value
    Scenario: Intellect symbol represents intellect value
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "i"
        Then the symbol represents the property "intellect"

    # Test for Rule 1.12.4c - {h} represents life value
    Scenario: Life symbol represents life value
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "h"
        Then the symbol represents the property "life"

    # Test for Rule 1.12.4d - {p} represents power value and physical damage
    Scenario: Power symbol represents power value
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "p"
        Then the symbol represents the property "power"
        And the symbol also refers to physical damage

    # Test for Rule 1.12.4e - {r} represents resource value
    Scenario: Resource symbol represents resource value
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "r"
        Then the symbol represents the property "resource"

    # Test for Rule 1.12.4f - {c} represents chi value
    Scenario: Chi symbol represents chi value
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "c"
        Then the symbol represents the property "chi"

    # Test for Rule 1.12.4g - {t} represents the tap effect
    Scenario: Tap symbol represents the tap effect
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "t"
        Then the symbol represents the "tap" effect

    # Test for Rule 1.12.4h - {u} represents the untap effect
    Scenario: Untap symbol represents the untap effect
        Given the game engine is initialized
        And the symbol registry is available
        When looking up the symbol "u"
        Then the symbol represents the "untap" effect
