import unittest

from dictionary_tools.CommentedDict import CommentedDict

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


