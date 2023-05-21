from functools import reduce
from typing import Hashable, List, Optional, Tuple, Union


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


def sort_mixed_list(
    num: Union[int, float, str]
) -> Tuple[int, Union[int, float, str], str]:
    try:
        ele = int(num)
        return 0, ele, ""
    except ValueError:
        return 1, num, ""


def extract_nested_dict(
    data: dict,
    path: Optional[str] = None,
    keys: Optional[List[Hashable]] = None,
    path_sep: str = "/",
) -> Union[str, int, float, dict]:
    """
    Extract a value from a nested dictionary

    The keys for the nested structure can be provided as a string or a list. Providing as a string can only work
    if all the keys are strings. The path parameter will be split by the path_sep parameter t0 generate a list of keys.
    If the expected keys are not strings, then supply the keys as a list to the keys parameter. The list of keys
    should be in order of appearance in the dictionary.

    :param data: the nested dictionary
    :type data: dict
    :param path: string of concatenated keys
    :type path: str
    :param keys: list of keys
    :type keys: list
    :param path_sep: the separator to use if keys provided as path
    :type path_sep: str
    :return: the value after moving through the nested dictionary via the keys
    :rtype: Union[str, int, float, dict]
    :raises TypeError, KeyError
    """
    if keys is None and path is None:
        raise TypeError(
            "Please provide either a path of joined keys as a string or a list of hashables."
        )

    if keys is None:
        if not isinstance(path, str):
            raise TypeError(
                f"Please provide the path parameter as a string, not a {type(path)}"
            )
        try:
            value = reduce(lambda d, k: d[k], path.split(path_sep), data)
        except KeyError:
            raise KeyError(f"One of the keys in {path} is not in the dictionary!")
    else:
        if not isinstance(keys, list):
            raise TypeError(
                f"Please provide the keys parameter as a list, not a {type(keys)}"
            )
        try:
            value = reduce(lambda d, k: d[k], keys, data)
        except KeyError:
            raise KeyError(f"One of the keys in {keys} is not in the dictionary!")

    return value


def order_keys(data: dict, keys: List[Hashable]) -> List[Hashable]:
    """
    Order a list of dictionary keys so that the order of keys reflects the order in which the keys appear in the
    nested dictionary

    :param data: input nested dictionary
    :type data: dict
    :param keys: list of keys which are not in the right order
    :type keys: List[Hashable]
    :return: list of Hashables in correct order
    :rtype: List[Hashable]
    :raises: KeyError
    """
    remaining_keys = keys.copy()
    ordered_keys: List[Hashable] = []
    while len(remaining_keys) > 0:
        if len(ordered_keys) > 0:
            sub = extract_nested_dict(data, keys=ordered_keys)
        else:
            sub = data.copy()

        if isinstance(sub, dict):
            added_key = False
            for i in remaining_keys:
                value = sub.get(i, None)
                if value is not None:
                    added_key = True
                    ordered_keys.append(i)
                    remaining_keys.remove(i)
                    break
            if not added_key:
                break
        else:
            break
    if len(remaining_keys) != 0:
        raise KeyError(
            f"Keys could not be ordered due to incorrect keys! The following keys remained {remaining_keys}"
        )
    return ordered_keys
