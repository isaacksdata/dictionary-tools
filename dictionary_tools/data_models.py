"""
Other commented data models used for keys and values
"""
from typing import Any, Union
from pydantic.dataclasses import dataclass as pyd_dataclass


@pyd_dataclass(eq=True, frozen=True)
class CommentedKey:
    key: Any
    comment: Union[str, None] = None


@pyd_dataclass(eq=True, frozen=True)
class CommentedValue:
    value: Any
    comment: Union[str, None] = None


class d_keys:

    def __init__(self, d, removeComments: bool = True):
        self.__d = d
        self.__removeComments = removeComments

    def __len__(self):
        return len(self.__d)

    def __contains__(self, key):
        return key in self.__d

    def __iter__(self):
        for key in self.__d:
            if isinstance(key, CommentedKey) and self.__removeComments:
                yield key.key
            else:
                yield key