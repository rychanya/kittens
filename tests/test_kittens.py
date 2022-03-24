"""Version tests"""
import toml

from kittens import __version__

FIX_VERSION = "4.0.0"


def test_version():
    """Test version"""
    assert __version__ == FIX_VERSION
    with open("pyproject.toml", "r", encoding="utf8") as file:
        settings = toml.load(file)
        assert settings["tool"]["poetry"]["version"] == FIX_VERSION
