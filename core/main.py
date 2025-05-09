import argparse

from core.db import create_data_path
from core.cli.list import register_list_command
from core.cli.open import register_open_command
from utils.helpers import load_or_create_settings
from core.cli.close import register_close_command
from core.cli.export import register_export_command
from core.cli.update import register_update_command
from core.cli.imports import register_import_command
from core.cli.transaction import register_transact_command


def main() -> None:
    create_data_path()
    load_or_create_settings()

    parser = argparse.ArgumentParser(
        prog="fcli",
        description=(
            "💸 FinanCLI - Manage your personal finances from the terminal."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    register_open_command(subparsers)
    register_close_command(subparsers)
    register_transact_command(subparsers)
    register_update_command(subparsers)
    register_list_command(subparsers)
    register_export_command(subparsers)
    register_import_command(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
