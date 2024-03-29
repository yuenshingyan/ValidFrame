import unittest
from datetime import datetime

import pandas as pd
import numpy as np

from src.vrame._column_validation import (
    _try_eval,
    _vec_isinstance,
    _vec_isnumeric,
    _vec_is_datetime,
    _vec_len,
)


class TestColumnValidationFunctions(unittest.TestCase):
    def test_try_eval_pos(self):
        self.assertEqual(_try_eval("1"), 1)
        self.assertEqual(_try_eval("1.0"), 1.0)
        self.assertEqual(_try_eval("[1]"), [1])
        self.assertEqual(_try_eval("(1)"), (1))
        self.assertEqual(_try_eval("{1}"), {1})
        self.assertEqual(_try_eval("{'k': 1}"), {'k': 1})

    def test_try_eval_neg(self):
        self.assertEqual(_try_eval(1), 1)
        self.assertEqual(_try_eval(1.0), 1.0)
        self.assertEqual(_try_eval([1]), [1])
        self.assertEqual(_try_eval((1)), (1))
        self.assertEqual(_try_eval({1}), {1})
        self.assertEqual(_try_eval({'k': 1}), {'k': 1})

    def test_vec_isinstance_pos(self):
        int_list = pd.Series((1, 2, 3))
        float_list = pd.Series([1.0, 2.0, 3.0])
        str_list = pd.Series(["1", "2", "3"])
        tuple_list = pd.Series([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
        list_list = pd.Series([[1], [2], [3]])
        set_list = pd.Series([{1}, {2}, {3}])
        dict_list = pd.Series([{"k1": 1}, {"k2": 2}, {"k3": 3}])

        self.assertTrue(_vec_isinstance(int_list, int))
        self.assertTrue(_vec_isinstance(float_list, float))
        self.assertTrue(_vec_isinstance(str_list, str))
        self.assertTrue(_vec_isinstance(tuple_list, tuple))
        self.assertTrue(_vec_isinstance(list_list, list))
        self.assertTrue(_vec_isinstance(set_list, set))
        self.assertTrue(_vec_isinstance(dict_list, dict))

    def test_vec_isinstance_neg(self):
        int_list = pd.Series((1, 2.0, "3"))
        float_list = pd.Series([1.0, 2, "3.0"])
        str_list = pd.Series(["1", 2.0, 3])
        tuple_list = pd.Series([(1, 2, 3), "(4, 5, 6)", [7, 8, 9]])
        list_list = pd.Series([[1], ([2]), "[3]"])
        set_list = pd.Series([{1}, [2], "{3}"])
        dict_list = pd.Series([{"k1": 1}, '{"k2": 2}', '{"k3": 3}'])

        self.assertFalse(_vec_isinstance(int_list, int))
        self.assertFalse(_vec_isinstance(float_list, float))
        self.assertFalse(_vec_isinstance(str_list, str))
        self.assertFalse(_vec_isinstance(tuple_list, tuple))
        self.assertFalse(_vec_isinstance(list_list, list))
        self.assertFalse(_vec_isinstance(set_list, set))
        self.assertFalse(_vec_isinstance(dict_list, dict))

    def test_vec_isnumeric_pos(self):
        numeric = pd.Series([1, 2.0])
        self.assertTrue(_vec_isnumeric(numeric))

    def test_vec_isnumeric_neg(self):
        non_numeric = pd.Series([1, "2.0"])
        self.assertFalse(_vec_isnumeric(non_numeric))

    def test_vec_is_datetime_pos(self):
        dt = pd.Series([datetime.now(), datetime.now()])
        self.assertTrue(_vec_is_datetime(dt))

    def test_vec_is_datetime_neg(self):
        non_dt = pd.Series(["123", datetime.now()])
        self.assertFalse(_vec_is_datetime(non_dt))

    def test_vec_len_pos(self):
        length = pd.Series([[1, 2, 3], [4, 5]])
        self.assertEqual(
            (np.array([3, 2]) == _vec_len(length)).sum(), 2)


# Running the test
if __name__ == '__main__':
    unittest.main()
