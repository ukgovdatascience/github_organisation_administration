from typing import Dict
from src.utils.parse_api_token import parse_api_token
import pytest

# Define arguments for the test_parse_api_token_returns_correctly test case
args_username_token = [
    ("hello", "world"),
    ("foo", "bar")
]
args_key_username_token = [
    ("username", "token"),
    ("user", "password")
]


@pytest.mark.parametrize("test_input_username, test_input_token", args_username_token)
@pytest.mark.parametrize("test_input_key_username, test_input_key_token", args_key_username_token)
def test_parse_api_token_returns_correctly(example_json_file: Dict[str, str], test_input_username: str,
                                           test_input_token: str, test_input_key_username: str,
                                           test_input_key_token: str) -> None:
    """Test that the parse_api_token returns correctly."""

    # Execute the parse_api_token function
    test_output = parse_api_token(example_json_file["path"], test_input_key_username, test_input_key_token)

    # Assert the returned output is correct
    assert test_output == (test_input_username, test_input_token)
