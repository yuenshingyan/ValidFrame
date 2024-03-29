"""This module contains all datatypes for `Vrame`."""

__all__ = [
    "Integer",
    "Float",
    "Boolean",
    "Datetime",
    "String",
    "List",
    "Tuple",
    "Set",
    "Dictionary",
    "Object"
]
__version__ = "1.0.1"
__author__ = "Yuen Shing Yan Hindy"


from datetime import datetime
import numpy as np
from src.vrame._column_types_validation import (
    _validate_int,
    _validate_float,
    _validate_bool,
    _validate_datetime,
    _validate_positive_int
)


class Integer:
    """
    Represents an integer with specified bounds and properties.

    This class is used to define an integer with a lower and upper bound,
    and additional properties such as nullability, skipping of NA values, and
    allowing float values.

    Parameters
    ----------
    lower : int, optional
        The lower bound of the integer. Default is negative infinity.
    upper : int, optional
        The upper bound of the integer. Default is positive infinity.
    nullable : bool, optional
        Whether the integer can be null. Default is True.
    skipna : bool, optional
        Whether to skip NA values. Default is True.
    allow_float : bool, optional
        Whether to allow float values. Default is False.

    Attributes
    ----------
    lower : int
        The lower bound of the integer.
    upper : int
        The upper bound of the integer.
    nullable : bool
        Whether the integer can be null.
    skipna : bool
        Whether to skip NA values.
    allow_float : bool
        Whether to allow float values.

    Methods
    -------
    __repr__()
        Returns a string representation of the Integer instance.

    Examples
    --------
    >>> int_instance = Integer(lower=0, upper=10, nullable=False)
    >>> print(int_instance)
    Integer(lower=0, upper=10, nullable=False)
    """

    def __init__(self, lower: int = -np.inf, upper: int = np.inf, 
                 nullable: bool = True, skipna: bool = True,
                 allow_float: bool = False) -> None:
        _validate_int(lower, "lower")
        _validate_int(upper, "upper")
        _validate_bool(nullable, "nullable")

        self.lower = lower
        self.upper = upper
        self.nullable = nullable
        self.skipna = skipna
        self.allow_float = allow_float

    def __repr__(self):
        """
        Returns a string representation of `Integer`.

        Returns
        -------
        str
            A string representation of `Integer`, including its attributes.
        """

        return (f"Integer(lower={self.lower}, upper={self.upper}, "
                f"nullable={self.nullable}, skipna={self.skipna}, "
                f"allow_float={self.allow_float})")


class Float:
    """
    A class representing a float with validation and constraints.

    This class is designed to encapsulate a float value with additional
    constraints such as lower and upper bounds, nullability, and integer
    allowance. It provides a way to validate these constraints upon
    initialization.

    Attributes
    ----------
    lower : float
        The lower bound for the float value. Default is negative infinity.
    upper : float
        The upper bound for the float value. Default is positive infinity.
    nullable : bool
        Indicates whether the float value can be null. Default is True.
    skipna : bool
        Indicates whether to skip null values. Default is True.
    allow_int : bool
        Indicates whether integer values are allowed. Default is False.

    Methods
    -------
    __repr__()
        Returns a string representation of the Float object.

    Examples
    --------
    >>> f = Float(lower=0, upper=10, nullable=False, skipna=True,
    >>> allow_int=True)
    >>> print(f)
    Float(lower=0, upper=10, nullable=False)
    """

    def __init__(self, lower: float = -np.inf, upper: float = np.inf,
                 nullable: bool = True, skipna: bool = True,
                 allow_int: bool = False) -> None:
        _validate_float(lower, "lower")
        _validate_float(upper, "upper")
        _validate_bool(nullable, "nullable")

        self.lower = lower
        self.upper = upper
        self.nullable = nullable
        self.skipna = skipna
        self.allow_int = allow_int

    def __repr__(self):
        """
        Returns a string representation of `Float`.

        Returns
        -------
        str
            A string representation of `Float`, including its attributes.
        """

        return (f"Float(lower={self.lower}, upper={self.upper}, "
                f"nullable={self.nullable}, skipna={self.skipna}, "
                f"allow_int={self.allow_int})")
    
    
