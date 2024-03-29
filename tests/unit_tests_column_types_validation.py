import unittest
from datetime import datetime, date
from src.vrame._column_types_validation import (
    _validate_int,
    _validate_float,
    _validate_bool,
    _is_datetime,
    _validate_datetime,
    _validate_positive_int
)


class TestColumnTypesValidationFunctions(unittest.TestCase):
    def test_validate_int_pos(self):
        _validate_int(1, "1")

    def test_validate_int_neg(self):
        with self.assertRaises(ValueError):
            _validate_int("1", "1")

    def test_validate_float_pos(self):
        _validate_float(1.0, "1.0")

    def test_validate_float_neg(self):
        with self.assertRaises(ValueError):
            _validate_float("1.0", "1.0")

    def test_validate_bool_pos(self):
        _validate_bool(True, "True")

    def test_validate_bool_neg(self):
        with self.assertRaises(ValueError):
            _validate_bool("True", "True")

    def test_is_datetime_pos(self):
        self.assertTrue(_is_datetime("2024-03-29"))

    def test_is_datetime_neg(self):
        self.assertFalse(_is_datetime("123456"))

    def test_validate_datetime_pos(self):
        _validate_datetime(datetime.now(), "_")
        _validate_datetime(date.today(), "_")
        _validate_datetime("2024-03-29", "_")

    def test_validate_datetime_neg(self):
        _validate_datetime("123", "_")

    def test_validate_positive_int_pos(self):
        _validate_positive_int(1, "1")

    def test_validate_positive_int_neg(self):
        _validate_positive_int(-1, "-1")


# Running the test
if __name__ == '__main__':
    unittest.main()
