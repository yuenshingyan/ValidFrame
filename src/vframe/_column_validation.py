"""This module contains functions for validating columns."""

__all__ = [
    "_try_eval",
    "_vec_isinstance",
    "_vec_isnumeric",
    "vec_is_datetime",
    "_vec_len"
]
__version__ = "alpha"
__author__ = "Yuen Shing Yan Hindy"


from datetime import datetime
import numpy as np
from typing import Iterable, Any


def _try_eval(arg: Any) -> Any:
    """
    Try to eval and returns `arg`. Should only being called with pd.Series
    `.apply` method.

    Parameters
    ----------
    arg: Any
        Cell values being parsed.

    Returns
    -------
    Any
        Parsed cell values.

    Raises
    ------
    TypeError
        If cell values are not str.
    """
    try:
        return eval(arg)
    except TypeError:
        return arg


def _vec_isinstance(arg: Iterable, dtype: Any) -> bool:
    """
    Validates if all cell values are the same datatype.

    Parameters
    ----------
    arg: Iterable
        Cell values that being validated.

    dtype: Any
        Datatype that being validated.

    Returns
    -------
    bool
        True, if all cell values are the same datatype.
        False, if all cell values are not the same datatype.
    """
    is_dtype = np.vectorize(isinstance)(arg, dtype)

    return (is_dtype > 0).sum() == len(is_dtype)


def _vec_isnumeric(arg: Iterable) -> bool:
    """
    Validates if all cell values are numeric.

    Parameters
    ----------
    arg: Iterable
        Cell values that being validated.

    Returns
    -------
    bool
        True, if all cell values are numeric.
        False, if all cell values are not numeric.
    """
    is_int = np.vectorize(isinstance)(arg, int)
    is_float = np.vectorize(isinstance)(arg, float)
    is_numeric = (is_int + is_float) > 0

    return is_numeric.sum() == len(is_numeric)


def vec_is_datetime(arg: Iterable) -> bool:
    """
    Validates if all cell values are datetime.

    Parameters
    ----------
    arg: Iterable
        Cell values that being validated.

    Returns
    -------
    bool
        True, if all cell values are datetime.
        False, if all cell values are not datetime.
    """
    is_datetime = np.vectorize(isinstance)(arg, datetime)

    return is_datetime.sum() == len(is_datetime)


def _vec_len(arg: Iterable) -> np.ndarray:
    """
    Returns the length of the cell values.

    Parameters
    ----------
    arg: Iterable
        Cell values that being checked for their length.

    Returns
    -------
    int
        Length of the cell values.
    """
    return np.vectorize(len)(arg)
