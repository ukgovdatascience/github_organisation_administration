from github import Github, NamedUser, PaginatedList
from src.utils.logger import Log, logger
from typing import Dict, Union


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

    # Get repository full names
    organisation_repository_names = [r.full_name for r in organisation_repositories]

    # Get all the contributors for the first repository, and return a dictionary of key-value pairs of repository full
    # names and contributor lists
    first_repo_contributors = get_contributors_for_repo(github_object, organisation_repository_names[0])
