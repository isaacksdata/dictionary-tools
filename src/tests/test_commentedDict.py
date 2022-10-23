import unittest

from src.data_models import CommentedKey
from src.CommentedDict import CommentedDict

# todo add some automated timing measurements


class CommentedDictTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dictionary = CommentedDict(
            numbers=[1, 2, 3],
            letters=["a", "b", "c"],
            comment="This is a dictionary for numbers and letters",
        )

    def test_comment(self) -> None:
        self.assertEqual(
            "This is a dictionary for numbers and letters", self.dictionary.comment
        )

    def test_keys(self) -> None:
        self.assertListEqual(["numbers", "letters"], list(self.dictionary.keys()))

    def test_set_comment(self) -> None:
        self.dictionary.set_comment("a new comment")
        self.assertEqual("a new comment", self.dictionary.comment)

    def test_add_data(self) -> None:
        self.dictionary["floats"] = [0.1, 0.2, 0.3]
        self.assertIn("floats", list(self.dictionary.keys()))
        self.assertListEqual(self.dictionary["floats"], [0.1, 0.2, 0.3])

    def test_add_CommentedKey(self) -> None:
        n = len(self.dictionary)
        ck = CommentedKey("mykey", "a test commented key")
        self.dictionary[ck] = 10
        self.assertEqual(len(self.dictionary), n + 1)

    def test_replace_CommentedKey_with_CommentedKey(self) -> None:
        ck = CommentedKey("mykey", "a test commented key")
        self.dictionary[ck] = 10
        n = len(self.dictionary)
        ck2 = CommentedKey("mykey", "another commented key")
        self.dictionary[ck2] = 100
        self.assertEqual(len(self.dictionary), n)
        self.assertEqual(self.dictionary[ck2], 100)
        self.assertEqual(self.dictionary[ck], 100)

    def test_replace_key_with_CommentedKey(self) -> None:
        ck = CommentedKey("numbers", "some numbers")
        self.dictionary[ck] = [1, 2, 3]
        n = len(self.dictionary)
        self.assertEqual(len(self.dictionary), n)
        self.assertListEqual(self.dictionary[ck], [1, 2, 3])
        self.assertListEqual(self.dictionary["numbers"], [1, 2, 3])

    def test_replace_CommentedKey_with_key(self) -> None:
        ck = CommentedKey("numbers", "some numbers")
        self.dictionary[ck] = [1, 2, 3]
        n = len(self.dictionary)
        self.dictionary["numbers"] = [1, 2, 3]
        self.assertEqual(len(self.dictionary), n)
        self.assertListEqual(self.dictionary["numbers"], [1, 2, 3])
        self.assertRaises(KeyError, self.dictionary.__getitem__, ck)

    def test_keys_types(self) -> None:
        self.assertListEqual(["str", "str"], self.dictionary.keys_types(pretty=True))

    def test_get_key(self) -> None:
        self.assertListEqual(self.dictionary["letters"], ["a", "b", "c"])
        self.assertListEqual(self.dictionary["numbers"], [1, 2, 3])

    def test_get_CommentedKey(self) -> None:
        ck = CommentedKey("mykey", "a commented key")
        self.dictionary[ck] = 100
        self.assertEqual(self.dictionary[ck], 100)

    def test_get_CommentedKeyValue_with_key(self) -> None:
        ck = CommentedKey("mykey", "a commented key")
        self.dictionary[ck] = 100
        self.assertEqual(self.dictionary["mykey"], 100)
