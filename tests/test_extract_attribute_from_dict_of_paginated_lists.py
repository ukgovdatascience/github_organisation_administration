from github import UnknownObjectException
from src.make_data.extract_attribute_from_dict_of_paginated_lists import (
    extract_attribute_from_paginated_list_elements,
    _extract_attributes_from_key_paginated_list_pair,
    extract_attribute_from_dict_of_paginated_lists
)
from typing import Any, Dict, List
from unittest.mock import MagicMock
import pytest

# Define test cases for the `TestExtractAttributeFromPaginatedListElements` test class
args_test_extract_attribute_from_paginated_list_elements_attribute_name = [
    "hello",
    "world"
]
args_test_extract_attribute_from_paginated_list_elements_list = [
    [1, 2, 3, 4],
    [2, 4, 6, 8]
]
args_test_extract_attribute_from_paginated_list_elements_exception = [
    ValueError,
    AttributeError
]


@pytest.mark.parametrize("test_input_attribute_name",
                         args_test_extract_attribute_from_paginated_list_elements_attribute_name)
class TestExtractAttributeFromPaginatedListElements:

    @staticmethod
    def create_list_of_classes_with_attribute_name(input_list: List[Any], attribute_name: str) -> List[MagicMock]:
        """Create a list of MagicMocks with a set attribute based on an input list."""

        class ExampleClass:

            def __init__(self, entry: str) -> None:
                """Example class that only has one attribute, `attribute_name`.

                Args:
                    entry: An example entry

                """
                setattr(self, attribute_name, entry)

        # Return a list of `ExampleClasses` based on each element of input_list
        return [ExampleClass(e)for e in input_list]

    @pytest.mark.parametrize("test_input_list", args_test_extract_attribute_from_paginated_list_elements_list)
    def test_returns_correctly_when_no_errors(self, test_input_list: List, test_input_attribute_name: str) -> None:
        """Test that, when no errors are raised, the output is as expected"""

        # Execute the `extract_attribute_from_paginated_list_elements` function
        test_output = extract_attribute_from_paginated_list_elements(
            self.create_list_of_classes_with_attribute_name(test_input_list, test_input_attribute_name),
            test_input_attribute_name
        )

        # Assert the output is as expected
        assert test_output == test_input_list

    @staticmethod
    def create_iterable_raises_exception(exception: Exception) -> object:
        """Create a class that raises an exception when iterated over."""

        class ExampleClass:

            def __init__(self, exception: Exception) -> None:
                """Example class that raises an exception when iterated over."""
                self.exception = exception

            def __iter__(self):
                raise self.exception

        # Return `ExampleClasses` with its exception
        return ExampleClass(exception)

    def test_unknownobjectexception_returns_correctly(self, test_input_attribute_name: str) -> None:
        """Test that the correct output is returned if an `UnknownObjectException` exception is raised."""

        # Execute the `extract_attribute_from_paginated_list_elements` function
        test_output = extract_attribute_from_paginated_list_elements(
            self.create_iterable_raises_exception(UnknownObjectException("Error", 404)), test_input_attribute_name
        )

        # Assert the output is as expected
        assert test_output is None

    @pytest.mark.parametrize("test_input_exception", args_test_extract_attribute_from_paginated_list_elements_exception)
    def test_all_other_exceptions_raised(self, test_input_attribute_name: str, test_input_exception: Exception) -> None:
        """Test that all other exceptions are raised correctly."""

        with pytest.raises(test_input_exception):
            _ = extract_attribute_from_paginated_list_elements(
                self.create_iterable_raises_exception(test_input_exception), test_input_attribute_name
            )


# Define test cases for the `TestExtractAttributesFromKeyPaginatedListPair` test class
args_test_extract_attributes_from_key_paginated_list_pair = [
    ({"hello": "world", "foo": "bar"}, "hello_world", "hello"),
    ({"hello": "world", "foo": "bar"}, "hello_world", "foo")
]


@pytest.mark.parametrize("test_input_pl, test_input_attribute_name, test_input_dictionary_key",
                         args_test_extract_attributes_from_key_paginated_list_pair)
