import unittest

from structure.structure import DictionaryParser


class StructureTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = DictionaryParser()
        self.dictionary_with_list = {1: 'hello world',
                                     2: 0.1,
                                     3: ['abc', 'def', 1]}
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

    def test_getStructure_nested(self):
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : int\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary))

    def test_gestStructure_nested2(self):
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : {\n\t\t\tstr : float\n\t\t}\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary_2))

    def test_gestStructure_nested3(self):
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : {\n\t\t\tstr : {\n\t\t\t\tstr : list[float, int, str] n=3\n\t\t\t}\n\t\t}\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary_3))


if __name__ == '__main__':
    unittest.main()
