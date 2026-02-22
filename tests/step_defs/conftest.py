"""
Configuration for pytest-bdd tests.

This file ensures that pytest-bdd can find and execute the feature files
and step definitions for the Flesh and Blood Comprehensive Rules tests.
"""

import pytest
from pytest_bdd import given, when, then


# Configure pytest-bdd to look for feature files in the correct location
def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    """
    Custom error handler for better debugging of BDD test failures.

    This helps identify which rule from the comprehensive rules is failing.
    """
    print(f"\nFailed step in scenario: {scenario.name}")
    print(f"Feature: {feature.name}")
    print(f"Step: {step.name}")
    print(f"Error: {exception}")
