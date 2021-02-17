from src.make_data.find_organisation_repos import find_organisation_repos
from unittest.mock import MagicMock
import pytest

# Test cases for the `TestFindOrganisationRepos` test class
args_test_find_organisation_repos_organisation = ["hello", "world"]
args_test_find_organisation_repos_repository_type = ["all", "public", "private", "forks", "sources", "member"]
args_test_find_organisation_repos_sort = ["created", "updated", "pushed", "full_name"]
args_test_find_organisation_repos_direction = ["asc", "desc"]


@pytest.mark.parametrize("test_input_organisation", args_test_find_organisation_repos_organisation)
@pytest.mark.parametrize("test_input_repository_type", args_test_find_organisation_repos_repository_type)
@pytest.mark.parametrize("test_input_sort", args_test_find_organisation_repos_sort)
@pytest.mark.parametrize("test_input_direction", args_test_find_organisation_repos_direction)
class TestFindOrganisationRepos:

    def test_get_organization_called_correctly(self, patch_find_organisation_repos_github: MagicMock,
                                               test_input_organisation: str, test_input_repository_type: str,
                                               test_input_sort: str, test_input_direction: str) -> None:
        """Test that the `github.Github.get_organization` method is called once correctly."""

        # Execute the `find_organisation_repos` function
        _ = find_organisation_repos(patch_find_organisation_repos_github, test_input_organisation,
                                    test_input_repository_type, test_input_sort, test_input_direction)

        # Assert the `github.Github.get_organization` method is called once correctly
        patch_find_organisation_repos_github.get_organization.assert_called_once_with(test_input_organisation)

    def test_get_repos_called_correctly(self, patch_find_organisation_repos_github: MagicMock,
                                        test_input_organisation: str, test_input_repository_type: str,
                                        test_input_sort: str, test_input_direction: str) -> None:
        """Test the `github.Organization.Organization.get_repos` method is called once correctly."""

        # Execute the `find_organisation_repos` function
        _ = find_organisation_repos(patch_find_organisation_repos_github, test_input_organisation,
                                    test_input_repository_type, test_input_sort, test_input_direction)

        # Assert the `github.Organization.Organization.get_repos` method is called once correctly
        patch_find_organisation_repos_github.get_organization.return_value.get_repos.assert_called_once_with(
            test_input_repository_type, test_input_sort, test_input_direction
        )

    def test_returns_correctly(self, patch_find_organisation_repos_github: MagicMock, test_input_organisation: str,
                               test_input_repository_type: str, test_input_sort: str,
                               test_input_direction: str) -> None:
        """Test the output of the function is as expected."""

        # Execute the `find_organisation_repos` function
        test_output = find_organisation_repos(patch_find_organisation_repos_github, test_input_organisation,
                                              test_input_repository_type, test_input_sort, test_input_direction)

        # Assert `test_output` is as expected
        assert test_output == patch_find_organisation_repos_github.get_organization.return_value.get_repos.return_value
