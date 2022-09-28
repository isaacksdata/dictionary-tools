from collections import UserDict
from typing import List, Hashable, Union, Any
import logging
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from dictionary_tools.structure import DictionaryParser
from dictionary_tools.data_models import d_keys, CommentedKey


class CommentedDict(UserDict):
    """
    Subclass of UserDict with addtional 'comment' attribute
    The comment can be used to describe something about the dictionary
    """
    def __init__(self, *args, **kwargs):
        self.comment = kwargs.pop('comment', '').strip()
        super().__init__(*args, **kwargs)

    def __repr__(self):
        dict_repr = super().__repr__()
        comments = [f'# {line}' for line in self.comment.splitlines()]
        return '\n'.join(comments + [dict_repr])

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
                logging.warning(f'Popping {key.key} and replacing with CommentedKey with key {key}')
                _ = self.data.pop(key.key)
            else:
                ck = self.__checkCommentedKeys(key.key)
                if ck is not None:
                    _ = self.data.pop(ck)
        elif self.__anyCommentedKey():
            # check if any of the CommentedKeys have key attribute equal to key
            ck = self.__checkCommentedKeys(key)
            if ck is not None:
                logging.warning(f'CommentedKey with key = {key} will be replaced with {key}')
                _ = self.data.pop(ck)
        else:
            pass
        self.data[key] = value

    def __checkCommentedKeys(self, key: Hashable) -> Union[type(None), CommentedKey]:
        match = [k for k in self.__getCommentedKeys() if k.key == key]
        if len(match) == 0:
            return None
        elif len(match) == 1:
            return match[0]
        else:
            raise ValueError('Cannot have two CommentedKeys with the same key in the same dictionary!')

    def set_comment(self, comment: str):
        self.comment = comment.strip()

    def get_structure(self):
        return DictionaryParser().getStructure(self)

    def keys_types(self, pretty: bool = False) -> List[Hashable]:
        fun = self.__prettyType if pretty else self.__simpleType
        return [fun(x) for x in d_keys(self, removeComments=False)]

    @staticmethod
    def __simpleType(obj) -> Any:
        return type(obj)

    @staticmethod
    def __prettyType(obj) -> str:
        return type(obj).__name__

    def keys(self) -> d_keys:
        return d_keys(self)

    def __anyCommentedKey(self) -> bool:
        return CommentedKey in self.keys_types()

    def __getCommentedKeys(self) -> List[CommentedKey]:
        return [x for x in d_keys(self, removeComments=False) if isinstance(x, CommentedKey)]

if __name__ == '__main__':
    myKey = CommentedKey(key='letter', comment='This a list of letters')
    c = CommentedDict(numbers=[1,2,3], myString='helloWorld', comment='This is my test')
    c[myKey] = ['a', 'b']
    c.keys()
    c.items()
    d = dict(one=1)
    d.keys()