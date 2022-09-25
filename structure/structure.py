"""
Print the structure of a dictionary
"""
from typing import Any, List, Union


class DictionaryParser:
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

    def getStructure_list(self, l: List[Any]) -> str:
        n = len(l)
        types = list(set([self.gtn(x) for x in l]))
        types.sort()
        response = f"list[{', '.join(types)}] n={n}"
        return response

    @staticmethod
    def is_iterable(obj: Any):
        if isinstance(obj, str):
            return False
        try:
            iter(obj)
        except TypeError:
            return False
        else:
            return True


