import unittest
from string import ascii_lowercase
import json

from dictionary_tools.structure import DictionaryParser


class StructureTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = DictionaryParser()
        self.dictionary_with_list = {1: 'hello world',
                                     2: 0.1,
                                     3: ['abc', 'def', 1]}
        self.dictionary_with_list_long = {1: 'hello world',
                                     2: 0.1,
                                     3: [ascii_lowercase, 'def', 1]}
        self.dictionary_with_tuple = {1: 'hello world',
                                      2: 0.1,
                                      3: ('abc', 'def', 1)}
        self.dictionary_with_tupleKey = {1: 'hello world',
                                         2: 0.1,
                                         ('abc', 'def', 1): 3}
        self.dictionary_with_custom_obj = {
            'one': 1,
            'two': type('MyClass', (object,), {'content': {}})()
        }
        self.nested_dictionary = {'key1': 2,
                                  'key2': {
                                      'nestedKey1': 'hello',
                                      'nestedKey2': 3
                                  }}
        self.nested_dictionary_2 = {'key1': 2,
                                  'key2': {
                                      'nestedKey1': 'hello',
                                      'nestedKey2': {
                                          'nestedKey3': 0.01
                                      }
                                  }}
        self.nested_dictionary_3 = {'key1': 2,
                                  'key2': {
                                      'nestedKey1': 'hello',
                                      'nestedKey2': {
                                          'nestedKey3': {
                                              'nestedKey4' : [1, 0.1, 'one']
                                          }
                                      }
                                  }}

    def test_getStructure(self):
        expected = "\n{\n\tint : str\n\tint : float\n\tint : list[int, str] n=3\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_list))

    def test_getStructure_example(self):
        self.parser.showExamples = True
        expected = "\n{\n\tint : str\n\tint : float\n\tint : list[int, str] n=3 e.g. abc\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_list))

    def test_getStructure_longExample(self):
        self.parser.showExamples = True
        expected = f"\n{{\n\tint : str\n\tint : float\n\tint : list[int, str] n=3 e.g. {ascii_lowercase[:10]}...\n}}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_list_long))

    def test_getStructure_tuple(self):
        expected = "\n{\n\tint : str\n\tint : float\n\tint : tuple(int, str) n=3\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_tuple))

    def test_getStructure_tupleKey(self):
        expected = "\n{\n\tint : str\n\tint : float\n\ttuple(int, str) n=3 : int\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_tupleKey))

    def test_getStructure_customObj(self):
        expected = "\n{\n\tstr : int\n\tstr : MyClass\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_custom_obj))

    def test_getStructure_nested(self):
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : int\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary))

    def test_gestStructure_nested2(self):
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : {\n\t\t\tstr : float\n\t\t}\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary_2))

    def test_gestStructure_nested3(self):
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : {\n\t\t\tstr : {\n\t\t\t\tstr : list[float, int, str] n=3\n\t\t\t}\n\t\t}\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary_3))

    def test_hardDict(self):
        with open('./combined-newsqa-data-v1.json', 'r') as f:
            d = json.load(f)
        expected = '\n{\n\tstr : str\n\tstr : list [\n\t{\n\t\tstr : str\n\t\tstr : str\n\t\tstr : list [\n\t\t{\n\t\t\tstr : float\n\t\t\tstr : {\n\t\t\t\tstr : int\n\t\t\t\tstr : int\n\t\t\t}\n\t\t\tstr : list [\n\t\t\t{\n\t\t\t\tstr : int\n\t\t\t\tstr : bool\n\t\t\t}\n\t\t\t] n=2\n\t\t\tstr : list [\n\t\t\t{\n\t\t\t\tstr : list [\n\t\t\t\t{\n\t\t\t\t\tstr : int\n\t\t\t\t\tstr : int\n\t\t\t\t}\n\t\t\t\t] n=1\n\t\t\t}\n\t\t\t] n=3\n\t\t\tstr : str\n\t\t\tstr : float\n\t\t}\n\t\t] n=9\n\t\tstr : str\n\t}\n\t] n=12744\n}\n'
        s = self.parser.getStructure(d)
        self.assertEqual(expected, s)


if __name__ == '__main__':
    unittest.main()
