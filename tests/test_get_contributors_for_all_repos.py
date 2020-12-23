from itertools import cycle, islice
from src.make_data.get_contributors_for_all_repos import get_contributors_for_all_repos, get_contributors_for_repo
from typing import Any, List
from unittest.mock import MagicMock
import pytest

# Define test cases for the TestGetContributorsForRepos test class
args_test_get_contributors_for_repos_repository_name = ["hello", "world"]


@pytest.mark.parametrize("test_input_repository_name", args_test_get_contributors_for_repos_repository_name)
class TestGetContributorsForRepos:

    def test_get_repo_called_correctly(self, patch_get_contributors_for_all_repos_github: MagicMock,
                                       test_input_repository_name: str) -> None:
        """Test that the github.Github.get_repo method is called once correctly."""

        # Execute the get_contributors_for_repo function
        _ = get_contributors_for_repo(patch_get_contributors_for_all_repos_github, test_input_repository_name)

        # Assert that the github.Github.get_repo method is called once with the correct arguments
        patch_get_contributors_for_all_repos_github.get_repo.assert_called_once_with(test_input_repository_name)

    def test_returns_correctly(self, patch_get_contributors_for_all_repos_github: MagicMock,
                               test_input_repository_name: str) -> None:
        """Test the output of the function is as expected."""

        # Define the expected value of the output dictionary
        test_expected_value = patch_get_contributors_for_all_repos_github.get_repo.return_value.get_contributors()

        # Execute the get_contributors_for_repo function
        test_output = get_contributors_for_repo(patch_get_contributors_for_all_repos_github, test_input_repository_name)

        # Assert the return is as expected
        assert test_output == {test_input_repository_name: test_expected_value}


# Define test cases for the TestGetContributorsForRepos test class
args_test_get_contributors_for_all_repos_repositories = [
    ["hello", "world"],
    ["foo", "bar"],
    ["hello", "world", "foo", "bar"],
    ["hello_world", "foo_bar"]
]
args_test_get_contributors_for_all_repos_cpu_count = [*range(1, 8, 2)]
args_test_get_contributors_for_all_repos_duplicates = [*range(1, 4)]


