"""Blueprints package for ex18.

This file makes the `blueprints` directory a proper Python package so imports
like `from blueprints.login import login` work reliably.
"""

__all__ = ["login", "sensors", "actuators"]
