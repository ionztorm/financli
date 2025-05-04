import argparse

from InquirerPy import inquirer

from core.db import get_connection
from utils.helpers import print_table
from core.controller import Controller

REQUIRED_FIELDS = {
    "bank": {"provider", "balance", "alias", "limiter"},
    "credit card": {"provider", "balance", "limiter"},
    "store card": {"provider", "balance", "limiter"},
    "loan": {"provider", "balance"},
    "subscription": {"provider", "monthly_charge"},
    "bill": {"provider", "monthly_charge"},
}


def register_open_command(subparsers: argparse._SubParsersAction) -> None:
    open_parser = subparsers.add_parser(
        "open",
        help=(
            "Create a new account of type Bank, Credit Card, "
            "Store Card, Loan, Subscription, or Bill."
        ),
    )

    open_parser.add_argument(
        "--account-type",
        choices=["bank", "credit", "store", "loan", "subscription", "bill"],
        help="Type of account to open",
    )

    open_parser.add_argument(
        "--provider", help="The name of the company or bank."
    )

    open_parser.add_argument(
        "--balance",
        help="The current balance of the account. "
        "Not valid for Subscriptions or Bills.",
    )

    open_parser.add_argument(
        "--alias",
        help=(
            "An alias for the account. Useful if you have multiple accounts"
            " with the same provider."
        ),
    )

    open_parser.add_argument(
        "--limiter",
        help=(
            "Used if the account has some kind of limit mechanism."
            "For example, your bank account may have an overdraft, or your "
            "credit card may have a credit limit."
        ),
    )

    open_parser.add_argument(
        "--monthly-charge", help=("Only applicable to subscriptions and bills.")
    )

    open_parser.set_defaults(func=handle_open)


def handle_open(args: argparse.Namespace) -> None:
    account_type = args.account_type
    if not account_type:
        account_type = inquirer.select(
            message="Choose account type:",
            choices=list(REQUIRED_FIELDS.keys()),
        ).execute()

    required_fields = REQUIRED_FIELDS.get(account_type, set())

    data = {"account_type": account_type}
    for field in required_fields:
        cli_value = getattr(args, field, None)
        if cli_value is not None:
            data[field] = cli_value
        else:
            data[field] = inquirer.text(
                message=f"Enter {field.replace('_', ' ')}:"
            ).execute()

    conn = get_connection()
    model = Controller(conn)

    model.open(data)
    updated_list = model.list({"account_type": account_type})

    print(f"\n{data['provider']} created.")
    print_table(updated_list)
