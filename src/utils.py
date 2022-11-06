from typing import Tuple, Union

def prettyType(obj: object) -> str:
    """
    Return the type of an object as a string
    :param obj: object to get the type of
    :type obj: Any
    :return: the type of the object
    :rtype: str
    """
    return type(obj).__name__


def simpleType(obj: object) -> type:
    """
    Return the type of an object
    :param obj: the object to get the type of
    :type obj: Any
    :return: the type of the object
    :rtype: type
    """
    return type(obj)


def sort_mixed_list(num: Union[int, float, str]) -> Tuple[int, Union[int, float, str], str]:
    try:
        ele = int(num)
        return 0, ele, ''
    except ValueError:
        return 1, num, ''
