"""
Print the structure of a dictionary
"""
from typing import Any, List, Union, Tuple


class DictionaryParser:
    """
    This is a class for parsing a dictionary and returning a string of its structure which can be printed for a
    convenient way of understanding any nested structure and the types used
    # todo add option to show an example of key or value
    # todo add option for comments e.g. docstrings within dictionary - might need to extend the dictionary class
    # todo check or DefaultDict, OrderedDict - other data structures
    """
    def __init__(self):
        self.dictionary: Union[dict, None] = None
        self.response: Union[dict, None] = None
        self.nTabs: int = 0
        self.tabs: str = ''

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
            response = response + f"{self.tabs}{self.gtn(k)} : {{\n"
        self.incrementTab()
        for key, value in dictionary.items():
            if not self.is_iterable(value):
                response = response + f"{self.tabs}{self.gtn(key)} : {self.gtn(value)}\n"
            elif isinstance(value, (list, tuple)):
                r = self.getStructure_list(value)
                response = response + f"{self.tabs}{self.gtn(key)} : {r}\n"
            elif isinstance(value, dict):
                response = self.getStructure_dict(value, response, key)
            else:
                print(f'Unknown object of type {type(value)}')
                response = response + f"{self.tabs}{self.gtn(key)} : {self.gtn(value)}\n"
        self.decrementTab()
        response = response + f"{self.tabs}}}\n"
        return response

    @staticmethod
    def gtn(obj: Any) -> str:
        """
        gtn -> short for getTypeName
        :param obj: object to get the type of as a string
        :type obj: Any
        :return: type
        :rtype: str
        """
        return type(obj).__name__

    def getStructure_list(self, l: Union[List[Any], Tuple[Any]]) -> str:
        """
        Get the structure of a list element. The response will include a list of all the types contained within the
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