class Boolean:
    """
    A class representing a boolean data type with configurable nullability
    and skipna behavior.

    Attributes
    ----------
    nullable : bool
        Indicates whether the boolean can be null. Default is True.
    skipna : bool
        Indicates whether to skip NA/null values. Default is True.

    Parameters
    ----------
    nullable : bool, optional
        Specifies if the boolean can be null. Default is True.
    skipna : bool, optional
        Specifies if NA/null values should be skipped. Default is True.

    Methods
    -------
    __repr__()
        Returns a string representation of the Boolean instance.

    Examples
    --------
    >>> bool_instance = Boolean(nullable=False, skipna=False)
    >>> print(bool_instance)
    Boolean(nullable=False)
    """

    def __init__(self, nullable: bool = True, skipna: bool = True) -> None:
        _validate_bool(nullable, "nullable")

        self.nullable = nullable
        self.skipna = skipna

    def __repr__(self):
        """
        Returns a string representation of `Boolean`.

        Returns
        -------
        str
            A string representation of `Boolean`, including its nullability.
        """

        return f"Boolean(nullable={self.nullable}, skipna={self.skipna})"

    
class String:
    """
    A class representing a string with specified minimum and maximum length,
    and optional nullability.

    Parameters
    ----------
    min_length : int
        The minimum length of the string.
    max_length : int
        The maximum length of the string.
    nullable : bool, optional
        Whether the string can be null, by default True.
    skipna : bool, optional
        Whether to skip null values, by default True.

    Attributes
    ----------
    min_length : int
        The minimum length of the string.
    max_length : int
        The maximum length of the string.
    nullable : bool
        Whether the string can be null.
    skipna : bool
        Whether to skip null values.

    Methods
    -------
    __repr__()
        Returns a string representation of the String object.

    Examples
    --------
    >>> s = String(min_length=1, max_length=10, nullable=True, skipna=True)
    >>> print(s)
    String(min_length=1, max_length=10, nullable=True)
    """

    def __init__(self, min_length: int, max_length: int, nullable: bool = True,
                 skipna: bool = True) -> None:
        _validate_positive_int(min_length, "min_length")
        _validate_positive_int(max_length, "max_length")
        _validate_bool(nullable, "nullable")

        self.min_length = min_length
        self.max_length = max_length
        self.nullable = nullable
        self.skipna = skipna

    def __repr__(self):
        """
        Returns a string representation of `String`.

        Returns
        -------
        str
            A string representation of `String`, including its nullability.
        """

        return (f"String(min_length={self.min_length}, "
                f"max_length={self.max_length}, nullable={self.nullable}, "
                f"skipna={self.skipna})")


class Datetime:
    """
    A class to represent a datetime range with validation and optional
    nullability.

    Parameters
    ----------
    lower : datetime | str
        The lower bound of the datetime range. Can be a datetime object or a
        string.
    upper : datetime | str
        The upper bound of the datetime range. Can be a datetime object or a
        string.
    nullable : bool, optional
        Indicates whether the datetime range can include null values, by
        default True.
    skipna : bool, optional
        Indicates whether to skip null values in the datetime range, by
        default True.

    Attributes
    ----------
    lower : datetime | str
        The lower bound of the datetime range.
    upper : datetime | str
        The upper bound of the datetime range.
    nullable : bool
        Indicates whether the datetime range can include null values.
    skipna : bool
        Indicates whether to skip null values in the datetime range.

    Methods
    -------
    __repr__()
        Returns a string representation of the Datetime object.

    Notes
    -----
    The class validates the datetime inputs and nullable/skipna flags upon
    initialization.
    """

    def __init__(self, lower: datetime | str, upper: datetime | str,
                 nullable: bool = True, skipna: bool = True,
                 yearfirst: bool = False) -> None:
        _validate_datetime(lower, "lower")
        _validate_datetime(upper, "upper")
        _validate_bool(nullable, "nullable")

        self.lower = lower
        self.upper = upper
        self.nullable = nullable
        self.skipna = skipna
        self.yearfirst = yearfirst

    def __repr__(self):
        """
        Returns a string representation of `Datetime`.

        Returns
        -------
        str
            A string representation of `Datetime`, including its nullability.
        """

        return (f"Datetime(lower={self.lower}, upper={self.upper}, "
                f"nullable={self.nullable}, skipna={self.skipna}, "
                f"yearfirst={self.yearfirst})")


