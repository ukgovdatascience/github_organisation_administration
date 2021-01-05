from py.path import local
from src.utils.logger import Log, create_logger
from typing import Dict, Union
from unittest.mock import MagicMock
import logging
import os
import pytest
import re

# Define the expected logging format for the `create_logger` function
EXPECTED_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"

# Define the expected base regular expression pattern for the log messages
EXPECTED_LOG_MESSAGE_BASE = r"\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}},\d{{3}} - {name} - {level}: `{function}`:"


@pytest.mark.parametrize("test_input_filename", [None, "hello.log", "world.log", "foo.log", "bar.log"])
@pytest.mark.parametrize("test_input_name", [None, "hello", "world", "foo", "bar"])
class TestCreateLogger:
    """Test the `create_logger` function."""

    def test_log_name(self, temporary_log_directory: local, patch_logging_getlogger: MagicMock, test_input_name: str,
                      test_input_filename: str) -> None:
        """Test the function is assigned the correct name."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # Assert the correct name is used
        patch_logging_getlogger.assert_called_with(test_input_name)

    def test_log_level(self, temporary_log_directory: local, patch_logging_getlogger: MagicMock, test_input_name: str,
                       test_input_filename: str) -> None:
        """Test the correct logging level is set."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # Assert the correct logging level is set for the log
        patch_logging_getlogger.return_value.setLevel.assert_called_once_with(logging.DEBUG)

    def test_log_format(self, temporary_log_directory: local, patch_logging_formatter: MagicMock, test_input_name: str,
                        test_input_filename: str) -> None:
        """Test the format of the log."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # Assert the correct logging format is applied for the log
        patch_logging_formatter.assert_called_once_with(EXPECTED_LOG_FORMAT)

    def test_streamhandler_level(self, temporary_log_directory: local, patch_logging_streamhandler: MagicMock,
                                 test_input_name: str, test_input_filename: str) -> None:
        """Test the correct logging level for the stream handler is used."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # Assert the correct logging level for the stream handler is used
        patch_logging_streamhandler.return_value.setLevel.assert_called_once_with(logging.INFO)

    def test_streamhandler_format(self, temporary_log_directory: local, patch_logging_formatter: MagicMock,
                                  patch_logging_streamhandler: MagicMock, test_input_name: str,
                                  test_input_filename: str) -> None:
        """Test the correct log format is used for the stream handler."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # Assert the correct log format is set for the stream handler
        patch_logging_streamhandler.return_value.setFormatter.assert_called_once_with(
            patch_logging_formatter.return_value
        )

    def test_filehandler_filename(self, temporary_log_directory: local, patch_logging_filehandler: MagicMock,
                                  test_input_name: str, test_input_filename: str) -> None:
        """Test the file handler is set with the correct filename."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # If a filename is given, check that the file handler is set with it. Otherwise check the file handler is not
        # called
        if test_input_filename:
            patch_logging_filehandler.assert_called_with(temporary_log_file_path)
        else:
            assert not patch_logging_filehandler.called

    def test_filehandler_level(self, temporary_log_directory: local, patch_logging_filehandler: MagicMock,
                               test_input_name: str, test_input_filename: str) -> None:
        """Test the file handler is set with the correct logging level."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # If a filename is given, check that the file handler is set with the correct logging level. Otherwise check
        # the file handler is not called
        if test_input_filename:
            patch_logging_filehandler.return_value.setLevel.assert_called_once_with(logging.INFO)
        else:
            assert not patch_logging_filehandler.called

    def test_filehandler_format(self, temporary_log_directory: local, patch_logging_formatter: MagicMock,
                                patch_logging_filehandler: MagicMock, test_input_name: str,
                                test_input_filename: str) -> None:
        """Test the file handler is set with the correct logging format."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # If a filename is given, check the file handler is set with the correct logging format. Otherwise check that
        # the file handler is not called
        if test_input_filename:
            patch_logging_filehandler.return_value.setFormatter.assert_called_once_with(
                patch_logging_formatter.return_value
            )
        else:
            assert not patch_logging_filehandler.called

    def test_add_handlers_to_log(self, mocker, temporary_log_directory: local, patch_logging_getlogger: MagicMock,
                                 patch_logging_streamhandler: MagicMock, patch_logging_filehandler: MagicMock,
                                 test_input_name: str, test_input_filename: str) -> None:
        """Test the stream handler is added to the log, as well as the file handler, if a filename is given."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        _ = create_logger(test_input_name, temporary_log_file_path)

        # If a filename is given, check that the last two handlers added to the log are stream and file handler.
        # Otherwise, check that only the stream handler is added
        if test_input_filename:

            # Define the last two expected calls as the stream and file handlers (in order)
            test_expected = [mocker.call(patch_logging_streamhandler.return_value),
                             mocker.call(patch_logging_filehandler.return_value)]

            # Assert that the last two calls to `addHandler` are correct
            assert patch_logging_getlogger.return_value.addHandler.call_args_list[-2:] == test_expected

        else:
            patch_logging_getlogger.return_value.addHandler.assert_called_with(patch_logging_streamhandler.return_value)

    def test_log_output(self, temporary_log_directory: local, patch_logging_getlogger: MagicMock, test_input_name: str,
                        test_input_filename: str) -> None:
        """Test the function outputs the expected log."""

        # Create a temporary log file, and get its path, if `test_input_filename` is not None
        if test_input_filename:
            temporary_log_file = temporary_log_directory.join(test_input_filename)
            temporary_log_file_path = os.path.join(temporary_log_file.dirname, temporary_log_file.basename)
        else:
            temporary_log_file_path = None

        # Run the `create_logger` function
        test_output = create_logger(test_input_name, temporary_log_file_path)

        # Assert the output is as expected
        assert test_output == patch_logging_getlogger.return_value


# Define test cases for test_input_level argument in the `TestLog` test class
args_test_log_test_input_level = list(sum(
    [(L, L.lower()) for L in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]],
    ()
))


@pytest.mark.parametrize("test_input_level", args_test_log_test_input_level)
class TestLog:

    def test_logger(self, patch_src_utils_logger_create_logger: MagicMock, test_input_level: str) -> None:
        """Test the `self.logger` instance attribute."""
        test_output = Log(patch_src_utils_logger_create_logger, test_input_level).logger
        assert test_output == patch_src_utils_logger_create_logger

    def test_level(self, patch_src_utils_logger_create_logger: MagicMock, test_input_level: str) -> None:
        """Test the `self.level` instance attribute."""
        assert Log(patch_src_utils_logger_create_logger, test_input_level).level == test_input_level.lower()

    @pytest.mark.parametrize("test_input_function_duration", range(1, 5))
    def test_log_messages_correct_for_no_exceptions(
            self, patch_src_utils_logger_time: MagicMock,
            example_log_file: Dict[str, Union[logging.Logger, logging.RootLogger, str]], test_input_level: str,
            test_input_function_duration: int
    ) -> None:
        """Test the decorator creates the correct log messages, if the function it wraps raises no exceptions."""

        # Set the `side_effect` of `patch_src_utils_logger_time`
        patch_src_utils_logger_time.side_effect = [0, test_input_function_duration]

        @Log(example_log_file["logger"], test_input_level)
        def example_function():
            """Example function that raises no errors."""
            pass

        # Define the base regular expression pattern of the log message. This will be a datetime stamp, followed by the
        # logger name, logging level, and wrapped function name
        log_base_pattern = EXPECTED_LOG_MESSAGE_BASE.format(name=example_log_file["logger"].name,
                                                            level=test_input_level.upper(),
                                                            function=example_function.__name__)

        # Define the complete log message expected
        test_expected_regex_pattern = fr"{log_base_pattern} Executing function\n{log_base_pattern} Executed in " \
                                      fr"{test_input_function_duration:0.2f} s"

        # Execute the `example_function`
        _ = example_function()

        # Open the log file, and assert the message is as expected. If level is DEBUG, assert the log is empty
        with open(example_log_file["path"], "r") as f:
            if test_input_level.upper() == "DEBUG":
                assert f.read() == ""
            else:
                assert re.match(test_expected_regex_pattern, f.read())

    @pytest.mark.parametrize("test_input_function_duration", range(1, 5))
    def test_log_messages_correct_for_exceptions(
            self, patch_src_utils_logger_time: MagicMock,
            example_log_file: Dict[str, Union[logging.Logger, logging.RootLogger, str]], test_input_level: str,
            test_input_function_duration: int
    ) -> None:
        """Test the decorator creates the correct log messages, if the function it wraps raises exceptions."""

        # Set the `side_effect` of `patch_src_utils_logger_time`
        patch_src_utils_logger_time.side_effect = [0, test_input_function_duration]

        @Log(example_log_file["logger"], test_input_level)
        def example_function():
            """Example function that raises a ValueError."""
            raise ValueError("Testing for errors")

        # Define the base regular expression pattern of the entry and error log messages
        entry_log_base_pattern = EXPECTED_LOG_MESSAGE_BASE.format(name=example_log_file["logger"].name,
                                                                  level=test_input_level.upper(),
                                                                  function=example_function.__name__)
        error_log_base_pattern = EXPECTED_LOG_MESSAGE_BASE.format(name=example_log_file["logger"].name, level="ERROR",
                                                                  function=example_function.__name__)

        # Define the expected entry and error log regular expression patterns
        test_expected_entry_log_regex_pattern = entry_log_base_pattern + r" Executing function\n"
        test_expected_error_log_regex_pattern = error_log_base_pattern + r" Raised an exception!"

        # Execute the `example_function`, which should raise a `ValueError`
        with pytest.raises(ValueError):
            _ = example_function()

        # Open the log file, and assert the message is as expected. If level is DEBUG, assert the log is empty
        with open(example_log_file["path"], "r") as f:
            if test_input_level.upper() == "DEBUG":
                assert re.match(test_expected_error_log_regex_pattern, f.read())
            else:
                assert re.match(test_expected_entry_log_regex_pattern + test_expected_error_log_regex_pattern, f.read())
