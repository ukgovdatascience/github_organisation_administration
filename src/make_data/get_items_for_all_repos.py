from functools import partial
from github import Github, PaginatedList
from src.make_data.get_items_for_repo import get_items_for_repo
from src.utils.logger import Log, logger
from typing import Any, Dict, List
import multiprocessing as mp


@Log(logger)
def get_items_for_all_repos(g: Github, method_name: str, repositories: PaginatedList.PaginatedList,
                            cpu_count: int = mp.cpu_count(), max_chunksize: int = 1000) -> Dict[str, List[Any]]:
    """Get all the items for a list of GitHub repositories, where items is the output from `method_name`.

    Args:
        g: A `github.Github` class object initialised with a GitHub username and personal access token with the
            necessary permissions.
        method_name: A method of the github.Repository.Repository class.
        repositories: A list of GitHub repositories as a `github.PaginatedList.PaginatedList` object.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to parallelise the API requests.
        max_chunksize: Default: 1000. The maximum number of repositories per CPU to call.

    Returns:
        A dictionary where the GitHub repositories' full names are keys, and their items are values.

    """

    # Compile the full names from each GitHub repository in repositories
    repositories_full_names = [r.full_name for r in repositories]

    # Partially complete the get_items_for_repo function with g, and method_name
    partial_get_items_for_repo = partial(get_items_for_repo, g, method_name)

    # Calculate the number of chunks to be sent to each process; if this exceeds max_chunksize, set to max_chunksize
    chunk_size = len(repositories_full_names) / cpu_count
    chunk_size = min(int(chunk_size) + bool(chunk_size), max_chunksize)

    # Set up a multiprocessing.Pool object, and use it to get items for each repository in parallel
    with mp.Pool(cpu_count) as pool:
        mp_items = list(pool.imap_unordered(partial_get_items_for_repo, repositories_full_names, chunksize=chunk_size))

    # Collapse the list of dictionaries in mp_items into a single dictionary - assumes there are no duplicate keys
    repositories_items = {k: v for d in mp_items for k, v in d.items()}

    # Assert that the above assumption is correct; if so return repositories_items
    assert len(repositories_items) == len(mp_items), "Repository names are not unique!"
    return repositories_items


if __name__ == "__main__":
    from src.make_data.find_organisation_repos import find_organisation_repos
    from src.utils.parse_api_token import parse_api_token
    import os

    # Load required environment variables
    GITHUB_ORGANISATION = os.getenv("GITHUB_ORGANISATION")

    # Get GitHub username and personal access token from a JSON file
    GITHUB_USER, GITHUB_TOKEN = parse_api_token(os.getenv("GITHUB_API_TOKEN"))

    # Instantiate the github.Github class to gain access to GitHub REST APIv3
    github_object = Github(GITHUB_USER, GITHUB_TOKEN, per_page=100)

    # Get all the repositories for GITHUB_ORGANISATION
    organisation_repositories = find_organisation_repos(github_object, GITHUB_ORGANISATION)

    # Get all the contributors for all repositories, and return a dictionary of key-value pairs of repository full
    # names and contributor lists
    organisation_contributors = get_items_for_all_repos(github_object, "get_contributors", organisation_repositories)
