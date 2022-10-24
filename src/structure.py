"""
Print the src of a dictionary
"""
from typing import Any, Hashable, List, Mapping, Tuple, Union


class DictionaryParser:
    """
    This is a class for parsing a dictionary and returning a string of its src which can be printed for a
    convenient way of understanding any nested src and the types used
    # todo option to display actual keys
    # todo check or DefaultDict, OrderedDict - other data structures
    """

    def __init__(self, showExamples: bool = False):
        """
        Init the Dictionary parser class
        :param showExamples: Should examples of iterables be included in the summary output
        :type showExamples: bool
        """
        self.dictionary: Union[dict, None] = None
        self.response: Union[dict, None] = None
        self.nTabs: int = 0
        self.tabs: str = ""
        self.showExamples = showExamples

    def incrementTab(self) -> None:
        """
        Increase the number of tabs by 1.
        E.g. '\t' -> '\t\t'
        :return: void
        :rtype: void
        """
        self.nTabs += 1
        self.tabs = "".join(["\t"] * self.nTabs)

    def decrementTab(self) -> None:
        """
        Decrease the number of tabs by 1
        E.g. '\t\t' -> '\t'
        :return: void
        :rtype: void
        """
        self.nTabs -= 1
        self.tabs = "".join(["\t"] * self.nTabs)

    def getStructure(self, dictionary: Mapping) -> str:
        """
        Initialise the response string and start the structure analysis of the dictionary
        :param dictionary: the dictionary object to parse
        :type dictionary: dict
        :return: response
        :rtype: str
        """
        response = """"""
        response = self.getStructure_dict(dictionary, response)
        return response

    def getStructure_dict(
        self, dictionary: Mapping, response: str, k: Hashable = None
    ) -> str:
        """
        Summarise the structure of a dictionary

        Iterate over the key : value pairs. If the value is not iterable (excluding strings) then the response is
        appended with the key and value type. If the value is iterable (list, tuple, ...) then the iterable itself is
        unpacked and described. If the value is another dictionary then the function becomes recursive as this function
        is called again on the sub-dictionary.
        :param dictionary: The dictionary to unpack and describe
        :type dictionary: dict
        :param response: the response string so far
        :type response: str
        :param k: if the input dictionary is a value, then k is the key
        :type k: hashable object
        :return: the updated response
        :rtype: str
        """
        if k is None:
            response = response + f"\n{self.tabs}{{\n"
        else:
            response = response + f"{self.tabs}{self.gtnk(k)} : {{\n"
        self.incrementTab()
        for key, value in dictionary.items():
            if not self.is_iterable(value):
                response = (
                    response + f"{self.tabs}{self.gtnk(key)} : {self.gtn(value)}\n"
                )
            elif isinstance(value, (list, tuple)):
                r = self.getStructure_list(value)
                response = response + f"{self.tabs}{self.gtnk(key)} : {r}\n"
            elif isinstance(value, dict):
                response = self.getStructure_dict(value, response, key)
            else:
                print(f"Unknown object of type {type(value)}")
                response = (
                    response + f"{self.tabs}{self.gtnk(key)} : {self.gtn(value)}\n"
                )
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

    def getStructure_list(self, my_list: Union[List[Any], Tuple[Any, ...]]) -> str:
        """
        Get the src of a list element. The response will include a list of all the types contained within the
        list 'l' and the length of list 'l'
        :param my_list: the list to be investigated
        :type my_list: list of any type
        :return: response
        :rtype: str
        """
        n = len(my_list)
        types = list(set([self.gtn(x) for x in my_list]))
        types.sort()
        l_type = self.gtn(my_list)
        if all([x == "dict" for x in types]):
            r = self.getStructure_dict(my_list[0], "")
        else:
            r = None
        if l_type == "list":
            if r is None:
                response = f"{l_type} [{', '.join(types)}] n={n}"
            else:
                response = f"{l_type} [{r}{self.tabs}] n={n}"
        else:
            if r is None:
                response = f"{l_type} ({', '.join(types)}) n={n}"
            else:
                response = f"{l_type} ({r}{self.tabs}) n={n}"
        if self.showExamples and len(my_list) > 0:
            example = my_list[0]
            if isinstance(example, str):
                example = f"{example[:10]}..." if len(example) > 10 else example
            response = response + f" e.g. {example}"
        return response

    @staticmethod
    def is_iterable(obj: Any) -> bool:
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
