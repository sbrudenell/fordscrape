import pathlib

import pytest
from fordscrape.state import State


@pytest.fixture
def state(tmp_path: pathlib.Path) -> State:
    return State(tmp_path / "state")


def test_initialize_default(state: State) -> None:
    state.initialize(make="testmake", model="testmodel", market="testmarket")
    assert state.get_search_params() == {
        "make": "testmake",
        "model": "testmodel",
        "market": "testmarket",
    }


def test_initialize_with_search_params(state: State) -> None:
    state.initialize(
        make="testmake", model="testmodel", market="testmarket", engine="testengine"
    )
    assert state.get_search_params() == {
        "make": "testmake",
        "model": "testmodel",
        "market": "testmarket",
        "engine": "testengine",
    }
