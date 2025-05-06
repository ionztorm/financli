import argparse

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from core.db import get_connection
from utils.helpers import msg, print_table
from core.controller import Controller
from core.utils.validator import TYPE_VALIDATORS

ACCOUNT_TYPES = [
    "bank",
    "credit card",
    "store card",
    "loan",
    "subscription",
    "bill",
]


def register_close_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("close", help="Close an account")
    parser.add_argument(
        "--account-type", type=str, help="The type of account to close."
    )
    parser.add_argument("--id", type=int, help="ID of the account to close.")
    parser.set_defaults(func=handle_close)


def handle_close(args: argparse.Namespace) -> None:
    conn = get_connection()
    model = Controller(conn)

    account_type = args.account_type
    if not account_type:
        account_type = inquirer.select(
            message="Choose account type:",
            choices=list(ACCOUNT_TYPES),
        ).execute()

    accounts = model.list({"account_type": account_type})

    if not accounts:
        msg(f"You do not currently have any {account_type} accounts.")
        return

    print_table(accounts)

    validator = TYPE_VALIDATORS.get(int, EmptyInputValidator())

    id = args.id
    if not id:
        id = inquirer.text(
            message="Enter the ID of the account to close: ",
            validate=validator,
        ).execute()

    try:
        model.close(account_type, id)
    except Exception as e:
        msg(f"{e}")
        return

    msg("The account was successfully closed. ")

    updated_accounts = model.list({"account_type": account_type})

    if not updated_accounts:
        return

    print_table(updated_accounts)
