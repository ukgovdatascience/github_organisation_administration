from src.make_data.get_items_for_all_repos import get_items_for_all_repos
from typing import Any, List
from unittest.mock import MagicMock
import pytest

# Define test cases for the TestGetItemsForAllRepos test class
args_test_get_items_for_all_repos_repositories = [
    ["hello", "world"],
    ["foo", "bar"],
    ["hello", "world", "foo", "bar"],
    ["hello_world", "foo_bar"]
]
args_test_get_items_for_all_repos_method_name = ["hello", "world"]
args_test_get_items_for_all_repos_cpu_count = [*range(1, 8, 2)]
args_test_parallelise_dictionary_processing = [1, 4, 8]
args_test_get_items_for_all_repos_duplicates = [*range(1, 4)]


@pytest.mark.parametrize("test_input_repositories", args_test_get_items_for_all_repos_repositories)
@pytest.mark.parametrize("test_input_method_name", args_test_get_items_for_all_repos_method_name)
@pytest.mark.parametrize("test_input_cpu_count", args_test_get_items_for_all_repos_cpu_count)
@pytest.mark.parametrize("test_input_max_chunksize", args_test_parallelise_dictionary_processing)
class TestGetItemsForAllRepos:

    @staticmethod
    def create_list_of_classes_with_full_name(input_list: List[Any]) -> List[object]:
        """Create a list of classes with a set attribute based on an input list."""

        class ExampleClass:

            def __init__(self, full_name: str) -> None:
                """Example class that only has one attribute, `full_name`.

                Args:
                    full_name: An example full name

                """
                self.full_name = full_name

        # Return a list of ExampleClasses based on each element of input_list
        return [ExampleClass(e)for e in input_list]

    def test_partial_called_correctly(self, patch_get_items_for_all_repos_github: MagicMock,
                                      patch_get_items_for_repo: MagicMock,
                                      patch_get_items_for_all_repos_partial: MagicMock,
                                      patch_get_items_for_all_repo_parallelise_dictionary_processing: MagicMock,
                                      test_input_method_name: str, test_input_repositories: List[str],
                                      test_input_cpu_count: int, test_input_max_chunksize: int) -> None:
        """Test that functools.partial function is called once correctly."""

        # Execute the get_items_for_all_repos function
        _ = get_items_for_all_repos(patch_get_items_for_all_repos_github,
                                    test_input_method_name,
                                    self.create_list_of_classes_with_full_name(test_input_repositories),
                                    test_input_cpu_count,
                                    test_input_max_chunksize)

        # Assert that functools.partial is called once with the correct arguments
        patch_get_items_for_all_repos_partial.assert_called_once_with(patch_get_items_for_repo,
                                                                      patch_get_items_for_all_repos_github,
                                                                      test_input_method_name)

    def test_parallelise_dictionary_processing_called_once_correctly(
            self, patch_get_items_for_all_repos_github: MagicMock, patch_get_items_for_repo: MagicMock,
            patch_get_items_for_all_repos_partial: MagicMock,
            patch_get_items_for_all_repo_parallelise_dictionary_processing: MagicMock,
            test_input_method_name: str, test_input_repositories: List[str], test_input_cpu_count: int,
            test_input_max_chunksize: int
    ) -> None:
        """Test the parallelise_dictionary_processing function is called once correctly."""

        # Execute the get_items_for_all_repos function
        _ = get_items_for_all_repos(patch_get_items_for_all_repos_github,
                                    test_input_method_name,
                                    self.create_list_of_classes_with_full_name(test_input_repositories),
                                    test_input_cpu_count,
                                    test_input_max_chunksize)

        # Assert that the parallelise_dictionary_processing function is called once correctly
        patch_get_items_for_all_repo_parallelise_dictionary_processing.assert_called_once_with(
            patch_get_items_for_all_repos_partial.return_value, test_input_repositories, test_input_cpu_count,
            test_input_max_chunksize
        )

    def test_returns_correctly(self, patch_get_items_for_all_repos_github: MagicMock,
                               patch_get_items_for_repo: MagicMock, patch_get_items_for_all_repos_partial: MagicMock,
                               patch_get_items_for_all_repo_parallelise_dictionary_processing: MagicMock,
                               test_input_method_name: str, test_input_repositories: List[str],
                               test_input_cpu_count: int, test_input_max_chunksize: int) -> None:
        """Test the output of the function is as expected."""

        # Execute the get_items_for_all_repos function
        test_output = get_items_for_all_repos(patch_get_items_for_all_repos_github,
                                              test_input_method_name,
                                              self.create_list_of_classes_with_full_name(test_input_repositories),
                                              test_input_cpu_count,
                                              test_input_max_chunksize)

        # Assert the output is as expected
        assert test_output == patch_get_items_for_all_repo_parallelise_dictionary_processing.return_value
