from py.path import local
from src.utils.logger import create_logger
from typing import Dict, Union
from unittest.mock import MagicMock
import logging
import json
import os
import pytest


@pytest.fixture
def temporary_log_directory(tmpdir_factory) -> local:
    """Create a temporary log directory"""
    return tmpdir_factory.mktemp("logs")


@pytest.fixture
def patch_logging_getlogger(mocker) -> MagicMock:
    """Patch the `logging.getLogger` function."""
    return mocker.patch("logging.getLogger")


@pytest.fixture
def patch_logging_formatter(mocker) -> MagicMock:
    """Patch the `logging.Formatter` function."""
    return mocker.patch("logging.Formatter")


@pytest.fixture
def patch_logging_filehandler(mocker, patch_logging_getlogger: MagicMock) -> MagicMock:
    """Patch the `logging.FileHandler` function."""
    return mocker.patch("logging.FileHandler")


@pytest.fixture
def patch_logging_streamhandler(mocker, patch_logging_filehandler: MagicMock) -> MagicMock:
    """Patch the `logging.StreamHandler` function."""
    return mocker.patch("logging.StreamHandler")


@pytest.fixture
def patch_src_utils_logger_create_logger(mocker) -> MagicMock:
    """Patch the `src.utils.logger.create_logger` function."""
    return mocker.patch("src.utils.logger.create_logger")


@pytest.fixture
def patch_src_utils_logger_time(mocker) -> MagicMock:
    """Patch the `time.time` function imported in src/utils/logger.py."""
    return mocker.patch("src.utils.logger.time")


@pytest.fixture
def example_log_file(temporary_log_directory) -> Dict[str, Union[logging.Logger, logging.RootLogger, str]]:
    """Create a temporary log file for testing purposes."""

    # Create a temporary directory to store the log file, and define a file path to a log file
    temporary_log_file = temporary_log_directory.join("temporary.log")
    temporary_log_filepath = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)

    # Create a log file
    temporary_log = create_logger("temporary_log", temporary_log_filepath)

    # Return a dictionary containing the log, and its filepath
    return {"logger": temporary_log, "path": temporary_log_filepath}


@pytest.fixture
def temporary_json_directory(tmpdir_factory) -> local:
    """Create a temporary directory for a JSON file"""
    return tmpdir_factory.mktemp("json")


@pytest.fixture
def example_json_file(temporary_json_directory, test_input_username: str, test_input_token: str,
                      test_input_key_username: str, test_input_key_token: str) -> Dict[str, str]:
    """Create a temporary JSON file for testing purposes."""

    # Create a temporary directory to store the JSON file, and define a file path to a JSON file
    temporary_json_file = temporary_json_directory.join("example_credentials.json")
    temporary_json_filepath = os.path.join(temporary_json_file.dirname, temporary_json_file.basename)

    # Create the JSON data, and write it to the file
    temporary_json = json.dumps({test_input_key_username: test_input_username, test_input_key_token: test_input_token},
                                ensure_ascii=False, indent=4)
    with open(temporary_json_filepath, "w") as f:
        f.write(temporary_json)

    # Return a dictionary containing the JSON, and its filepath
    return {"json": temporary_json, "path": temporary_json_filepath}


@pytest.fixture
def patch_find_organisation_repos_github(mocker) -> MagicMock:
    """Patch the `github.Github` class imported into find_organisation_repos.py."""
    return mocker.patch("src.make_data.find_organisation_repos.Github")


@pytest.fixture
def patch_get_items_for_repo_github(mocker) -> MagicMock:
    """Patch the `github.Github` class imported into get_items_for_repo.py."""
    return mocker.patch("src.make_data.get_items_for_repo.Github")


@pytest.fixture
def patch_get_items_for_all_repos_github(mocker) -> MagicMock:
    """Patch the `github.Github` class imported into get_items_for_all_repo.py."""
    return mocker.patch("src.make_data.get_items_for_all_repos.Github")


@pytest.fixture
def patch_get_items_for_repo(mocker) -> MagicMock:
    """Patch the `get_items_for_repo` function imported into get_items_for_all_repo.py."""
    return mocker.patch("src.make_data.get_items_for_all_repos.get_items_for_repo")


@pytest.fixture
def patch_get_items_for_all_repos_partial(mocker) -> MagicMock:
    """Patch the `functools.partial` function imported into get_items_for_all_repo.py."""
    return mocker.patch("src.make_data.get_items_for_all_repos.partial")


@pytest.fixture
def patch_get_items_for_all_repo_parallelise_dictionary_processing(mocker) -> MagicMock:
    """Patch the `parallelise_dictionary_processing` function imported into get_items_for_all_repo.py."""
    return mocker.patch("src.make_data.get_items_for_all_repos.parallelise_dictionary_processing")


@pytest.fixture
def patch_multiprocessing_pool(mocker) -> MagicMock:
    """Patch the `multiprocessing.Pool` function."""
    return mocker.patch("multiprocessing.Pool")


@pytest.fixture
def patch_multiprocessing_pool_enter_imap_unordered(patch_multiprocessing_pool: MagicMock) -> MagicMock:
    """Patch the `imap_unordered` function within an open `multiprocessing.Pool` context manager."""
    return patch_multiprocessing_pool.return_value.__enter__.return_value.imap_unordered


@pytest.fixture
def patch_extract_attribute_from_paginated_list_elements(mocker) -> MagicMock:
    """Patch the `extract_attribute_from_paginated_list_elements` function."""
    return mocker.patch("src.make_data.extract_attribute_from_dict_of_paginated_lists."
                        "extract_attribute_from_paginated_list_elements")


@pytest.fixture
def patch_extract_attribute_from_dict_of_paginated_lists_partial(mocker) -> MagicMock:
    """Patch the `functools.partial` function imported into extract_attribute_from_dict_of_paginated_lists.py."""
    return mocker.patch("src.make_data.extract_attribute_from_dict_of_paginated_lists.partial")


@pytest.fixture
def patch_extract_attribute_from_dict_of_paginated_lists_parallelise_dictionary_processing(mocker) -> MagicMock:
    """Patch `parallelise_dictionary_processing` function from extract_attribute_from_dict_of_paginated_lists.py."""
    return mocker.patch("src.make_data.extract_attribute_from_dict_of_paginated_lists."
                        "parallelise_dictionary_processing")


@pytest.fixture
def patch_add_team_with_permissions_extract_attribute_from_paginated_list_elements(mocker) -> MagicMock:
    """Patch the extract_attribute_from_paginated_list_elements function."""
    return mocker.patch("src.make_data.add_team_with_permissions_to_all_repositories."
                        "extract_attribute_from_paginated_list_elements")


@pytest.fixture
def patch_check_team_added_already(mocker) -> MagicMock:
    """Patch the `check_team_added_already` function."""
    return mocker.patch("src.make_data.add_team_with_permissions_to_all_repositories.check_team_added_already")


@pytest.fixture
def patch_add_team_with_permissions_to_repository(mocker) -> MagicMock:
    """Patch the `check_team_added_already` function."""
    return mocker.patch("src.make_data.add_team_with_permissions_to_all_repositories."
                        "add_team_with_permissions_to_repository")
