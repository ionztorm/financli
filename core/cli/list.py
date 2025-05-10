import argparse

from InquirerPy import inquirer

from core.db import get_connection
from utils.helpers import msg
from core.controller import Controller
from utils.constants import EXTENDED_MENU
from core.cli.utils.print_table import print_table


def register_list_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "list", help="List all registered accounts of a specified account type."
    )

    parser.add_argument(
        "--account-type", type=str, help="The type of account you want to list."
    )

    parser.set_defaults(func=handle_list)


def handle_list(args: argparse.Namespace) -> None:
    conn = get_connection()
    model = Controller(conn)

    account_type = args.account_type
    if not account_type:
        account_type = inquirer.select(
            message="Please select an account type: ", choices=EXTENDED_MENU
        ).execute()

    accounts = model.list({"account_type": account_type})

    if not accounts:
        msg(f"No {account_type} accounts found.")
        return

    print_table(accounts)
