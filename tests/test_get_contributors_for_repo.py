from src.make_data.get_contributors_for_repo import get_contributors_for_repo
from unittest.mock import MagicMock
import pytest

# Define test cases for the TestGetContributorsForRepos test class
args_test_get_contributors_for_repos_repository_name = ["hello", "world"]


@pytest.mark.parametrize("test_input_repository_name", args_test_get_contributors_for_repos_repository_name)
class TestGetContributorsForRepos:

    def test_get_repo_called_correctly(self, patch_get_contributors_for_repo_github: MagicMock,
                                       test_input_repository_name: str) -> None:
        """Test that the github.Github.get_repo method is called once correctly."""

        # Execute the get_contributors_for_repo function
        _ = get_contributors_for_repo(patch_get_contributors_for_repo_github, test_input_repository_name)

        # Assert that the github.Github.get_repo method is called once with the correct arguments
        patch_get_contributors_for_repo_github.get_repo.assert_called_once_with(test_input_repository_name)

    def test_returns_correctly(self, patch_get_contributors_for_repo_github: MagicMock,
                               test_input_repository_name: str) -> None:
        """Test the output of the function is as expected."""

        # Define the expected value of the output dictionary
        test_expected_value = patch_get_contributors_for_repo_github.get_repo.return_value.get_contributors()

        # Execute the get_contributors_for_repo function
        test_output = get_contributors_for_repo(patch_get_contributors_for_repo_github, test_input_repository_name)

        # Assert the return is as expected
        assert test_output == {test_input_repository_name: test_expected_value}
