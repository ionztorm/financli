import argparse

from core.db.init import create_data_path
from core.utils.helpers import load_or_create_settings


def main() -> None:
    create_data_path()
    load_or_create_settings()

    parser = argparse.ArgumentParser(
        prog="budget",
        description=(
            "💸 Budget CLI - Manage your personal finances from the terminal."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
