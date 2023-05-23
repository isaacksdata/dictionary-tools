import unittest

from dict_tools.utils import extract_nested_dict, order_keys


class UtilsTestCse(unittest.TestCase):
    def setUp(self) -> None:
        self.dictionary = {
            "a": {"b": "c"},
            1: {2: {3: {"key": 4}}},
            (1, 2): {0.51: "value"},
        }

    def test_extract_nested_dict(self) -> None:
        path = "a/b"
        self.assertEqual(extract_nested_dict(self.dictionary, path=path), "c")
        keys_1 = [1, 2, 3, "key"]
        self.assertEqual(extract_nested_dict(self.dictionary, keys=keys_1), 4)
        keys_2 = [(1, 2), 0.51]
        self.assertEqual(extract_nested_dict(self.dictionary, keys=keys_2), "value")

    def test_order_keys(self) -> None:
        test_data = [2, 3, 1, "key"]
        expected_output = [1, 2, 3, "key"]
        self.assertListEqual(order_keys(self.dictionary, test_data), expected_output)

        self.assertRaises(KeyError, order_keys, self.dictionary, [3, 1, "key"])