@pytest.mark.parametrize("test_input_repositories", args_test_get_contributors_for_all_repos_repositories)
@pytest.mark.parametrize("test_input_cpu_count", args_test_get_contributors_for_all_repos_cpu_count)
class TestGetContributorsForAllRepos:

    @staticmethod
    def create_list_of_classes_with_full_name(input_list: List[Any]) -> List[MagicMock]:
        """Create a list of MagicMocks with a set attribute based on an input list."""

        class ExampleClass:

            def __init__(self, full_name: str) -> None:
                """Example class that only has one attribute, `full_name`.

                Args:
                    full_name: An example full name

                """
                self.full_name = full_name

        # Return a list of ExampleClasses based on each element of input_list
        return [ExampleClass(e)for e in input_list]

    def test_partial_called_correctly(self, patch_get_contributors_for_all_repos_github: MagicMock,
                                      patch_get_contributors_for_repo: MagicMock,
                                      patch_get_contributors_for_all_repos_partial: MagicMock,
                                      patch_multiprocessing_pool: MagicMock, test_input_repositories: List[str],
                                      test_input_cpu_count: int) -> None:
        """Test that functools.partial function is called once correctly."""

        # Execute the get_contributors_for_all_repos function
        _ = get_contributors_for_all_repos(patch_get_contributors_for_all_repos_github,
                                           self.create_list_of_classes_with_full_name(test_input_repositories),
                                           test_input_cpu_count)

        # Assert that functools.partial is called once with the correct arguments
        patch_get_contributors_for_all_repos_partial.assert_called_once_with(
            patch_get_contributors_for_repo, patch_get_contributors_for_all_repos_github
        )

    def test_pool_called_once_correctly(self, patch_get_contributors_for_all_repos_github: MagicMock,
                                        patch_get_contributors_for_repo: MagicMock,
                                        patch_get_contributors_for_all_repos_partial: MagicMock,
                                        patch_multiprocessing_pool: MagicMock, test_input_repositories: List[str],
                                        test_input_cpu_count: int) -> None:
        """Test multiprocessing.Pool is called once correctly."""

        # Execute the get_contributors_for_all_repos function
        _ = get_contributors_for_all_repos(patch_get_contributors_for_all_repos_github,
                                           self.create_list_of_classes_with_full_name(test_input_repositories),
                                           test_input_cpu_count)

        # Assert multiprocessing.Pool is called once with the correct arguments
        patch_multiprocessing_pool.assert_called_once_with(test_input_cpu_count)

    def test_imap_unordered_called_correctly(self, patch_get_contributors_for_all_repos_github: MagicMock,
                                             patch_get_contributors_for_repo: MagicMock,
                                             patch_get_contributors_for_all_repos_partial: MagicMock,
                                             patch_multiprocessing_pool_enter_imap_unordered: MagicMock,
                                             test_input_repositories: List[str],
                                             test_input_cpu_count: int) -> None:
        """Test multiprocessing.Pool.imap_unordered is called correctly."""

        # Execute the get_contributors_for_all_repos function
        _ = get_contributors_for_all_repos(patch_get_contributors_for_all_repos_github,
                                           self.create_list_of_classes_with_full_name(test_input_repositories),
                                           test_input_cpu_count)

        # Assert multiprocessing.Pool.imap_unordered is called with the correct arguments
        patch_multiprocessing_pool_enter_imap_unordered.assert_called_once_with(
            patch_get_contributors_for_all_repos_partial.return_value, test_input_repositories
        )

    @pytest.mark.parametrize("test_input_duplicates", args_test_get_contributors_for_all_repos_duplicates)
    def test_assertion_error_raised_for_duplicate_keys(self, patch_get_contributors_for_all_repos_github: MagicMock,
                                                       patch_get_contributors_for_repo: MagicMock,
                                                       patch_get_contributors_for_all_repos_partial: MagicMock,
                                                       patch_multiprocessing_pool_enter_imap_unordered: MagicMock,
                                                       test_input_repositories: List[str], test_input_cpu_count: int,
                                                       test_input_duplicates: int) -> None:
        """Test an AssertionError is raised if duplicate keys (repository names) are returned."""

        # Generate duplicate repositories
        test_input_duplicate_repositories = islice(cycle(test_input_repositories),
                                                   len(test_input_repositories) + test_input_duplicates)

        # Set the return value of patch_multiprocessing_pool_enter_imap_unordered
        patch_multiprocessing_pool_enter_imap_unordered.return_value = (
            {r: ["octocat"]} for r in test_input_duplicate_repositories
        )

        # Execute the get_contributors_for_all_repos function, checking that it raises an AssertionError
        with pytest.raises(AssertionError):
            _ = get_contributors_for_all_repos(patch_get_contributors_for_all_repos_github,
                                               self.create_list_of_classes_with_full_name(test_input_repositories),
                                               test_input_cpu_count)

    def test_returns_correctly(self, patch_get_contributors_for_all_repos_github: MagicMock,
                               patch_get_contributors_for_repo: MagicMock,
                               patch_get_contributors_for_all_repos_partial: MagicMock,
                               patch_multiprocessing_pool_enter_imap_unordered: MagicMock,
                               test_input_repositories: List[str], test_input_cpu_count: int) -> None:
        """Test the output of the function is as expected."""

        # Set the return value of patch_multiprocessing_pool_enter_imap_unordered
        patch_multiprocessing_pool_enter_imap_unordered.return_value = (
            {r: ["octocat"]} for r in test_input_repositories
        )

        # Execute the get_contributors_for_all_repos function
        test_output = get_contributors_for_all_repos(
            patch_get_contributors_for_all_repos_github,
            self.create_list_of_classes_with_full_name(test_input_repositories),
            test_input_cpu_count
        )

        # Assert the output is as expected
        assert test_output == {r: ["octocat"] for r in test_input_repositories}
