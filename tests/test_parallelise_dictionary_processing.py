from itertools import cycle, islice
from src.utils.parallelise_dictionary_processing import parallelise_dictionary_processing
from typing import Callable, Dict
from unittest.mock import MagicMock
import pytest

# Define test cases for the TestParalleliseDictionaryProcessing test class
args_test_parallelise_dictionary_processing_callable_function = [lambda x: {x: x ** 2}]
args_test_parallelise_dictionary_processing_iterable = [[1, 2, 3]]
args_test_parallelise_dictionary_processing_cpu_count = [1, 3, 5, 7]
args_test_parallelise_dictionary_processing_max_chunksize = [1, 4, 8]
args_test_parallelise_dictionary_processing_duplicates = [1, 2, 3, 4]


@pytest.mark.parametrize("test_input_callable_function", args_test_parallelise_dictionary_processing_callable_function)
@pytest.mark.parametrize("test_input_iterable", args_test_parallelise_dictionary_processing_iterable)
@pytest.mark.parametrize("test_input_cpu_count", args_test_parallelise_dictionary_processing_cpu_count)
@pytest.mark.parametrize("test_input_max_chunksize", args_test_parallelise_dictionary_processing_max_chunksize)
class TestParalleliseDictionaryProcessing:

    def test_pool_called_once_correctly(self, patch_multiprocessing_pool: MagicMock,
                                        test_input_callable_function: Callable[..., Dict], test_input_iterable: iter,
                                        test_input_cpu_count: int, test_input_max_chunksize: int) -> None:
        """Test multiprocessing.Pool is called once correctly."""

        # Execute the parallelise_dictionary_processing function
        _ = parallelise_dictionary_processing(test_input_callable_function, test_input_iterable, test_input_cpu_count,
                                              test_input_max_chunksize)

        # Assert multiprocessing.Pool is called once with the correct arguments
        patch_multiprocessing_pool.assert_called_once_with(test_input_cpu_count)

    def test_imap_unordered_called_correctly(self, patch_multiprocessing_pool_enter_imap_unordered: MagicMock,
                                             test_input_callable_function: Callable[..., Dict],
                                             test_input_iterable: iter, test_input_cpu_count: int,
                                             test_input_max_chunksize: int) -> None:
        """Test multiprocessing.Pool.imap_unordered is called correctly."""

        # Calculate the expected chunk size for each process
        test_expected_chunksize = len(test_input_iterable) / test_input_cpu_count
        test_expected_chunksize = min(int(test_expected_chunksize) + bool(test_expected_chunksize),
                                      test_input_max_chunksize)

        # Execute the parallelise_dictionary_processing function
        _ = parallelise_dictionary_processing(test_input_callable_function, test_input_iterable, test_input_cpu_count,
                                              test_input_max_chunksize)

        # Assert multiprocessing.Pool.imap_unordered is called with the correct arguments
        patch_multiprocessing_pool_enter_imap_unordered.assert_called_once_with(
            test_input_callable_function, test_input_iterable, chunksize=test_expected_chunksize
        )

    @pytest.mark.parametrize("test_input_duplicates", args_test_parallelise_dictionary_processing_duplicates)
    def test_assertion_error_raised_for_duplicate_keys(self,
                                                       patch_multiprocessing_pool_enter_imap_unordered: MagicMock,
                                                       test_input_callable_function: Callable[..., Dict],
                                                       test_input_iterable: iter, test_input_cpu_count: int,
                                                       test_input_max_chunksize: int,
                                                       test_input_duplicates: int) -> None:
        """Test an AssertionError is raised if duplicate keys (repository names) are returned."""

        # Generate duplicate iterables
        test_input_duplicate_iterable = list(islice(cycle(test_input_iterable),
                                                    len(test_input_iterable) + test_input_duplicates))

        # Set the return_value of patch_multiprocessing_pool_enter_imap_unordered
        patch_multiprocessing_pool_enter_imap_unordered.return_value = (
            test_input_callable_function(i) for i in test_input_duplicate_iterable
        )

        # Execute the parallelise_dictionary_processing function, checking that it raises an AssertionError
        with pytest.raises(AssertionError):
            _ = parallelise_dictionary_processing(test_input_callable_function, test_input_duplicate_iterable,
                                                  test_input_cpu_count, test_input_max_chunksize)

    def test_returns_correctly(self, patch_multiprocessing_pool_enter_imap_unordered: MagicMock,
                               test_input_callable_function: Callable[..., Dict], test_input_iterable: iter,
                               test_input_cpu_count: int, test_input_max_chunksize: int) -> None:
        """Test the output of the function is as expected."""

        # Set the return value of patch_multiprocessing_pool_enter_imap_unordered
        patch_multiprocessing_pool_enter_imap_unordered.return_value = (
            {r: ["octocat"]} for r in test_input_iterable
        )

        # Execute the parallelise_dictionary_processing function
        test_output = parallelise_dictionary_processing(test_input_callable_function, test_input_iterable,
                                                        test_input_cpu_count, test_input_max_chunksize)

        # Assert the output is as expected
        assert test_output == {r: ["octocat"] for r in test_input_iterable}
