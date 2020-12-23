from functools import partial
from github import Github, NamedUser, PaginatedList
from src.utils.logger import Log, logger
from typing import Dict, List, Union
import multiprocessing as mp


@Log(logger, level="debug")
def get_contributors_for_repo(g: Github, repository_name: str) -> Dict[str, Union[PaginatedList.PaginatedList,
                                                                                  NamedUser.NamedUser]]:
    """Get all contributors for a GitHub repository.

    Args:
        g: A `github.Github` class object initialised with a GitHub username and personal access token with the
            necessary permissions.
        repository_name: A Github repository name.

    Returns:
        A `github.PaginatedList.PaginatedList` or `NamedUser.NamedUser` object containing the contributors in a GitHub
        repository.

    """

    # Get the repository
    g_repository = g.get_repo(repository_name)

    # Return a dictionary of the repository name as a key with the contributors as the values
    return {repository_name: g_repository.get_contributors()}


@Log(logger)
def get_contributors_for_all_repos(g: Github, repositories: PaginatedList.PaginatedList,
                                   cpu_count: int = mp.cpu_count()) -> Dict[str, List[str]]:
    """Get all the contributors for a list of GitHub repositories.

    Args:
        g: A `github.Github` class object initialised with a GitHub username and personal access token with the
            necessary permissions.
        repositories: A list of GitHub repositories as a `github.PaginatedList.PaginatedList` object.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to paralleise the API requests.

    Returns:
        A dictionary where the GitHub repositories' full names are keys, and their contributors are values.

    """

    # Compile the full names from each Repository in repositories
    repositories_full_names = [r.full_name for r in repositories]

    # Partially complete the get_contributors_for_repo function with the github_object
    partial_get_contributors_for_repo = partial(get_contributors_for_repo, g)

    # Set up a multiprocessing.Pool object, and use it to get contributors for each repository in parallel
    with mp.Pool(cpu_count) as pool:
        mp_contributors = list(pool.imap_unordered(partial_get_contributors_for_repo, repositories_full_names))

    # Collapse the list of dictionaries in mp_contributors into a single dictionary - assumes there are no duplicate
    # keys in mp_contributors
    repositories_contributors = {k: v for d in mp_contributors for k, v in d.items()}

    # Assert that the above assumption is correct; if so return repositories_contributors
    assert len(repositories_contributors) == len(mp_contributors), "Repository names are not unique!"
    return repositories_contributors


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
    organisation_contributors = get_contributors_for_all_repos(github_object, organisation_repositories)
