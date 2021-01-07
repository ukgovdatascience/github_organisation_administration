from github import Github
from src.utils.logger import Log, logger
from typing import Any, Dict


@Log(logger, level="debug")
def get_items_for_repo(g: Github, method_name: str, repository_name: str) -> Dict[str, Any]:
    """Get all values of an item for a GitHub repository, where items is the output from `method_name`.

    Args:
        g: A `github.Github` class object initialised with a GitHub username and personal access token with the
            necessary permissions.
        method_name: A method of the github.Repository.Repository class.
        repository_name: A Github repository name.

    Returns:
        A dictionary where the key is the repository name, and the value is the result of executing method_name on a
        GitHub repository called repository_name.

    """
    return {repository_name: getattr(g.get_repo(repository_name), method_name)()}


if __name__ == "__main__":
    from src.make_data.find_organisation_repos import find_organisation_repos
    import os

    # Load required environment variables
    GITHUB_ORGANISATION = os.getenv("GITHUB_ORGANISATION")

    # Instantiate the github.Github class to gain access to GitHub REST APIv3
    github_object = Github(os.getenv("GITHUB_API_KEY"), per_page=100)

    # Get all the repositories for GITHUB_ORGANISATION
    organisation_repositories = find_organisation_repos(github_object, GITHUB_ORGANISATION)

    # Get repository full names
    organisation_repository_names = [r.full_name for r in organisation_repositories]

    # Get all the contributors for the first repository, and return a dictionary of key-value pairs of repository full
    # names and contributor lists
    first_repo_contributors = get_items_for_repo(github_object, "get_contributors", organisation_repository_names[0])
