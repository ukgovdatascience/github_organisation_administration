from src.make_data.add_team_with_permissions_to_all_repositories import (
    add_team_with_permissions_to_all_repositories,
    add_team_with_permissions_to_repository,
    check_team_added_already
)
from typing import Any, List
from unittest.mock import MagicMock
import pytest

# Define arguments for the `TestCheckTeamAddedAlready` test class
args_test_check_team_added_already = [
    ("hello", ["foo", "hello", "bar", "world"]),
    ("world", ["foo", "hello", "bar", "world"]),
    ("hello", ["foo", "hello_world", "bar", "world"]),
    ("world", ["foo", "hello", "bar", "hello_world"]),
]


@pytest.mark.parametrize("test_input_team_name, test_input_repository_teams", args_test_check_team_added_already)
class TestCheckTeamAddedAlready:

    @staticmethod
    def create_class_with_get_teams_method(input_teams: List[Any]) -> object:
        """Create a class with a `get_teams` method."""

        class ExampleClass:

            def __init__(self, teams: List[Any]) -> None:
                """Example class that has a get_teams method, and a name attribute."""
                self.teams = teams

            def get_teams(self) -> List[Any]:
                return self.teams

        # Return `ExampleClass`
        return ExampleClass(input_teams)

    def test_extract_attribute_from_paginated_list_elements_called_once_correctly(
            self, patch_add_team_with_permissions_extract_attribute_from_paginated_list_elements: MagicMock,
            test_input_team_name: str, test_input_repository_teams: List[str]
    ) -> None:
        """Test that the `extract_attribute_from_paginated_list_elements` function is called once correctly."""

        # Execute the `check_team_added_already` function
        _ = check_team_added_already(test_input_team_name,
                                     self.create_class_with_get_teams_method(test_input_repository_teams))

        # Assert that the `extract_attribute_from_paginated_list_elements` is called once correctly
        patch_add_team_with_permissions_extract_attribute_from_paginated_list_elements.assert_called_once_with(
            self.create_class_with_get_teams_method(test_input_repository_teams).get_teams(), "name"
        )

    @staticmethod
    def create_list_of_classes_with_name(input_list: List[str]) -> List[object]:
        """Create a list of classes with a set attribute based on an input list."""

        class ExampleSubClass:

            def __init__(self, name: str) -> None:
                """Example class that only has one attribute, `name`."""
                self.name = name

        # Return a list of `ExampleClasses` based on each element of input_list
        return [ExampleSubClass(e)for e in input_list]

    def test_returns_correctly(self, test_input_team_name: str, test_input_repository_teams: List[str]) -> None:
        """Test the function returns correctly."""

        # Create a repository input for the `check_team_added_already` that is a class that has a `get_teams` method,
        # where this method returns a list of classes each with a `name` attribute
        test_input_repository = self.create_class_with_get_teams_method(
            self.create_list_of_classes_with_name(test_input_repository_teams)
        )

        # Define the expected output
        test_expected = test_input_team_name in test_input_repository_teams

        # Execute the `check_team_added_already` function, and assert it is as expected
        assert check_team_added_already(test_input_team_name, test_input_repository) == test_expected


class ExampleTeamClass:

    def __init__(self, name: str) -> None:
        """Define an example team class with `name` attribute, and `add_to_repos` and `set_repo_permission` methods."""
        self.name = name

    @staticmethod
    def add_to_repos(entry: Any) -> Any:
        return entry

    @staticmethod
    def set_repo_permission(*args: Any, **kwargs: Any) -> Any:
        return args, kwargs


# Define test cases for the `TestAddTeamWithPermissionsToRepository` test class
args_test_add_team_with_permissions_to_repository = [
    ("hello", "world", "foo", True),
    ("world", "foo", "bar", False)
]


@pytest.mark.parametrize("test_input_team_name, test_input_permission, test_input_repository, test_input_check",
                         args_test_add_team_with_permissions_to_repository)
