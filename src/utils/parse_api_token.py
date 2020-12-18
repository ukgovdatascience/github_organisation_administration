from src.utils.logger import Log, logger
from py.path import local
from typing import Tuple, Union
import json


@Log(logger)
def parse_api_token(file: Union[str, local], key_username: str = "username",
                    key_token: str = "token") -> Tuple[str, str]:
    """Parse a JSON file containing an API username and token.

    Args:
        file: A JSON file containing a username and token, where the keys for each are key_username, and key_token.
        key_username: The username key in file.
        key_token: The token key in file.

    Returns:
        A tuple of two elements, where the first element is the username, and the second element is the token.

    """

    # Read and parse the JSON file, and return only the key_username, and key_token keys in the file
    with open(file, "r") as f:
        j = f.read()
    t = json.loads(j)
    return t[key_username], t[key_token]
