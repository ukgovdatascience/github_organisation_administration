from github import Github, PaginatedList, Repository
from src.utils.logger import Log, logger
from typing import Union


@Log(logger)
def find_organisation_repos(g: Github, organisation: str, repository_type: str = "all", sort: str = "full_name",
                            direction: str = "asc") -> Union[PaginatedList.PaginatedList, Repository.Repository]:
    """Get repositories for a GitHub organisation.

    For accepted string values for `repository_type`, `sort`, and `direction`, see the `GitHub REST API Reference`_.

    Args:
        g: A `github.Github` class object initialised with a GitHub username and personal access token with the
            necessary permissions.
        organisation: A GitHub organisation name.
        repository_type: The repository types required.
        sort: How the return should be sorted.
        direction: The direction of `sort`.

    Returns:
        A `github.PaginatedList.PaginatedList` or `github.Repository.Repository` object containing the GitHub
        repositories in a GitHub organisation.

    .. _GitHub REST API Reference:
        https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#list-organization-repositories

    """

    # Get the organisation
    g_organisation = g.get_organization(organisation)

    # Return all repositories
    return g_organisation.get_repos(repository_type, sort, direction)


if __name__ == "__main__":
    import os

    # Load required environment variables
    GITHUB_ORGANISATION = os.getenv("GITHUB_ORGANISATION")

    # Instantiate the github.Github class to gain access to GitHub REST APIv3
    github_object = Github(os.getenv("GITHUB_API_KEY"), per_page=100)

    # Get all the repositories for GITHUB_ORGANISATION
    organisation_repositories = find_organisation_repos(github_object, GITHUB_ORGANISATION)
