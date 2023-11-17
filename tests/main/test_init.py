import pathlib

import pytest
from cli_test_helpers import shell
from fordscrape.state import State


@pytest.fixture
def new_state_path(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "state"


def test_no_args(new_state_path: pathlib.Path) -> None:
    result = shell(f"fordscrape init {new_state_path}")
    assert result.exit_code != 0


def test_minimum_args(new_state_path: pathlib.Path) -> None:
    result = shell(f"fordscrape init {new_state_path} --model=testmodel")
    assert result.exit_code == 0
    state = State(new_state_path)
    params = state.get_search_params()
    assert params["model"] == "testmodel"


def test_many_args(new_state_path: pathlib.Path) -> None:
    result = shell(
        f"fordscrape init {new_state_path} --model=testmodel "
        "--make=testmake --market=testmarket --param=engine=testengine "
        "--param=modeltrim=testmodeltrim"
    )
    assert result.exit_code == 0
    state = State(new_state_path)
    params = state.get_search_params()
    assert params["model"] == "testmodel"
    assert params["make"] == "testmake"
    assert params["market"] == "testmarket"
    assert params["engine"] == "testengine"
    assert params["modeltrim"] == "testmodeltrim"
