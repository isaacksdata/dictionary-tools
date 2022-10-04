import inspect
import logging
import os
import sys
from collections import UserDict
from typing import Hashable, KeysView, List, Union

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.data_models import CommentedKey, d_keys
from src.structure import DictionaryParser


class CommentedDict(UserDict):
    """
    Subclass of UserDict with addtional 'comment' attribute

    Additional functionalities include:
        1) a method to print the general structure of the dictionary
        2) a method to return the types of the dictionary keys
        3) a method to return the dictionary comment

    The __setitem__ and __getitem__ methods are over-ridden in order to handle CommentedKeys.
    The __getitem__method allows the values of CommentedKeys to be returned by supplying the key attribute of the
    CommentedKey.
    e.g. given a CommentedDict with a CommentedKey as follows called d:

    print(d)
    # This is my test
    {'numbers': [1, 2, 3], 'myString': 'helloWorld', CommentedKey(key='letter',
    comment='This a list of letters'): ['a', 'b']}

    The list of letters "['a', 'b']" could be returned with "d['letter']"

    The __setitem__ is over-ridden such that a standard dictionary key and CommentedKey cannot both exist in the
    dictionary if the key attribute of the CommentedKey is equal to the standard key.

    e.g. given a CommentedDict with a CommentedKey as follows called d:

    print(d)
    # This is my test
    {'numbers': [1, 2, 3], 'myString': 'helloWorld', CommentedKey(key='letter',
    comment='This a list of letters'): ['a', 'b']}

    Then d['letter'] = ['c', 'd']

    would result in the dictionary
    print(d)
    # This is my test
    {'numbers': [1, 2, 3], 'myString': 'helloWorld', 'letter': ['c', 'd']}

    """

    def __init__(self, *args, **kwargs):
        self.comment = kwargs.pop("comment", "").strip()
        super().__init__(*args, **kwargs)

    def __repr__(self):
        dict_repr = super().__repr__()
        comments = [f"# {line}" for line in self.comment.splitlines()]
        return "\n".join(comments + [dict_repr])

    def __getitem__(self, key):
        """
        Overriding the getitem method

        :param key:
        :type key:
        :return:
        :rtype:
        """
        if key in self.data:
            return self.data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        if isinstance(key, CommentedKey):
            commentedKey = self.__checkCommentedKeys(key.key)
        else:
            commentedKey = self.__checkCommentedKeys(key)
        if commentedKey is not None:
            return self.data[commentedKey]
        raise KeyError(key)

    def __setitem__(self, key, value):
        # check for any CommentedKeys in the dictionary
        if isinstance(key, CommentedKey):
            v = self.data.get(key.key, None)
            if v is not None:
                logging.warning(
                    f"Popping {key.key} and replacing with CommentedKey with key {key}"
                )
                _ = self.data.pop(key.key)
            else:
                ck = self.__checkCommentedKeys(key.key)
                if ck is not None:
                    _ = self.data.pop(ck)
        elif self.__anyCommentedKey():
            # check if any of the CommentedKeys have key attribute equal to key
            ck = self.__checkCommentedKeys(key)
            if ck is not None:
                logging.warning(
                    f"CommentedKey with key = {key} will be replaced with {key}"
                )
                _ = self.data.pop(ck)
        else:
            pass
        self.data[key] = value

    def __checkCommentedKeys(self, key: Hashable) -> Union[type[None], CommentedKey]:
        """
        Check to see if there is a CommentedKey in the dictionary whereby the key attribute equals the input key
        :param key: input key
        :type key: Hashable
        :return: the CommentedKey if found else None
        :rtype: CommentedKey or None
        """
        match = [k for k in self.__getCommentedKeys() if k.key == key]
        if len(match) == 0:
            return None
        elif len(match) == 1:
            return match[0]
        else:
            raise ValueError(
                "Cannot have two CommentedKeys with the same key in the same dictionary!"
            )

    def set_comment(self, comment: str) -> None:
        """
        Set the comment of the dictionary
        :param comment: the comment
        :type comment: str
        :return: void
        :rtype: void
        """
        self.comment = comment.strip()

    def get_structure(self) -> str:
        """
        Get the structure of the dictionary as a summary string

        Utilises the DictionaryParser class
        :return: string of the dictionary structure
        :rtype: str
        """
        return DictionaryParser().getStructure(self)

    def keys_types(self, pretty: bool = False, unique: bool = False) -> List[Hashable]:
        """
        Get the types of the keys in the dictionary
        :param pretty: True if the types of the keys should be returned as pretty strings rather than type
        :type pretty: bool
        :param unique: True if the list should contain unique types. E.g. for a dictionary with three keys and all are
            strings, then [str] would be returned
        :type unique: bool
        :return: list of types
        :rtype: list of Hashables
        """
        fun = self.__prettyType if pretty else self.__simpleType
        types = [fun(x) for x in d_keys(self, removeComments=False)]
        if unique:
            return list(set(types))
        else:
            return types

    @staticmethod
    def __simpleType(obj) -> type:
        """
        Return the type of an object
        :param obj: the object to get the type of
        :type obj: Any
        :return: the type of the object
        :rtype: type
        """
        return type(obj)

    @staticmethod
    def __prettyType(obj) -> str:
        """
        Return the type of an object as a string
        :param obj: object to get the type of
        :type obj: Any
        :return: the type of the object
        :rtype: str
        """
        return type(obj).__name__

    def keys(self) -> d_keys:
        """
        Return the keys of the dictionary
        :return: the keys
        :rtype: d_keys
        """
        return d_keys(self)

    def __anyCommentedKey(self) -> bool:
        """
        Determine if any keys of the dictionary are CommentedKeys
        :return: True if a CommentedKey is found
        :rtype: bool
        """
        return CommentedKey in self.keys_types()

    def __getCommentedKeys(self) -> List[CommentedKey]:
        """
        Return the CommentedKeys of the dictionary
        :return: commented keys
        :rtype: list of commented keys
        """
        return [
            x for x in d_keys(self, removeComments=False) if isinstance(x, CommentedKey)
        ]


if __name__ == "__main__":
    myKey = CommentedKey(key="letter", comment="This a list of letters")
    c = CommentedDict(
        numbers=[1, 2, 3], myString="helloWorld", comment="This is my test"
    )
    c[myKey] = ["a", "b"]
    c.keys()
    c.items()
    d = dict(one=1)
    d.keys()
