"""
Print the src of a dictionary
"""
import random
from collections import OrderedDict, defaultdict
from typing import Any, Hashable, List, Mapping, Tuple, Union

from src.CommentedDict import CommentedDict
from src.data_models import CommentedKey, CommentedValue
from src.utils import sort_mixed_list

random.seed(10)


class DictionaryParser:
    """
    This is a class for parsing a dictionary and returning a string of its src which can be printed for a
    convenient way of understanding any nested src and the types used

    If showVariables is True, then the keys and values will be printed. If the key or a value is an iterable
    (except a string) then a number of examples will be printed. The number of examples displayed is controlled by
    nExamples parameter. These examples may be random, first or last - controlled by whereExamples parameter.
    """

    def __init__(
        self,
        showExamples: bool = False,
        showKeyComments: bool = False,
        showValueComments: bool = False,
        showVariables: bool = False,
        nExamples: int = 3,
        whereExamples: str = "random",
    ):
        """
        Init the Dictionary parser class
        :param showExamples: Should examples of iterables be included in the summary output
        :type showExamples: bool
        :param showKeyComments: Should the comment of CommentedKeys be printed in the output
        :type showKeyComments: bool
        :param showValueComments: Should the comment of CommentedValues be printed in the output
        :type showValueComments: bool
        :param showVariables: Should the actual variables of the dictionary be printed
        :type showVariables: bool
        :param nExamples: the number of examples to show of an iterable if showVariables is True
        :type nExamples: int
        :param whereExamples: where to sample examples of an iterable from is showVariables is True. Should be
                            'random', 'first' or 'last'
        :type whereExamples: str
        """
        self.dictionary: Union[dict, None] = None
        self.response: Union[dict, None] = None
        self.nTabs: int = 0
        self.tabs: str = ""
        self.showExamples = showExamples
        self.showKeyComments = showKeyComments
        self.showValueComments = showValueComments
        self.showVariables = showVariables
        self.nExamples = nExamples
        self.whereExamples = whereExamples
        self.is_ordered = False

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
        :type dictionary: Mapping
        :return: response
        :rtype: str
        """
        response = """"""
        response = self.check_default_dict(dictionary=dictionary, response=response)
        response = self.check_ordered_dict(dictionary=dictionary, response=response)
        response = self.check_commented_dict(dictionary=dictionary, response=response)
        response = self.getStructure_dict(dictionary, response)
        return response

    @staticmethod
    def check_commented_dict(dictionary: Mapping, response: str) -> str:
        """
        Check if the dictionary is a commented dict and if so add a statement to print the comment

        :param dictionary: the input dictionary
        :type dictionary: Mapping
        :param response: the response string so far
        :type response: str
        :return: response
        :rtype: str
        """
        if isinstance(dictionary, CommentedDict):
            response = response + f"\nComment : {dictionary.comment}"
        return response

    def check_ordered_dict(self, dictionary: Mapping, response: str) -> str:
        """
        Check if the dictionary is an ordered dict and if so add a statement to say so

        If ordered dict, then set self.is_ordered to True
        :param dictionary: the input dictionary
        :type dictionary: Mapping
        :param response: the response string so far
        :type response: str
        :return: response
        :rtype: str
        """
        if isinstance(dictionary, OrderedDict):
            response = response + "\nOrderedDict"
            self.is_ordered = True
        return response

    @staticmethod
    def check_default_dict(dictionary: Mapping, response: str) -> str:
        """
        Check if the dictionary is a default dict and if so add a statement to describe the default element

        :param dictionary: the input dictionary
        :type dictionary: Mapping
        :param response: the response string so far
        :type response: str
        :return: response
        :rtype: str
        """
        if isinstance(dictionary, defaultdict):
            default = dictionary.default_factory
            if default is not None:
                response = response + f"\nDefault = {default.__name__}"
            else:
                response = response + "\nDefault = Not specified"
        return response

    def getStructure_dict(
        self,
        dictionary: Union[Mapping, CommentedValue],
        response: str,
        k: Hashable = None,
        idx: str = "",
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
        :param idx: index of the key if the value is a dictionary
        :type idx: str
        :return: the updated response
        :rtype: str
        """
        is_commented_value = False
        comment = None
        if k is None:
            response = response + f"\n{self.tabs}{{\n"
        else:
            if isinstance(dictionary, CommentedValue):
                response = (
                    response
                    + f"{self.tabs}{idx}{self.gtnk(k)} : {type(dictionary).__name__} [{{\n"
                )
                comment = dictionary.comment
                dictionary = dictionary.value
                is_commented_value = True
            else:
                response = response + f"{self.tabs}{idx}{self.gtnk(k)} : {{\n"
        if isinstance(dictionary, Mapping):
            self.incrementTab()
            for i, (key, value) in enumerate(dictionary.items()):
                idx = f"{i+1}-> " if self.is_ordered else ""

                if (
                    not isinstance(value, CommentedValue)
                    and not self.is_iterable(value)
                ) or (
                    isinstance(value, CommentedValue)
                    and not self.is_iterable(value.value)
                ):
                    response = (
                        response
                        + f"{self.tabs}{idx}{self.gtnk(key)} : {self.gtn(value)}\n"
                    )
                elif isinstance(value, (list, tuple)) or (
                    isinstance(value, CommentedValue)
                    and isinstance(value.value, (list, tuple))
                ):
                    r = self.getStructure_list(value)
                    response = response + f"{self.tabs}{idx}{self.gtnk(key)} : {r}\n"
                elif isinstance(value, dict) or (
                    isinstance(value, CommentedValue) and isinstance(value.value, dict)
                ):
                    response = self.getStructure_dict(value, response, key, idx)
                else:
                    print(f"Unknown object of type {type(value)}")
                    response = (
                        response
                        + f"{self.tabs}{idx}{self.gtnk(key)} : {self.gtn(value)}\n"
                    )
            self.decrementTab()
            if is_commented_value:
                response = response + f"{self.tabs}}}] <{comment}>\n"
            else:
                response = response + f"{self.tabs}}}\n"
            return response
        else:
            raise TypeError(
                f"Only objects of type Mapping should be passed here. "
                f"Not objects of type {type(dictionary)}"
            )

    def gtn(self, obj: Any, blockVariable: bool = False) -> str:
        """
        gtn -> short for getTypeName
        :param obj: object to get the type of as a string
        :type obj: Any
        :param blockVariable: If True, then showVariable class parameter is blocked
        :type blockVariable: bool
        :return: type
        :rtype: str
        """
        if self.showVariables and not blockVariable:
            return self.gtn_with_variable(obj=obj)
        if isinstance(obj, CommentedValue):
            response = f"{type(obj).__name__} [{self.gtn(obj.value)}]"
            if self.showValueComments:
                response = response + f" <{obj.comment}>"
        else:
            response = type(obj).__name__
        return response

    def gtn_with_variable(self, obj: Any) -> str:
        """
        gtn -> short for getTypeName and show the variable in the response
        :param obj: object to get the type of as a string
        :type obj: Any
        :return: type
        :rtype: str
        """
        if isinstance(obj, CommentedValue):
            response = f"{type(obj).__name__} [{self.gtn(obj.value)}]"
            if self.showValueComments:
                response = response + f" <{obj.comment}>"
        else:
            if isinstance(obj, (tuple, list)):
                if self.whereExamples == "random":
                    items = random.sample(obj, k=self.nExamples)
                    items.sort(key=sort_mixed_list)
                elif self.whereExamples == "first":
                    items = obj[: self.nExamples]
                elif self.whereExamples == "last":
                    items = obj[self.nExamples * -1 :]
                else:
                    raise ValueError(
                        f"self.whereExamples must be one of 'random', 'first' or 'last' : "
                        f"not {self.whereExamples}"
                    )
                response = f"{type(obj).__name__} <{items}>"
            else:
                response = f"{type(obj).__name__} <{obj}>"
        return response

    def gtnk(self, obj: Any) -> str:
        """
        gtnk -> short for getTypeNameKey
        This method is called when getting the type name for keys as iterable keys need to be dealt with
        seperatley
        :param obj: object to get the type of as a string
        :type obj: Any
        :return: type
        :rtype: str
        """
        if self.showVariables:
            return self.gtnk_with_variable(obj=obj)
        if isinstance(obj, CommentedKey):
            response = f"{type(obj).__name__} [{self.gtnk(obj.key)}]"
            if self.showKeyComments:
                response = response + f" <{obj.comment}>"
        elif isinstance(obj, tuple):
            response = self.getStructure_list(obj)
        else:
            response = type(obj).__name__
        return response

    def gtnk_with_variable(self, obj: Any) -> str:
        """
        gtnk -> short for getTypeNameKey and show with the variable
        This method is called when getting the type name for keys as iterable keys need to be dealt with
        seperatley
        :param obj: object to get the type of as a string
        :type obj: Any
        :return: type
        :rtype: str
        """
        if isinstance(obj, CommentedKey):
            response = f"{type(obj).__name__} [{self.gtnk(obj.key)}]"
            if self.showKeyComments:
                response = response + f" <{obj.comment}>"
        elif isinstance(obj, tuple):
            response = self.getStructure_list(obj)
        else:
            response = f"{type(obj).__name__} <{obj}>"
        return response

    def getStructure_list(
        self, my_list: Union[List[Any], Tuple[Any, ...], CommentedValue]
    ) -> str:
        """
        Get the src of a list element. The response will include a list of all the types contained within the
        list 'l' and the length of list 'l'
        :param my_list: the list to be investigated
        :type my_list: list of any type
        :return: response
        :rtype: str
        """
        is_commented_value: bool = False
        if isinstance(my_list, CommentedValue):
            is_commented_value = True
            name = type(my_list).__name__
            comment = my_list.comment
            my_list = my_list.value
        else:
            name = None
            comment = None

        assert isinstance(
            my_list, (tuple, list)
        ), f"Got {type(my_list)} instead of tuple or list!"
        n = len(my_list)
        types = list(set([self.gtn(x, blockVariable=True) for x in my_list]))
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
        if is_commented_value:
            response = f"{name} [" + response + f"] <{comment}>"
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
