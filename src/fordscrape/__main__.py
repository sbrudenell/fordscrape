import argparse
import pathlib
from collections.abc import Callable
from typing import cast

from fordscrape.state import State


def _init(args: argparse.Namespace) -> int:
    state = State(args.state_path)
    extra_params = {}
    for param_key_value in args.param or []:
        split = param_key_value.split("=")
        if len(split) != 2:
            raise ValueError()
        name, value = split
        extra_params[name] = value
    state.initialize(
        make=args.make, model=args.model, market=args.market, **extra_params
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser("fordscrape")

    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser("init")
    parser_init.add_argument("state_path", type=pathlib.Path)
    parser_init.add_argument("--make", default="Ford")
    parser_init.add_argument("--market", default="US")
    parser_init.add_argument("--model", required=True)
    parser_init.add_argument("--param", action="append")
    parser_init.set_defaults(func=_init)

    args = parser.parse_args()
    return cast(Callable[[argparse.Namespace], int], args.func)(args)


if __name__ == "__main__":
    raise SystemExit(main())
