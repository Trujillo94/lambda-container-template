import os

from src.utils import toolbox


def test_load_env_var_exists():
    os.environ["TEST"] = "test"
    try:
        value = toolbox.load_env_var("TEST")
        assert value == "test"
    finally:
        os.environ.pop("TEST")


def test_load_env_var_not_exists():
    value = toolbox.load_env_var("__TEST__")
    assert value is None


def test_load_json_file(json_file):
    loaded_content = toolbox.load_json_file(json_file["file"])
    assert loaded_content == json_file["content"]
