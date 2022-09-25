from collections import UserDict

from dictionary_tools.structure import DictionaryParser


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

    def set_comment(self, comment: str):
        self.comment = comment.strip()

    def get_structure(self):
        return DictionaryParser().getStructure(self)


if __name__ == '__main__':
    c = CommentedDict(numbers=[1,2,3], myString='helloWorld', comment='This is my test')
    c.items()