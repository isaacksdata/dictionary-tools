"""
Print the dictionary_tools of a dictionary
"""
from typing import Any, List, Union, Tuple


class DictionaryParser:
    """
    This is a class for parsing a dictionary and returning a string of its dictionary_tools which can be printed for a
    convenient way of understanding any nested dictionary_tools and the types used
    # todo add option to show an example of key or value
    # todo add option for comments e.g. docstrings within dictionary - might need to extend the dictionary class
    # todo check or DefaultDict, OrderedDict - other data structures
    """
    def __init__(self, showExamples: bool = False):
        self.dictionary: Union[dict, None] = None
        self.response: Union[dict, None] = None
        self.nTabs: int = 0
        self.tabs: str = ''
        self.showExamples = showExamples

    def incrementTab(self):
        self.nTabs += 1
        self.tabs = ''.join(['\t'] * self.nTabs)

    def decrementTab(self):
        self.nTabs -= 1
        self.tabs = ''.join(['\t'] * self.nTabs)

    def getStructure(self, dictionary: dict) -> str:
        response = f""""""
        response = self.getStructure_dict(dictionary, response)
        return response

    def getStructure_dict(self, dictionary: dict,
                          response: str,
                          k: str = None) -> str:
        if k is None:
            response = response + f"\n{self.tabs}{{\n"
        else:
            response = response + f"{self.tabs}{self.gtnk(k)} : {{\n"
        self.incrementTab()
        for key, value in dictionary.items():
            if not self.is_iterable(value):
                response = response + f"{self.tabs}{self.gtnk(key)} : {self.gtn(value)}\n"
            elif isinstance(value, (list, tuple)):
                r = self.getStructure_list(value)
                response = response + f"{self.tabs}{self.gtnk(key)} : {r}\n"
            elif isinstance(value, dict):
                response = self.getStructure_dict(value, response, key)
            else:
                print(f'Unknown object of type {type(value)}')
                response = response + f"{self.tabs}{self.gtnk(key)} : {self.gtn(value)}\n"
        self.decrementTab()
        response = response + f"{self.tabs}}}\n"
        return response

    def gtn(self, obj: Any) -> str:
        """
        gtn -> short for getTypeName
        :param obj: object to get the type of as a string
        :type obj: Any
        :return: type
        :rtype: str
        """
        return type(obj).__name__

    def gtnk(self, obj: Any) -> str:
        """
        gtn -> short for getTypeNameKey
        This method is called when getting the type name for keys as iterable keys need to be dealt with
        seperatley
        :param obj: object to get the type of as a string
        :type obj: Any
        :return: type
        :rtype: str
        """
        if isinstance(obj, tuple):
            return self.getStructure_list(obj)
        else:
            return type(obj).__name__

    def getStructure_list(self, l: Union[List[Any], Tuple[Any]]) -> str:
        """
        Get the dictionary_tools of a list element. The response will include a list of all the types contained within the
        list 'l' and the length of list 'l'
        :param l: the list to be investigated
        :type l: list of any type
        :return: response
        :rtype: str
        """
        n = len(l)
        types = list(set([self.gtn(x) for x in l]))
        types.sort()
        l_type = self.gtn(l)
        if l_type == 'list':
            response = f"{l_type}[{', '.join(types)}] n={n}"
        else:
            response = f"{l_type}({', '.join(types)}) n={n}"
        if self.showExamples and len(l) > 0:
            example = l[0]
            if isinstance(example, str):
                example = f'{example[:10]}...' if len(example) > 10 else example
            response = response + f' e.g. {example}'
        return response

    @staticmethod
    def is_iterable(obj: Any):
        """
        Return True if an object is iterable.
        If true then the object has the __iter__ method or the __getitem__ method
        Strings are iterable but for this exercise - False is returned for string types
        :param obj: the object to check
        :type obj: any
        :return: True or False
        :rtype: bool
        """
        if isinstance(obj, str):
            return False
        try:
            iter(obj)
        except TypeError:
            return False
        else:
            return True


