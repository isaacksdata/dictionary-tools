import unittest
import inspect
import os
import sys
import json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from CommentedDict import CommentedDict
from data_models import CommentedKey, CommentedValue

# todo add some automated timing measurements


class CommentedDictTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dictionary = CommentedDict(numbers=[1, 2, 3],
                                        letters=['a', 'b', 'c'],
                                        comment='This is a dictionary for numbers and letters')

    def test_comment(self):
        self.assertEqual('This is a dictionary for numbers and letters', self.dictionary.comment)

    def test_keys(self):
        self.assertListEqual(['numbers', 'letters'], list(self.dictionary.keys()))

    def test_set_comment(self):
        self.dictionary.set_comment('a new comment')
        self.assertEqual('a new comment', self.dictionary.comment)

    def test_add_data(self):
        self.dictionary['floats'] = [0.1, 0.2, 0.3]
        self.assertIn('floats', list(self.dictionary.keys()))
        self.assertListEqual(self.dictionary['floats'], [0.1, 0.2, 0.3])

    def test_add_CommentedKey(self):
        n = len(self.dictionary)
        ck = CommentedKey('mykey', 'a test commented key')
        self.dictionary[ck] = 10
        self.assertEqual(len(self.dictionary), n+1)

    def test_replace_CommentedKey_with_CommentedKey(self):
        ck = CommentedKey('mykey', 'a test commented key')
        self.dictionary[ck] = 10
        n = len(self.dictionary)
        ck2 = CommentedKey('mykey', 'another commented key')
        self.dictionary[ck2] = 100
        self.assertEqual(len(self.dictionary), n)
        self.assertEqual(self.dictionary[ck2], 100)
        self.assertEqual(self.dictionary[ck], 100)

    def test_replace_key_with_CommentedKey(self):
        ck = CommentedKey('numbers', 'some numbers')
        self.dictionary[ck] = [1, 2, 3]
        n = len(self.dictionary)
        self.assertEqual(len(self.dictionary), n)
        self.assertListEqual(self.dictionary[ck], [1, 2, 3])
        self.assertListEqual(self.dictionary['numbers'], [1, 2, 3])

    def test_replace_CommentedKey_with_key(self):
        ck = CommentedKey('numbers', 'some numbers')
        self.dictionary[ck] = [1, 2, 3]
        n = len(self.dictionary)
        self.dictionary['numbers'] = [1, 2, 3]
        self.assertEqual(len(self.dictionary), n)
        self.assertListEqual(self.dictionary['numbers'], [1, 2, 3])
        self.assertRaises(KeyError, self.dictionary.__getitem__, ck)

    def test_keys_types(self):
        self.assertListEqual(['str', 'str'], self.dictionary.keys_types(pretty=True))

    def test_get_key(self):
        self.assertListEqual(self.dictionary['letters'], ['a', 'b', 'c'])
        self.assertListEqual(self.dictionary['numbers'], [1, 2, 3])

    def test_get_CommentedKey(self):
        ck = CommentedKey('mykey', 'a commented key')
        self.dictionary[ck] = 100
        self.assertEqual(self.dictionary[ck], 100)

    def test_get_CommentedKeyValue_with_key(self):
        ck = CommentedKey('mykey', 'a commented key')
        self.dictionary[ck] = 100
        self.assertEqual(self.dictionary['mykey'], 100)
