from functools import partial
from github import PaginatedList, Repository, Team
from src.make_data.extract_attribute_from_dict_of_paginated_lists import extract_attribute_from_paginated_list_elements
from src.utils.logger import Log, logger
from src.utils.parallelise_dictionary_processing import parallelise_processing
import multiprocessing as mp


@Log(logger, level="debug")
def check_team_added_already(team_name: str, repository: Repository.Repository) -> bool:
    """Check if a GitHub organisation team already exists in a GitHub repository.

    Args:
        team_name: A GitHub organisation team name.
        repository: A `github.Repository.Repository` object of the GitHub repository of interest.

    Returns:
        True/False depending on whether `team_name` exists as the name of a GitHub organisation team within the GitHub
        repository `repository`.

    """
    return team_name in extract_attribute_from_paginated_list_elements(repository.get_teams(), "name")


@Log(logger, level="debug")
def add_team_with_permissions_to_repository(team: Team.Team, permission: str,
                                            repository: Repository.Repository) -> None:
    """Add a team to a GitHub repository if it isn't already added, and set its permission level.

    Args:
        team: A `github.Team.Team` object containing the GitHub organisation team to add to the repository with set
            permissions.
        permission: A permission level to provide the `team` within `repository`. See the `GitHub API documentation`_
            for possible options.
        repository: A `github.Repository.Repository` object containing the GitHub organisation repository of interest.

    Returns:
        None. `repository` will have `team` with `permission` access to it.

    .. _GitHub API documentation:
        https://docs.github.com/en/free-pro-team@latest/rest/reference/teams#add-or-update-team-repository-permissions

    """

    # Check if the team already exists in the repository - if not, add the team to the repository
    if not check_team_added_already(team.name, repository):
        team.add_to_repos(repository)

    # Set the team repository permission to permission
    team.set_repo_permission(repository, permission)


@Log(logger)
def add_team_with_permissions_to_all_repositories(team: Team.Team, permission: str,
                                                  repositories: PaginatedList.PaginatedList,
                                                  cpu_count: int = mp.cpu_count(), max_chunksize: int = 1000) -> None:
    """Add a team to a list of GitHub repositories if it isn't already added, and set its permission level.

    Args:
        team: A `github.Team.Team` object containing the GitHub organisation team to add to the repository with set
            permissions.
        permission: A permission level to provide the `team` within `repository`. See the `GitHub API
            documentation`_ for possible options.
        repositories: A `github.PaginatedList.PaginatedList` objects containing `github.Repository.Repository`
            objects of the GitHub organisation repositories.
        cpu_count: Default: maximum number of CPUs. The number of CPUs to parallelise the processing.
        max_chunksize: Default: 1000. The maximum number of iterables per CPU.

    Returns:
        None. Each repository in `repositories` will have `team` with `permission` access to it.

    .. _GitHub API documentation:
        https://docs.github.com/en/free-pro-team@latest/rest/reference/teams#add-or-update-team-repository-permissions

    """

    # Partially complete the first two arguments of the `add_team_with_permissions_to_repository` function
    partial_add_team_with_permissions_to_repository = partial(add_team_with_permissions_to_repository, team, permission)

    # Parallelise the request to set all repositories with `team` having `permission` permissions
    _ = parallelise_processing(partial_add_team_with_permissions_to_repository, repositories, cpu_count, max_chunksize)
