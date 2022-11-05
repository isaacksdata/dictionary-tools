import json
import unittest
from collections import OrderedDict, defaultdict
from string import ascii_lowercase

from src.CommentedDict import CommentedDict
from src.structure import DictionaryParser


class StructureTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = DictionaryParser()
        self.dictionary_with_list = {1: "hello world", 2: 0.1, 3: ["abc", "def", 1]}
        self.dictionary_with_list_long = {
            1: "hello world",
            2: 0.1,
            3: [ascii_lowercase, "def", 1],
        }
        self.dictionary_with_tuple = {1: "hello world", 2: 0.1, 3: ("abc", "def", 1)}
        self.dictionary_with_tupleKey = {1: "hello world", 2: 0.1, ("abc", "def", 1): 3}
        self.dictionary_with_custom_obj = {
            "one": 1,
            "two": type("MyClass", (object,), {"content": {}})(),
        }
        self.nested_dictionary = {
            "key1": 2,
            "key2": {"nestedKey1": "hello", "nestedKey2": 3},
        }
        self.nested_dictionary_2 = {
            "key1": 2,
            "key2": {"nestedKey1": "hello", "nestedKey2": {"nestedKey3": 0.01}},
        }
        self.nested_dictionary_3 = {
            "key1": 2,
            "key2": {
                "nestedKey1": "hello",
                "nestedKey2": {"nestedKey3": {"nestedKey4": [1, 0.1, "one"]}},
            },
        }

        self.commented_dictionary = CommentedDict(
            numbers=[1, 2, 3],
            letters=["a", "b", "c"],
            comment="This is a dictionary for numbers and letters",
        )

    def test_getStructure(self) -> None:
        expected = "\n{\n\tint : str\n\tint : float\n\tint : list [int, str] n=3\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_list))

    def test_getStructure_example(self) -> None:
        self.parser.showExamples = True
        expected = (
            "\n{\n\tint : str\n\tint : float\n\tint : list [int, str] n=3 e.g. abc\n}\n"
        )
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_list))

    def test_getStructure_longExample(self) -> None:
        self.parser.showExamples = True
        expected = f"\n{{\n\tint : str\n\tint : float\n\tint : list [int, str] n=3 e.g. {ascii_lowercase[:10]}...\n}}\n"
        self.assertEqual(
            expected, self.parser.getStructure(self.dictionary_with_list_long)
        )

    def test_getStructure_tuple(self) -> None:
        expected = "\n{\n\tint : str\n\tint : float\n\tint : tuple (int, str) n=3\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.dictionary_with_tuple))

    def test_getStructure_tupleKey(self) -> None:
        expected = "\n{\n\tint : str\n\tint : float\n\ttuple (int, str) n=3 : int\n}\n"
        self.assertEqual(
            expected, self.parser.getStructure(self.dictionary_with_tupleKey)
        )

    def test_getStructure_customObj(self) -> None:
        expected = "\n{\n\tstr : int\n\tstr : MyClass\n}\n"
        self.assertEqual(
            expected, self.parser.getStructure(self.dictionary_with_custom_obj)
        )

    def test_getStructure_nested(self) -> None:
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : int\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary))

    def test_gestStructure_nested2(self) -> None:
        expected = "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : {\n\t\t\tstr : float\n\t\t}\n\t}\n}\n"
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary_2))

    def test_gestStructure_nested3(self) -> None:
        expected = (
            "\n{\n\tstr : int\n\tstr : {\n\t\tstr : str\n\t\tstr : {\n\t\t\tstr : {\n\t\t\t\tstr : "
            "list [float, int, str] n=3\n\t\t\t}\n\t\t}\n\t}\n}\n"
        )
        self.assertEqual(expected, self.parser.getStructure(self.nested_dictionary_3))

    def test_hardDict(self) -> None:
        with open("./combined-newsqa-data-v1.json", "r") as f:
            d = json.load(f)
        expected = (
            "\n{\n\tstr : str\n\tstr : list [\n\t{\n\t\tstr : str\n\t\tstr : str\n\t\tstr : "
            "list [\n\t\t{\n\t\t\tstr : float\n\t\t\tstr : {\n\t\t\t\tstr : int\n\t\t\t\tstr : "
            "int\n\t\t\t}\n\t\t\tstr : list [\n\t\t\t{\n\t\t\t\tstr : int\n\t\t\t\tstr : "
            "bool\n\t\t\t}\n\t\t\t] n=2\n\t\t\tstr : list [\n\t\t\t{\n\t\t\t\tstr : "
            "list [\n\t\t\t\t{\n\t\t\t\t\tstr : int\n\t\t\t\t\tstr : int\n\t\t\t\t}\n\t\t\t\t] "
            "n=1\n\t\t\t}\n\t\t\t] n=3\n\t\t\tstr : str\n\t\t\tstr : "
            "float\n\t\t}\n\t\t] n=9\n\t\tstr : str\n\t}\n\t] n=12744\n}\n"
        )
        s = self.parser.getStructure(d)
        self.assertEqual(expected, s)

    def test_defaultdict(self) -> None:
        # ----- testing default int --------
        d = defaultdict(int)
        d[1] = 1
        s = self.parser.getStructure(d)
        expected = "\nDefault = int\n{\n\tint : int\n}\n"
        self.assertEqual(s, expected)

        # testing default list
        d2: defaultdict = defaultdict(list)
        keys = ["a", "a", "b", "b", "c"]
        values = [1, 2, 3, 4, 5]
        for k, v in zip(keys, values):
            d2[k].append(v)
        s = self.parser.getStructure(d2)
        expected = "\nDefault = list\n{\n\tstr : list [int] n=2\n\tstr : list [int] n=2\n\tstr : list [int] n=1\n}\n"
        self.assertEqual(s, expected)

    def test_ordereddict(self) -> None:
        d = OrderedDict()
        keys = ["a", "b", "c", "d", "e", "f"]
        values = [1, 0.1, "third element", [1, 2, 3], (1, 2, 3), dict(key="value")]
        for k, v in zip(keys, values):
            d[k] = v
        s = self.parser.getStructure(d)
        expected = (
            "\nOrderedDict\n{\n\t1-> str : int\n\t2-> str : float\n\t3-> str : str\n\t4-> str : list [int] "
            "n=3\n\t5-> str : tuple (int) n=3\n\t6-> str : {\n\t\t1-> str : str\n\t}\n}\n"
        )
        self.assertEqual(s, expected)

    def test_commenteddict(self) -> None:
        s = self.parser.getStructure(self.commented_dictionary)
        expected = ("\nComment : This is a dictionary for numbers and letters\n{\n\tstr : list [int] "
                    "n=3\n\tstr : list [str] n=3\n}\n")
        self.assertEqual(s, expected)


if __name__ == "__main__":
    unittest.main()
