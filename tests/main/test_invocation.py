import importlib

from cli_test_helpers import shell


def test_main_module() -> None:
    importlib.import_module("fordscrape.__main__")


def test_runas_module() -> None:
    result = shell("python -m fordscrape --help")
    assert result.exit_code == 0


def test_entrypoint() -> None:
    result = shell("fordscrape --help")
    assert result.exit_code == 0