class TestAddTeamWithPermissionsToRepository:

    def test_check_team_added_already_called_once_correctly(
            self, patch_check_team_added_already: MagicMock, test_input_team_name: str, test_input_permission: str,
            test_input_repository: str, test_input_check: bool
    ) -> None:
        """Test the `check_team_added_already` function is called once correctly."""

        # Set the return value of `patch_check_team_added_already` to `test_input_check`
        patch_check_team_added_already.return_value = test_input_check

        # Execute the `add_team_with_permissions_to_repository` function
        add_team_with_permissions_to_repository(ExampleTeamClass(test_input_team_name), test_input_permission,
                                                test_input_repository)

        # Assert that the `check_team_added_already` function is called once correctly
        patch_check_team_added_already.assert_called_once_with(test_input_team_name, test_input_repository)

    def test_add_to_repos_called_only_if_check_team_added_already_false(
            self, patch_check_team_added_already: MagicMock, test_input_team_name: str, test_input_permission: str,
            test_input_repository: str, test_input_check: bool
    ) -> None:
        """Test that the `add_to_repos` method is called once correctly only if `check_team_added_already` is False."""

        # Set the return value of `patch_check_team_added_already` to `test_input_check`
        patch_check_team_added_already.return_value = test_input_check

        # Create a MagicMock, and add a `name` attribute
        test_input_team = MagicMock()
        test_input_team.name = test_input_team_name

        # Execute the `add_team_with_permissions_to_repository` function
        add_team_with_permissions_to_repository(test_input_team, test_input_permission, test_input_repository)

        # Assert that the `add_to_repos` method is not called if `check_team_added_already` returns True, otherwise
        # check it is called once correctly
        if test_input_check:
            assert not test_input_team.add_to_repos.called
        else:
            test_input_team.add_to_repos.assert_called_once_with(test_input_repository)

    def test_set_repo_permission_called_once_correctly(
            self, patch_check_team_added_already: MagicMock, test_input_team_name: str, test_input_permission: str,
            test_input_repository: str, test_input_check: bool
    ) -> None:
        """Test that the `set_repo_permission` method is called once correctly."""

        # Set the return value of `patch_check_team_added_already` to `test_input_check`
        patch_check_team_added_already.return_value = test_input_check

        # Create a MagicMock, and add a `name` attribute
        test_input_team = MagicMock()
        test_input_team.name = test_input_team_name

        # Execute the `add_team_with_permissions_to_repository` function
        add_team_with_permissions_to_repository(test_input_team, test_input_permission, test_input_repository)

        # Assert the `set_repo_permission` method is called once correctly
        test_input_team.set_repo_permission.assert_called_once_with(test_input_repository, test_input_permission)


# Define test cases for the `TestAddTeamWithPermissionsToAllRepositories` test class
args_test_add_team_with_permissions_to_all_repositories = [
    ("hello", "world", ["foo", "bar", "hello_world"], 2, 4),
    ("world", "foo", ["bar", "hello_world", "foo_bar", "hello"], 1, 3)
]


@pytest.mark.parametrize("test_input_team, test_input_permission, test_input_repositories, test_input_cpu_count, "
                         "test_input_max_chunksize", args_test_add_team_with_permissions_to_all_repositories)
class TestAddTeamWithPermissionsToAllRepositories:

    def test_partial_called_once_correctly(
            self, patch_add_team_with_permissions_to_all_repositories_partial: MagicMock,
            patch_add_team_with_permissions_to_repository: MagicMock,
            patch_add_team_with_permissions_to_all_repositories_parallelise_processing: MagicMock,
            test_input_team: str, test_input_permission: str, test_input_repositories: List[str],
            test_input_cpu_count: int, test_input_max_chunksize: int
    ) -> None:
        """Test that `functools.partial` function is called once correctly."""

        # Execute the `add_team_with_permissions_to_all_repositories` function
        add_team_with_permissions_to_all_repositories(test_input_team, test_input_permission, test_input_repositories,
                                                      test_input_cpu_count, test_input_max_chunksize)

        # Assert that `functools.partial` is called once with the correct arguments
        patch_add_team_with_permissions_to_all_repositories_partial.assert_called_once_with(
            patch_add_team_with_permissions_to_repository, test_input_team, test_input_permission
        )

    def test_parallelise_processing_called_once_correctly(
            self, patch_add_team_with_permissions_to_all_repositories_partial: MagicMock,
            patch_add_team_with_permissions_to_repository: MagicMock,
            patch_add_team_with_permissions_to_all_repositories_parallelise_processing: MagicMock,
            test_input_team: str, test_input_permission: str, test_input_repositories: List[str],
            test_input_cpu_count: int, test_input_max_chunksize: int
    ) -> None:
        """Test that `parallelise_processing` function is called once correctly."""

        # Execute the `add_team_with_permissions_to_all_repositories` function
        add_team_with_permissions_to_all_repositories(test_input_team, test_input_permission, test_input_repositories,
                                                      test_input_cpu_count, test_input_max_chunksize)

        # Assert that `parallelise_processing` is called once with the correct arguments
        patch_add_team_with_permissions_to_all_repositories_parallelise_processing.assert_called_once_with(
            patch_add_team_with_permissions_to_all_repositories_partial.return_value, test_input_repositories,
            test_input_cpu_count, test_input_max_chunksize
        )
