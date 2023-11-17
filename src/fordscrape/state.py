import pathlib
from collections.abc import Mapping
from typing import cast

import apsw


class State:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path

    @property
    def db_path(self) -> pathlib.Path:
        return self.path / "state.db"

    def initialize(self, *, make: str, model: str, market: str, **kwargs: str) -> None:
        search_params = {
            "make": make,
            "model": model,
            "market": market,
        }
        search_params.update(kwargs)
        self.path.mkdir()
        conn = apsw.Connection(str(self.db_path))
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE search_params (name TEXT NOT NULL, value TEXT NOT NULL)"
        )
        cur.execute("CREATE UNIQUE INDEX search_params_name ON search_params (name)")
        cur.executemany(
            "INSERT INTO search_params (name, value) VALUES (?, ?)",
            list(search_params.items()),
        )

    def get_search_params(self) -> Mapping[str, str]:
        conn = apsw.Connection(str(self.db_path))
        cur = conn.cursor()
        cur.execute("SELECT name, value FROM search_params")
        return dict(cast(list[tuple[str, str]], cur.fetchall()))
