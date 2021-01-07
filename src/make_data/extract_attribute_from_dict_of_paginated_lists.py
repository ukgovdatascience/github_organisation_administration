from functools import partial
from github import PaginatedList, UnknownObjectException
from src.utils.logger import Log, logger
from src.utils.parallelise_dictionary_processing import parallelise_dictionary_processing
from typing import Any, Dict, List, Optional, Union
import multiprocessing as mp


@Log(logger, level="debug")
def extract_attribute_from_paginated_list_elements(pl: Union[List, PaginatedList.PaginatedList],
                                                   attribute_name: str) -> Optional[List[Any]]:
    """Extract a given attribute from the elements of a `github.PaginatedList.PaginatedList` object.

    Args:
        pl: A list or `github.PaginatedList.PaginatedList` object.
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
def _extract_attributes_from_key_paginated_list_pair(pl: Dict[Any, Union[List, PaginatedList.PaginatedList]],
                                                     attribute_name: str,
                                                     dictionary_key: Any) -> Dict[Any, Optional[List[Any]]]:
    """Extract a given attribute from a list or `github.PaginatedList.PaginatedList` object in a key-value pair.

    Assumed that the list or `github.PaginatedList.PaginatedList` object is the value in the key-value pair.

    Args:
        pl: A dictionary of keys and values, where the values are lists or `github.PaginatedList.PaginatedList` objects.
        attribute_name: A valid attribute of the elements in `pl`.
        dictionary_key: A valid key in `pl`.

    Returns:
        A dictionary of one key-value pair, where the key is `dictionary_key`, and the value is a list of the attribute
        `attribute_name` for each of the elements in `pl`. If an error was returned in the original API request,
        None is returned instead as the value.

    """
    return {dictionary_key: extract_attribute_from_paginated_list_elements(pl[dictionary_key], attribute_name)}


@Log(logger)
def extract_attribute_from_dict_of_paginated_lists(pl: Dict[Any, Union[List, PaginatedList.PaginatedList]],
                                                   attribute_name: str, cpu_count: int = mp.cpu_count(),
                                                   max_chunksize: int = 1000) -> Dict:
    """Extract a given attribute from `github.PaginatedList.PaginatedList` object(s) in a dictionary.

    Args:
        pl: A dictionary of keys and values, where the values are lists or `github.PaginatedList.PaginatedList` objects.
        attribute_name: A valid attribute of the elements in `pl`.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to parallelise the API requests.
        max_chunksize: Default: 1000. The maximum number of repositories per CPU to call.

    Returns:
        A dictionary of key-value pairs, where the keys are the same as in `pl`, but the values are the desired
        attribute `attribute_name` from the `github.PaginatedList.PaginatedList` values of `pl`.

    """

    # Partially complete arguments of the _extract_attributes_from_key_paginated_list_pair function
    partial_extract_attributes_from_key_paginated_list_pair = partial(_extract_attributes_from_key_paginated_list_pair,
                                                                      pl, attribute_name)

    # Parallelise the attribute extraction, and return the compiled output
    return parallelise_dictionary_processing(partial_extract_attributes_from_key_paginated_list_pair,
                                             pl.keys(), cpu_count, max_chunksize)


if __name__ == "__main__":
    from github import Github
    from src.make_data.find_organisation_repos import find_organisation_repos
    from src.make_data.get_items_for_all_repos import get_items_for_all_repos
    import os

    # Load required environment variables
    GITHUB_ORGANISATION = os.getenv("GITHUB_ORGANISATION")

    # Instantiate the github.Github class to gain access to GitHub REST APIv3
    github_object = Github(os.getenv("GITHUB_API_TOKEN"), per_page=100)

    # Get all the repositories for GITHUB_ORGANISATION
    organisation_repositories = find_organisation_repos(github_object, GITHUB_ORGANISATION)

    # Get all the contributors for all repositories, and return a dictionary of key-value pairs of repository full
    # names and contributor lists
    organisation_contributors = get_items_for_all_repos(github_object, "get_contributors", organisation_repositories)

    # Get the full_name attributes of each element in organisation_repositories
    repository_full_names = extract_attribute_from_paginated_list_elements(organisation_repositories, "full_name")

    # Get all the contributor logins for the organisation for each repository
    contributor_logins = extract_attribute_from_dict_of_paginated_lists(organisation_contributors, "login")
