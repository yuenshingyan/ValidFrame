import unittest
from datetime import datetime, date
from vrame._column_types_validation import (
    _validate_int,
    _validate_float,
    _validate_bool,
    _is_datetime,
    _validate_datetime,
    _validate_positive_int
)


class TestColumnTypesValidationFunctions(unittest.TestCase):
    """
    A test suite for validating column types in data processing.
    """

    def test_validate_int_pos(self):
        """
        Tests the positive case for integer validation.
        """
        _validate_int(1, "1")

    def test_validate_int_neg(self):
        """
        Tests the negative case for integer validation, expecting a ValueError.
        """
        with self.assertRaises(ValueError):
            _validate_int("1", "1")

    def test_validate_float_pos(self):
        """
        Tests the positive case for float validation.
        """
        _validate_float(1.0, "1.0")

    def test_validate_float_neg(self):
        """
        Tests the negative case for float validation, expecting a ValueError.
        """
        with self.assertRaises(ValueError):
            _validate_float("1.0", "1.0")

    def test_validate_bool_pos(self):
        """
        Tests the positive case for boolean validation.
        """
        _validate_bool(True, "True")

    def test_validate_bool_neg(self):
        """
        Tests the negative case for boolean validation, expecting a ValueError.
        """
        with self.assertRaises(ValueError):
            _validate_bool("True", "True")

    def test_is_datetime_pos(self):
        """
        Tests the positive case for datetime validation.
        """
        self.assertTrue(_is_datetime("2024-03-29"))

    def test_is_datetime_neg(self):
        """
        Tests the negative case for datetime validation.
        """
        self.assertFalse(_is_datetime("123456"))

    def test_validate_datetime_pos(self):
        """
        Tests the positive case for datetime validation with various formats.
        """
        _validate_datetime(datetime.now(), "_")
        _validate_datetime(date.today(), "_")
        _validate_datetime("2024-03-29", "_")

    def test_validate_datetime_neg(self):
        """
        Tests the negative case for datetime validation, expecting a
        ValueError.
        """
        _validate_datetime("123", "_")

    def test_validate_positive_int_pos(self):
        """
        Tests the positive case for positive integer validation.
        """
        _validate_positive_int(1, "1")

    def test_validate_positive_int_neg(self):
        """
        Tests the negative case for positive integer validation, expecting a
        ValueError.
        """
        _validate_positive_int(-1, "-1")


# Running the test
if __name__ == '__main__':
    unittest.main()