class TestExtractAttributesFromKeyPaginatedListPair:

    def test_calls_extract_attribute_from_paginated_list_elements_once_correctly(
            self, patch_extract_attribute_from_paginated_list_elements: MagicMock, test_input_pl: Dict[str, Any],
            test_input_attribute_name: str, test_input_dictionary_key: str
    ) -> None:
        """Test the `extract_attribute_from_paginated_list_elements` function is called once correctly."""

        # Execute the `_extract_attributes_from_key_paginated_list_pair` function
        _ = _extract_attributes_from_key_paginated_list_pair(test_input_pl, test_input_attribute_name,
                                                             test_input_dictionary_key)

        # Assert the `extract_attribute_from_paginated_list_elements` function is called once correctly
        patch_extract_attribute_from_paginated_list_elements.assert_called_once_with(
            test_input_pl[test_input_dictionary_key], test_input_attribute_name
        )

    def test_returns_correctly(self, patch_extract_attribute_from_paginated_list_elements: MagicMock,
                               test_input_pl: Dict[str, Any], test_input_attribute_name: str,
                               test_input_dictionary_key: str) -> None:
        """Test the function returns correctly."""

        # Execute the `_extract_attributes_from_key_paginated_list_pair` function
        test_output = _extract_attributes_from_key_paginated_list_pair(test_input_pl, test_input_attribute_name,
                                                                       test_input_dictionary_key)

        # Define the expected output
        test_expected = {test_input_dictionary_key: patch_extract_attribute_from_paginated_list_elements.return_value}

        # Assert the returned value is as expected
        assert test_output == test_expected


# Define test cases for the `TestExtractAttributeFromDictOfPaginatedLists` test class
args_test_extract_attribute_from_dict_of_paginated_lists = [
    ({"hello": "world", "foo": "bar"}, "hello_world", 2, 50),
    ({"hello": "world", "foo": "bar"}, "hello_world", 6, 100)
]


@pytest.mark.parametrize("test_input_pl, test_input_attribute_name, test_input_cpu_count, test_input_max_chunksize",
                         args_test_extract_attribute_from_dict_of_paginated_lists)
class TestExtractAttributeFromDictOfPaginatedLists:

    def test_calls_partial_once_correctly(
            self, patch_extract_attribute_from_dict_of_paginated_lists_partial: MagicMock,
            patch_extract_attribute_from_dict_of_paginated_lists_parallelise_dictionary_processing: MagicMock,
            test_input_pl: Dict[str, Any], test_input_attribute_name: str, test_input_cpu_count: int,
            test_input_max_chunksize: int
    ) -> None:
        """Test the function calls `functools.partial` once with the correct arguments."""

        # Execute the `extract_attribute_from_dict_of_paginated_lists` function
        _ = extract_attribute_from_dict_of_paginated_lists(test_input_pl, test_input_attribute_name,
                                                           test_input_cpu_count, test_input_max_chunksize)

        # Assert the `functools.partial` is called once correctly
        patch_extract_attribute_from_dict_of_paginated_lists_partial.assert_called_once_with(
            _extract_attributes_from_key_paginated_list_pair, test_input_pl, test_input_attribute_name
        )

    def test_parallelise_dictionary_processing_called_once_correctly(
            self, patch_extract_attribute_from_dict_of_paginated_lists_partial: MagicMock,
            patch_extract_attribute_from_dict_of_paginated_lists_parallelise_dictionary_processing: MagicMock,
            test_input_pl: Dict[str, Any], test_input_attribute_name: str, test_input_cpu_count: int,
            test_input_max_chunksize: int
    ) -> None:
        """Test the `parallelise_dictionary_processing` function is called once correctly."""

        # Execute the `extract_attribute_from_dict_of_paginated_lists` function
        _ = extract_attribute_from_dict_of_paginated_lists(test_input_pl, test_input_attribute_name,
                                                           test_input_cpu_count, test_input_max_chunksize)

        # Assert `parallelise_dictionary_processing` function is called once correctly
        patch_extract_attribute_from_dict_of_paginated_lists_parallelise_dictionary_processing.assert_called_once_with(
            patch_extract_attribute_from_dict_of_paginated_lists_partial.return_value, test_input_pl.keys(),
            test_input_cpu_count, test_input_max_chunksize
        )

    def test_returns_correctly(
            self, patch_extract_attribute_from_dict_of_paginated_lists_partial: MagicMock,
            patch_extract_attribute_from_dict_of_paginated_lists_parallelise_dictionary_processing: MagicMock,
            test_input_pl: Dict[str, Any], test_input_attribute_name: str, test_input_cpu_count: int,
            test_input_max_chunksize: int
    ) -> None:
        """Test the function returns correctly."""

        # Execute the `extract_attribute_from_dict_of_paginated_lists` function
        test_output = extract_attribute_from_dict_of_paginated_lists(test_input_pl, test_input_attribute_name,
                                                                     test_input_cpu_count, test_input_max_chunksize)

        # Assert the return is as expected
        assert test_output == patch_extract_attribute_from_dict_of_paginated_lists_parallelise_dictionary_processing\
            .return_value