class List:
    """
    A class representing a list with configurable properties.

    Attributes
    ----------
    nullable : bool
        Indicates whether the list can contain null values. Default is True.
    min_items : int
        The minimum number of items the list can contain. Default is 0.
    max_items : int
        The maximum number of items the list can contain. Default is infinity.
    skipna : bool
        Indicates whether to skip null values when processing the list.
        Default is True.

    Parameters
    ----------
    nullable : bool, optional
        Specifies if the list can contain null values. Default is True.
    min_items : int, optional
        Specifies the minimum number of items the list can contain. Default
        is 0.
    max_items : int, optional
        Specifies the maximum number of items the list can contain. Default
        is infinity.
    skipna : bool, optional
        Specifies if null values should be skipped when processing the list.
        Default is True.

    Methods
    -------
    __repr__()
        Returns a string representation of the List object.

    Examples
    --------
    >>> list_instance = List(nullable=False, min_items=1, max_items=5,
    >>> skipna=False)
    >>> print(list_instance)
    List(nullable=False)
    """

    def __init__(self, min_items: int = 0, max_items: int = np.inf,
                 nullable: bool = True, skipna: bool = True) -> None:
        _validate_bool(nullable, "nullable")
        _validate_positive_int(min_items, "min_items")
        _validate_positive_int(max_items, "max_items")

        self.min_items = min_items
        self.max_items = max_items
        self.nullable = nullable
        self.skipna = skipna

    def __repr__(self):
        """
        Returns a string representation of `List`.

        Returns
        -------
        str
            A string representation of `List`, including its nullability.
        """

        return (f"List(min_items={self.min_items}, max_items={self.max_items},"
                f" nullable={self.nullable}, skipna={self.skipna})")


class Tuple:
    """
    A class representing a tuple with configurable properties.

    Parameters
    ----------
    nullable : bool, optional
        Indicates whether the tuple can contain null values, by default True.
    min_items : int, optional
        The minimum number of items the tuple must contain, by default 0.
    max_items : int, optional
        The maximum number of items the tuple can contain, by default np.inf.
    skipna : bool, optional
        Indicates whether to skip null values when processing the tuple, by
        default True.

    Attributes
    ----------
    nullable : bool
        Indicates whether the tuple can contain null values.
    min_items : int
        The minimum number of items the tuple must contain.
    max_items : int
        The maximum number of items the tuple can contain.
    skipna : bool
        Indicates whether to skip null values when processing the tuple.

    Methods
    -------
    __repr__()
        Returns a string representation of the Tuple object.

    Examples
    --------
    >>> t = Tuple(nullable=False, min_items=2, max_items=5, skipna=False)
    >>> print(t)
    Tuple(nullable=False)
    """

    def __init__(self, min_items: int = 0, max_items: int = np.inf,
                 nullable: bool = True,  skipna: bool = True) -> None:
        _validate_bool(nullable, "nullable")
        _validate_positive_int(min_items, "min_items")
        _validate_positive_int(max_items, "max_items")

        self.min_items = min_items
        self.max_items = max_items
        self.nullable = nullable
        self.skipna = skipna

    def __repr__(self):
        """
        Returns a string representation of `Tuple`.

        Returns
        -------
        str
            A string representation of `Tuple`, including its nullability.
        """

        return (f"Tuple(min_items={self.min_items}, "
                f"max_items={self.max_items}, nullable={self.nullable}, "
                f"skipna={self.skipna})")


