from functools import partial
from github import Github, PaginatedList
from src.make_data.get_items_for_repo import get_items_for_repo
from src.utils.logger import Log, logger
from src.utils.parallelise_dictionary_processing import parallelise_dictionary_processing
from typing import Any, Dict, List, Union
import multiprocessing as mp


@Log(logger)
def get_items_for_all_repos(g: Github, method_name: str, repositories: Union[List, PaginatedList.PaginatedList],
                            cpu_count: int = mp.cpu_count(), max_chunksize: int = 1000) -> Dict[str, List[Any]]:
    """Get all the items for a list of GitHub repositories, where items is the output from `method_name`.

    Args:
        g: A `github.Github` class object initialised with a GitHub username and personal access token with the
            necessary permissions.
        method_name: A method of the github.Repository.Repository class.
        repositories: A list of `github.Repository.Repository` repositories as a list or
            `github.PaginatedList.PaginatedList` object.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to parallelise the API requests.
        max_chunksize: Default: 1000. The maximum number of repositories per CPU to call.

    Returns:
        A dictionary where the GitHub repositories' full names are keys, and their items are values.

    """

    # Compile the full names from each GitHub repository in repositories
    repositories_full_names = [r.full_name for r in repositories]

    # Partially complete the get_items_for_repo function with g, and method_name
    partial_get_items_for_repo = partial(get_items_for_repo, g, method_name)

    # Parallelise the API request, and return the compiled output
    return parallelise_dictionary_processing(partial_get_items_for_repo, repositories_full_names, cpu_count,
                                             max_chunksize)


if __name__ == "__main__":
    from src.make_data.find_organisation_repos import find_organisation_repos
    import os

    # Load required environment variables
    GITHUB_ORGANISATION = os.getenv("GITHUB_ORGANISATION")

    # Instantiate the github.Github class to gain access to GitHub REST APIv3
    github_object = Github(os.getenv("GITHUB_API_KEY"), per_page=100)

    # Get all the repositories for GITHUB_ORGANISATION
    organisation_repositories = find_organisation_repos(github_object, GITHUB_ORGANISATION)

    # Get all the contributors for all repositories, and return a dictionary of key-value pairs of repository full
    # names and contributor lists
    organisation_contributors = get_items_for_all_repos(github_object, "get_contributors", organisation_repositories)
