"""This module contains all custom error for `Vrame`."""

__all__ = ["ParseError", "OutOfBoundError"]
__version__ = "1.0.2"
__author__ = "Yuen Shing Yan Hindy"


class ParseError(Exception):
    """
    Raised when any of the cell values cannot be parsed.
    """
    pass


class OutOfBoundError(Exception):
    """
    Raised when any of the cell values are higher or lower than the defined
    range. This error is applicable to both the upper and lower bounds and
    also the minimum and maximum number of items.
    """
    pass
