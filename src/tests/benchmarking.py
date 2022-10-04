import inspect
import os
import sys
from line_profiler import LineProfiler

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from CommentedDict import CommentedDict
from data_models import CommentedKey, CommentedValue

basic_dict = {}
basic_dict['mykey'] = 10
commentedDict = CommentedDict()
commentedDict['mykey'] = 10
commentedKey = CommentedKey(key='myCommentedKey', comment="Test commented Key")
anotherCommentedKey = CommentedKey(key='AnotherCommentedKey', comment="Test commented Key")
commentedDict_withCommentedKey = CommentedDict()
commentedDict_withCommentedKey[commentedKey] = 20


def basic_set():
    basic_dict[1] = 2


def commented_set():
    commentedDict[1] = 2


def basic_replace():
    basic_dict['mykey'] = 20


def commented_replace():
    commentedDict['mykey'] = 20


def basic_get():
    _ = basic_dict['mykey']


def commented_get():
    _ = commentedDict['mykey']


def set_commentedKey():
    commentedDict[commentedKey] = 10


def replace_commentedKey_basic():
    commentedDict_withCommentedKey['myCommentedKey'] = 20


def replace_commentedKey_with_commentedKey():
    commentedDict_withCommentedKey[commentedKey] = 100


def get_commentedKey():
    _ = commentedDict_withCommentedKey[commentedKey]


def get_commentedKey_with_str():
    _ = commentedDict_withCommentedKey['myCommentedKey']


def main():
    basic_set()
    commented_set()
    basic_replace()
    commented_replace()
    basic_get()
    commented_get()
    set_commentedKey()
    replace_commentedKey_basic()
    replace_commentedKey_with_commentedKey()
    get_commentedKey()
    get_commentedKey_with_str()


if __name__ == '__main__':
    lprofiler = LineProfiler()

    lprofiler.add_function(basic_set)
    lprofiler.add_function(commented_set)

    lp_wrapper = lprofiler(main)

    lp_wrapper()

    lprofiler.print_stats()