class Set:
    """
    A class representing a set with configurable properties.

    Parameters
    ----------
    nullable : bool, optional
        Indicates whether the set can contain null values, by default True.
    min_items : int, optional
        The minimum number of items the set must contain, by default 0.
    max_items : int, optional
        The maximum number of items the set can contain, by default np.inf.
    skipna : bool, optional
        Indicates whether to skip null values, by default True.

    Attributes
    ----------
    nullable : bool
        Indicates whether the set can contain null values.
    min_items : int
        The minimum number of items the set must contain.
    max_items : int
        The maximum number of items the set can contain.
    skipna : bool
        Indicates whether to skip null values.

    Methods
    -------
    __repr__()
        Returns a string representation of the Set object.
    """

    def __init__(self, min_items: int = 0, max_items: int = np.inf,
                 nullable: bool = True,  skipna: bool = True) -> None:
        _validate_bool(nullable, "nullable")
        _validate_positive_int(min_items, "min_items")
        _validate_positive_int(max_items, "max_items")

        self.min_items = min_items
        self.max_items = max_items
        self.nullable = nullable
        self.skipna = skipna

    def __repr__(self):
        """
        Returns a string representation of `Set`.

        Returns
        -------
        str
            A string representation of `Set`, including its nullability.
        """

        return (f"Set(min_items={self.min_items}, max_items={self.max_items}, "
                f"nullable={self.nullable}, skipna={self.skipna})")

    
class Dictionary:
    """
    A class representing a dictionary with configurable properties.

    Parameters
    ----------
    nullable : bool, optional
        Indicates whether the dictionary can contain null values. Default is
        True.
    min_items : int, optional
        The minimum number of items the dictionary must contain. Default is 0.
    max_items : int, optional
        The maximum number of items the dictionary can contain. Default is
        infinity.
    skipna : bool, optional
        Indicates whether to skip null values when processing the dictionary.
        Default is True.

    Attributes
    ----------
    nullable : bool
        Indicates whether the dictionary can contain null values.
    min_items : int
        The minimum number of items the dictionary must contain.
    max_items : int
        The maximum number of items the dictionary can contain.
    skipna : bool
        Indicates whether to skip null values when processing the dictionary.

    Methods
    -------
    __repr__()
        Returns a string representation of the dictionary.

    Examples
    --------
    >>> d = Dictionary(nullable=False, min_items=1, max_items=5, skipna=False)
    >>> print(d)
    Dictionary(nullable=False)
    """

    def __init__(self, min_items: int = 0, max_items: int = np.inf,
                 nullable: bool = True,  skipna: bool = True) -> None:
        _validate_bool(nullable, "nullable")
        _validate_positive_int(min_items, "min_items")
        _validate_positive_int(max_items, "max_items")

        self.min_items = min_items
        self.max_items = max_items
        self.nullable = nullable
        self.skipna = skipna

    def __repr__(self):
        """
        Returns a string representation of `Dictionary`.

        Returns
        -------
        str
            A string representation of `Dictionary`, including its nullability.
        """

        return (f"Dictionary(min_items={self.min_items}, "
                f"max_items={self.max_items}, nullable={self.nullable}, "
                f"skipna={self.skipna})")


class Object:
    """
    A class representing an object with configurable nullability and skipping
    of NA values.

    Parameters
    ----------
    nullable : bool, optional
        Whether the object can be nullable, by default True.
    skipna : bool, optional
        Whether to skip NA values, by default True.

    Attributes
    ----------
    nullable : bool
        Indicates if the object can be nullable.
    skipna : bool
        Indicates if NA values should be skipped.

    Methods
    -------
    __repr__()
        Returns a string representation of the object.
    """

    def __init__(self, nullable: bool = True, skipna: bool = True) -> None:
        _validate_bool(nullable, "nullable")

        self.nullable = nullable
        self.skipna = skipna

    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns
        -------
        str
            A string representation of the object, including its nullability.
        """

        return f"Object(nullable={self.nullable}, skipna={self.skipna})"
