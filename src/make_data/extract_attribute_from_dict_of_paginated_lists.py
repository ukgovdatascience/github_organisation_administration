from functools import partial
from github import PaginatedList, UnknownObjectException
from src.utils.logger import Log, logger
from src.utils.parallelise_dictionary_processing import parallelise_dictionary_processing
from typing import Any, Dict, List, Optional
import multiprocessing as mp


@Log(logger, level="debug")
def extract_attribute_from_paginated_list_elements(pl: PaginatedList.PaginatedList,
                                                   attribute_name: str) -> Optional[List[Any]]:
    """Extract a given attribute from the elements of a github.PaginatedList.PaginatedList object.

    Args:
        pl: A github.PaginatedList.PaginatedList object.
        attribute_name: A valid attribute of the elements in `pl`.

    Returns:
        A list of the attribute `attribute_name` for each of the elements in `pl`. If an error was returned in the
        original API request, None is returned instead.

    """

    # Return the attribute attribute_name from each element of pl; if an error was returned in the API request, return
    # None instead of raising the UnknownObjectException exception
    try:
        return [getattr(e, attribute_name) for e in pl]
    except UnknownObjectException:
        return None


@Log(logger, level="debug")
def _extract_attributes_from_key_paginated_list_pair(pl: Dict[Any, PaginatedList.PaginatedList], attribute_name: str,
                                                     dictionary_key: Any) -> Dict[Any, Optional[List[Any]]]:
    """Extract a given attribute from the elements of a github.PaginatedList.PaginatedList object in a key-value pair.

    Assumed that the github.PaginatedList.PaginatedList object is the value in the key-value pair.

    Args:
        pl: A dictionary of keys and values, where the values are github.PaginatedList.PaginatedList objects.
        attribute_name: A valid attribute of the elements in `pl`.
        dictionary_key: A valid key in `pl`.

    Returns:
        A dictionary of one key-value pair, where the key is `dictionary_key`, and the value is a list of the attribute
        `attribute_name` for each of the elements in `pl`. If an error was returned in the original API request,
        None is returned instead as the value.

    """
    return {dictionary_key: extract_attribute_from_paginated_list_elements(pl[dictionary_key], attribute_name)}


@Log(logger)
def extract_attribute_from_dict_of_paginated_lists(pl: Dict[Any, PaginatedList.PaginatedList], attribute_name: str,
                                                   cpu_count: int = mp.cpu_count(), max_chunksize: int = 1000) -> Dict:
    """Extract a given attribute from github.PaginatedList.PaginatedList object(s) in a dictionary.

    Args:
        pl: A dictionary of keys and values, where the values are github.PaginatedList.PaginatedList objects.
        attribute_name: A valid attribute of the elements in `pl`.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to parallelise the API requests.
        max_chunksize: Default: 1000. The maximum number of repositories per CPU to call.

    Returns:
        A dictionary of key-value pairs, where the keys are the same as in `pl`, but the values are the desired
        attribute `attribute_name` from the github.PaginatedList.PaginatedList values of `pl`.

    """

    # Partially complete arguments of the _extract_attributes_from_key_paginated_list_pair function
    partial_extract_attributes_from_key_paginated_list_pair = partial(_extract_attributes_from_key_paginated_list_pair,
                                                                      pl, attribute_name)

    # Parallelise the attribute extraction, and return the compiled output
    return parallelise_dictionary_processing(partial_extract_attributes_from_key_paginated_list_pair,
                                             pl.keys(), cpu_count, max_chunksize)
