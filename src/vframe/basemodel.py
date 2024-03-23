"""This module contains `BaseModel`."""

__all__ = ["BaseModel"]
__version__ = "alpha"
__author__ = "Yuen Shing Yan Hindy"

from datetime import datetime
import pandas as pd
from src.vframe.column_types import (
    Integer,
    Float,
    Boolean,
    Datetime,
    String,
    List,
    Tuple,
    Dictionary,
    Set, 
    Object
)
from src.vframe._column_validation import (
    _try_eval,
    _vec_isinstance,
    _vec_isnumeric,
    vec_is_datetime,
    _vec_len
)
from src.vframe.error import ParseError, OutOfBoundError
from joblib import Parallel, delayed


Fields = (Integer | Float | Boolean | Datetime | String | List | Tuple | 
          Dictionary | Set | Object)


class BaseModel:
    """
    Base model class for handling data frames.

    This class provides a foundation for models that operate on pandas
    DataFrames. It ensures that the input frame is a pandas DataFrame and
    initializes a dictionary to store field types.

    Parameters
    ----------
    frame : pd.DataFrame
        The pandas DataFrame to be used by the model.

    Raises
    ------
    ValueError
        If the input frame is not a pandas DataFrame.

    Attributes
    ----------
    frame : pd.DataFrame
        The pandas DataFrame used by the model.
    field_type : dict
        A dictionary mapping field names to their types, excluding special
        methods.
    """
    def __init__(self, frame: pd.DataFrame, n_jobs: int) -> None:
        if not isinstance(frame, pd.DataFrame):
            raise ValueError("Argument 'frame' must be 'pd.DataFrame'.")

        self.frame = frame
        self.field_type = {k: v for k, v in self.__class__.__dict__.items()
                           if not k.startswith('__')}
        self.n_jobs = n_jobs

    @staticmethod
    def _check_null(field: Fields, column: pd.Series, name: str):
        """
        Check if a column contains null values and if it's not supposed to.

        This method raises a ValueError if the column specified by `name`
        contains null values and the corresponding field is not nullable.

        Parameters
        ----------
        field : Fields
            The field object that describes the column.
        column : pd.Series
            The pandas Series representing the column to check.
        name : str
            The name of the column to check.

        Raises
        ------
        ValueError
            If the column contains null values and the field is not nullable.
        """
        if (
                not field.nullable and
                pd.isnull(column).sum() > 0
        ):
            raise ValueError(f"Null values found in column '{name}'.")

    @staticmethod
    def _parse(field: Fields, column: pd.Series, name: str) -> pd.Series:
        """
        Parse and convert a pandas Series according to the specified field
        type.

        This method attempts to parse and convert the values in a pandas
        Series based on the type of the field provided. It supports various
        field types including Integer, Float, Boolean, List, Tuple,
        Dictionary, Set, Datetime, and String. The conversion is done using
        the `_try_eval` function for complex types and built-in pandas
        functions for simpler types like Datetime and String.

        Parameters
        ----------
        field : Fields
            The field type to which the column values should be converted.
        column : pd.Series
            The pandas Series containing the values to be parsed and converted.
        name : str
            The name of the column being parsed. Used in error messages.

        Returns
        -------
        pd.Series
            The parsed and converted pandas Series.

        Raises
        ------
        ParseError
            If not all values in the column can be parsed into the specified
            field type.
        """
        try:
            if (
                    isinstance(field, Integer) or
                    isinstance(field, Float) or
                    isinstance(field, Boolean) or
                    isinstance(field, List)
            ):
                column = column.apply(_try_eval)
            elif (
                    isinstance(field, Tuple) or
                    isinstance(field, Dictionary) or
                    isinstance(field, Set)
            ):
                column = column.apply(_try_eval)
            elif isinstance(field, Datetime):
                column = pd.to_datetime(column)
            elif isinstance(field, String):
                column = column.astype(str)
        except (NameError, pd.errors.UndefinedVariableError):
            raise ParseError(f"Not all values in column '{name}' can be "
                             f"parsed into {name}.")

        return column

    @staticmethod
    def _check_definition(field: Fields, column: pd.Series, name: str):
        """
        Check if the values in a column match the expected data type defined
        by a field.

        This method raises a TypeError if the values in the specified column
        do not match the expected data type defined by the field. The field
        can be of various types such as Integer, Float, Boolean, Datetime,
        List, Tuple, Dictionary, or Set. The method checks the type of each
        value in the column against the expected type defined by the field.

        Parameters
        ----------
        field : Fields
            The field object defining the expected data type.
        column : pd.Series
            The pandas Series containing the values to be checked.
        name : str
            The name of the column being checked.

        Raises
        ------
        TypeError
            If the values in the column do not match the expected data type
            defined by the field.
        """
        if (
                isinstance(field, Integer) and
                not _vec_isinstance(column, int) and
                field.allow_float
        ):
            raise TypeError(f"Not all values in column '{name}' are integer.")

        if (
                isinstance(field, Float) and
                not _vec_isinstance(column, float) and
                field.allow_int
        ):
            raise TypeError(f"Not all values in column '{name}' are float.")

        if isinstance(field, Boolean) and not _vec_isinstance(column, bool):
            raise TypeError(f"Not all values in column '{name}' are boolean.")

        if (
                isinstance(field, Datetime) and
                not _vec_isinstance(column, datetime)
        ):
            raise TypeError(f"Not all values in column '{name}' are datetime.")

        if isinstance(field, List) and not _vec_isinstance(column, list):
            raise TypeError(f"Not all values in column '{name}' are list.")

        if isinstance(field, Tuple) and not _vec_isinstance(column, tuple):
            raise TypeError(f"Not all values in column '{name}' are tuple.")

        if isinstance(field, Dictionary) and not _vec_isinstance(column, dict):
            raise TypeError(f"Not all values in column '{name}' are dict.")

        if isinstance(field, Set) and not _vec_isinstance(column, set):
            raise TypeError(f"Not all values in column '{name}' are set.")

    @staticmethod
    def _check_range(field: Fields, column: pd.Series, name: str):
        """
        Check if the values in a column are within the specified range for a
        given field type.

        This method validates that the values in a pandas Series column are
        within the specified range for the given field type. It supports
        Integer, Float, and Datetime field types. For Integer and Float
        fields, it checks if the minimum and maximum values in the column
        are within the specified lower and upper bounds. For Datetime
        fields, it checks if all values in the column are datetime objects.

        Parameters
        ----------
        field : Fields
            The field type to validate against. Must be an instance of
            Integer, Float, or Datetime.
        column : pd.Series
            The pandas Series column to validate.
        name : str
            The name of the column being validated.

        Raises
        ------
        TypeError
            If the values in the column are not numeric for Integer or Float
            fields, or if the values are not datetime objects for Datetime
            fields.
        OutOfBoundError
            If the minimum or maximum value in the column exceeds the
            specified lower or upper bound for Integer or Float fields.
        """
        if (
                isinstance(field, Integer) or
                isinstance(field, Float)
        ):
            if not _vec_isnumeric(column):
                raise TypeError(
                    f"Not all values in column '{name}' are numeric."
                )
            else:
                column_min = column.min(skipna=field.skipna)
                column_max = column.max(skipna=field.skipna)
                is_ge_lower = column_min >= field.lower
                is_le_upper = column_max <= field.upper

                if not is_ge_lower:
                    raise OutOfBoundError(
                        f"Minimum value in {name} exceeded lower "
                        f"bound. Lower bound is {field.lower}, min value in "
                        f"column {name} is {column_min}")

                if not is_le_upper:
                    raise OutOfBoundError(
                        f"Maximum value in column {name} exceeded upper "
                        f"bound. Upper bound is {field.upper}, max value in "
                        f"column {name} is {column_max}")
        elif isinstance(field, Datetime) and not vec_is_datetime(column):
            raise TypeError(f"Not all values in column {name} are datetime.")

    @staticmethod
    def _check_items(field: Fields, column: pd.Series):
        """
        Validate the items in a column against specified bounds.

        This function checks if the items in the provided column exceed the
        specified bounds
        defined by the `field` parameter. It supports validation for iterables
        (List, Tuple, Set, Dictionary) and strings (String). For iterables, it
        checks if the number of items is within the specified minimum and
        maximum bounds. For strings, it checks if the length of the string is
        within the specified minimum and maximum lengths.

        Parameters
        ----------
        field : Fields
            The field object defining the bounds for validation. It can be an
            instance of List, Tuple,
            Set, Dictionary, or String.
        column : pd.Series
            The pandas Series containing the items to be validated.

        Raises
        ------
        OutOfBoundError
            If the items in the column do not meet the specified bounds
            defined by the `field` parameter.
        """
        if (
                isinstance(field, List) or
                isinstance(field, Tuple) or
                isinstance(field, Set) or
                isinstance(field, Dictionary)
        ):
            is_ge_min_items = all(_vec_len(column) >= field.min_items)
            is_le_max_items = all(_vec_len(column) <= field.max_items)

            if not is_ge_min_items:
                raise OutOfBoundError(
                    f"Number of items in cells less than the lower bound "
                    f"of {field.min_items}."
                )

            if not is_le_max_items:
                raise OutOfBoundError(
                    f"Number of items in cells more than the upper bound "
                    f"of {field.max_items}.")
        elif isinstance(field, String):
            is_ge_min_len = all(column.str.len() >= field.min_length)
            is_le_max_len = all(column.str.len() <= field.max_length)

            if not is_ge_min_len:
                raise OutOfBoundError(
                    f"String in cells shorter than minimum length of "
                    f"{field.min_length}."
                )

            if not is_le_max_len:
                raise OutOfBoundError(
                    f"String in cells longer than maximum length of "
                    f"{field.max_length}."
                )

    def _validate(self, field: Fields, name: str) -> pd.Series:
        column = self.frame.loc[:, name]
        self._check_null(field, column, name)
        column = self._parse(field, column, name)
        self._check_definition(field, column, name)
        self._check_definition(field, column, name)

        return column

    def validate(self) -> pd.DataFrame:
        """
        Validate and process each field in the DataFrame according to its type.

        This method iterates over each field defined in `self.field_type`,
        checks for null values, parses the field according to its type,
        and checks if the field meets its definition. The processed column
        is then updated in the DataFrame.

        Returns
        -------
        pd.DataFrame
            The DataFrame with all fields validated and processed.

        Notes
        -----
        The method assumes that `self.field_type` is a dictionary mapping
        field names to their types, and `self.frame` is a pandas DataFrame
        containing the data to be validated.

        The `_check_null`, `_parse`, and `_check_definition` methods are
        assumed to be implemented in the same class and are used to perform
        specific validation and processing tasks on each field.
        """
        columns = Parallel(
            n_jobs=self.n_jobs
        )(
            delayed(
                self._validate
            )(field, name) for name, field in self.field_type.items()
        )
        return pd.concat(columns, axis=1)
