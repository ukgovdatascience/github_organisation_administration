from time import time
from typing import Any, Callable, Optional, Union
import functools
import logging
import os


def create_logger(name: str = None, filename: Optional[str] = None) -> Union[logging.Logger, logging.RootLogger]:
    """Create a logger.

    Args:
        name: Default: None. Name of the logger. If None, this is the root logger
        filename: Default: None. File path to write out to. If None, no file is created.

    Returns:
        A logger for logging progress of the code, and a log file, if filename is not None.

    """

    # Create a logger, and set its level
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Set the format of the log messages
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")

    # Create a logging console handler, and set its level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Set the format of `ch`, and add it to `log`
    ch.setFormatter(log_format)
    log.addHandler(ch)

    # Check if `filename` is not None
    if filename is not None:

        # Create a file handler, and set its level
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.INFO)

        # Set the format of `fh`, and add it to `log`
        fh.setFormatter(log_format)
        log.addHandler(fh)

    # Return `log`
    return log


class Log(object):

    # Message formats
    MSG_ENTRY = "`{}`: Executing function"
    MSG_EXIT = "`{}`: Executed in {:,.2f} s"
    MSG_EXCEPTION = "`{}`: Raised an exception!"

    def __init__(self, logger_obj: Union[logging.Logger, logging.RootLogger] = None, level: str = "info") -> None:
        """A logging decorator to log entry, and exit into any given function, and also log exceptions.

        Args:
            logger_obj: Default: None. A logging.Logger or logging.RootLogger object. If None, a root logger is setup
              later.
            level: Default: 'info'. The level of function entry/and exit messages. Must be a one of the levels listed
              in the documentation here: https://docs.python.org/3/library/logging.html#logging-levels

        """

        # Instantiate attributes
        self.logger = logger_obj
        self.level = level.lower()

    def __call__(self, func: Callable) -> Any:
        """Logging decorator wrapper around a function to log entry/exit messages, and exceptions.

        Args:
            func: A callable function.

        Returns:
            If no exceptions, the outputs from the function will be returned. Otherwise the exception will be raised.

        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # Try to execute the function
            try:

                # Log an entry message into the function
                getattr(self.logger, self.level)(self.MSG_ENTRY.format(func.__name__))

                # Start a timer
                time_start = time()

                # Execute the function
                output = func(*args, **kwargs)

                # Log an exit message out of the function
                getattr(self.logger, self.level)(self.MSG_EXIT.format(func.__name__, time() - time_start))

                # Return the output from the function
                return output

            except Exception as e:

                # Log an exception message, and re-raise the error
                self.logger.exception(self.MSG_EXCEPTION.format(func.__name__))
                raise e

        # Return the wrapper
        return wrapper


# Create the logger
logger = create_logger("src", os.path.join(os.getenv("DIR_DATA_LOGS"), "github_organisation_administration.log"))
