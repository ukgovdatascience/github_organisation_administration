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
    """Patch the logging.getLogger function."""
    return mocker.patch("logging.getLogger")


@pytest.fixture
def patch_logging_formatter(mocker) -> MagicMock:
    """Patch the logging.Formatter function."""
    return mocker.patch("logging.Formatter")


@pytest.fixture
def patch_logging_filehandler(mocker, patch_logging_getlogger: MagicMock) -> MagicMock:
    """Patch the logging.FileHandler function."""
    return mocker.patch("logging.FileHandler")


@pytest.fixture
def patch_logging_streamhandler(mocker, patch_logging_filehandler: MagicMock) -> MagicMock:
    """Patch the logging.StreamHandler function."""
    return mocker.patch("logging.StreamHandler")


@pytest.fixture
def patch_src_utils_logger_create_logger(mocker) -> MagicMock:
    """Patch the src.utils.logger.create_logger function."""
    return mocker.patch("src.utils.logger.create_logger")


@pytest.fixture
def patch_src_utils_logger_time(mocker) -> MagicMock:
    """Patch the time.time function imported in src/utils/logger.py."""
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
