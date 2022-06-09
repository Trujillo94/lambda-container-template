import json
import logging
import os

logger = logging.getLogger("Toolbox")


def load_env_var(key):
    """
    Returns the value of the environment variable or None if not found.

    :param key: Environment variable key
    :return: The environment variable value, or None
    """
    value = os.environ.get(key)

    if value is None:
        logger.warning(f"Environment variable '{key}' not found.")
    return value


def load_json_file(json_file_path):
    """
    Loads a JSON file content into a dict object.
    :param json_file_path: path to the JSON file
    :return: The dict object with the JSON content
    """

    with open(json_file_path, "r") as json_file:
        content = json.load(json_file)

    return content
