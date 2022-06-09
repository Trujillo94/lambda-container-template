import os
import pytest
import json
import logging

__ENV_FILE = ".env"


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    if not os.path.exists(__ENV_FILE):
        pytest.exit(f"Please create and fill environment variables in '{__ENV_FILE}' before running the tests.")


@pytest.fixture(autouse=True)
def log_level(caplog):
    """
    Fixture to set the log level on all tests

    :param caplog: Pytest built-in fixture with the log configuration
    """
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def json_file():
    """
    Fixture to create a JSON file to be read/modified.
    Once done, the JSON file is removed even if there are exceptions.
    """

    content = {
      "12345": "a",
      "54321": "b"
    }
    json_file = "./test.json"

    with open(json_file, "w") as file:
        file.write(json.dumps(content, indent=4))
    try:
        yield {
            "file": json_file,
            "content": content
        }
    finally:
        os.remove(json_file)
