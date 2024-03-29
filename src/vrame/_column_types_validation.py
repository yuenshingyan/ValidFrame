"""This module contains all functions for validating datatypes in module
`datatypes`."""

__all__ = [
    "_validate_int",
    "_validate_float",
    "_validate_bool",
    "_validate_datetime",
    "_validate_positive_int"
]
__version__ = "1.0.0"
__author__ = "Yuen Shing Yan Hindy"

from typing import Any
from dateutil.parser import parse
import datetime


def _validate_int(arg: Any, arg_str: str) -> None:
    """
    Validate if `arg` an instance of int.

    Parameters
    ----------
    arg : Any
        Variable that being validated.

    arg_str : str
        Variable's name in str.

    Raises
    ------
    ValueError
        If `arg` is not an instance of int.
    """
    if not isinstance(arg, int):
        raise ValueError(f"Argument '{arg_str}' must be int.")


def _validate_float(arg: Any, arg_str: str) -> None:
    """
    Validate if `arg` an instance of float.

    Parameters
    ----------
    arg : Any
        Variable that being validated.

    arg_str : str
        Variable's name in str.

    Raises
    ------
    ValueError
        If `arg` is not an instance of float.
    """
    if not isinstance(arg, float):
        raise ValueError(f"Argument '{arg_str}' must be float.")


def _validate_bool(arg: Any, arg_str: str) -> None:
    """
    Validate if `arg` an instance of bool.

    Parameters
    ----------
    arg : Any
        Variable that being validated.

    arg_str : str
        Variable's name in str.

    Raises
    ------
    ValueError
        If `arg` is not an instance of bool.
    """
    if not isinstance(arg, bool):
        raise ValueError(f"Argument '{arg_str}' must be bool.")


def _is_datetime(arg: Any) -> bool:
    """
    Validate if `arg` is datetime. Should only be called by function
    `_validate_datetime`.

    Parameters
    ----------
    arg : Any
        Variable that being validated.

    Raises
    ------
    ValueError
        If `arg` is not datetime.
    """
    try:
        parse(arg, fuzzy=False)
        return True
    except ValueError:
        return False


def _validate_datetime(arg: Any, arg_str: str) -> None:
    """
    Validate if `arg` an instance of datetime, date, time or if `arg` is
    actual datetime.

    Parameters
    ----------
    arg : Any
        Variable that being validated.

    arg_str : str
        Variable's name in str.

    Raises
    ------
    ValueError
        If arg` is not an instance of datetime, date, time or if `arg` is not
        actual datetime.
    """
    if (
            not isinstance(arg, datetime.datetime) and
            not isinstance(arg, datetime.date) and
            not isinstance(arg, datetime.time) and
            not _is_datetime(arg)
    ):
        raise ValueError(
            f"Argument '{arg_str}' must be datetime or datetime-like string.")


def _validate_positive_int(arg: Any, arg_str: str) -> None:
    """
    Validate if `arg` an instance of positive int.

    Parameters
    ----------
    arg : Any
        Variable that being validated.

    arg_str : str
        Variable's name in str.

    Raises
    ------
    ValueError
        If `arg` is not an instance of positive int.
    """
    if not isinstance(arg, int) and arg < 0:
        raise ValueError(f"Argument '{arg_str}' must be positive int.")
