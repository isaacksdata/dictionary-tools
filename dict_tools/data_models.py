"""Other commented data models used for keys and values"""

from typing import Any, Generator, Hashable, Mapping, Union

from pydantic.dataclasses import dataclass as pyd_dataclass


@pyd_dataclass(eq=True, frozen=True)
class CommentedKey:
    """This is a pydantic dataclass for validating data to be used a dictionary key with a comment

    An object of CommentedKey can be used as a normal dictionary key but with a comment to describe what this key is
    for. Can be useful for complicated, nested dictionaries.

    Attributes:
        key (Hashable): An hashable object which will be the true dictionary key
        comment (str): A comment describing the purpose of the key

    """

    key: Hashable
    comment: Union[str, None] = None


@pyd_dataclass(eq=True, frozen=True)
class CommentedValue:
    """This is a pydantic dataclass for validating data to be used a dictionary value with a comment

    An object of CommentedValue can be used as a normal dictionary value but with a comment to describe what this value
    is. Can be useful for complicated, nested dictionaries.

    Attributes:
        value (Any): An hashable object which will be the true dictionary value
        comment (str): A comment describing the purpose of the value

    """

    value: Any
    comment: Union[str, None] = None


class d_keys:
    """A class used for extracting dictionary keys from CommentedDict"""

    def __init__(self, d: Mapping, removeComments: bool = True):
        """
        Init the class with the dictionary
        :param d: the dictionary to get the keys from
        :type d: dict or CommentedDict
        :param removeComments: True if the comments should be removed from any CommentedKeys
        :type removeComments: bool
        """
        self.__d = d
        self.__removeComments = removeComments

    def __len__(self) -> int:
        return len(self.__d)

    def __contains__(self, key: Hashable) -> bool:
        return key in self.__d

    def __iter__(self) -> Generator:
        for key in self.__d:
            if isinstance(key, CommentedKey) and self.__removeComments:
                yield key.key
            else:
                yield key
