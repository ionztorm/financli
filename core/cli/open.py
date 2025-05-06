import argparse

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from core.db import get_connection
from utils.helpers import print_table
from core.controller import Controller
from core.utils.validator import TYPE_VALIDATORS

REQUIRED_FIELDS = {
    "bank": [
        ("provider", str),
        ("balance", float),
        ("alias", str),
        ("limiter", float),
    ],
    "credit card": [("provider", str), ("balance", float), ("limiter", float)],
    "store card": [("provider", str), ("balance", float), ("limiter", float)],
    "loan": [("provider", str), ("balance", float)],
    "subscription": [("provider", str), ("monthly_charge", float)],
    "bill": [("provider", str), ("monthly_charge", float)],
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

    required_fields = REQUIRED_FIELDS.get(account_type, [])
    data = {"account_type": account_type}

    for field, field_type in required_fields:
        cli_value = getattr(args, field, None)

        if cli_value is not None:
            try:
                data[field] = field_type(cli_value)
            except ValueError:
                print(
                    f"Invalid value for {field}. "
                    f"Expected {field_type.__name__}."
                )
                return
        else:
            validator = TYPE_VALIDATORS.get(field_type, EmptyInputValidator())

            user_input = inquirer.text(
                message=f"Enter {field.replace('_', ' ')}:",
                validate=validator,
            ).execute()

            data[field] = field_type(user_input)

    conn = get_connection()
    model = Controller(conn)

    try:
        model.open(data)
    except Exception as e:
        print(f"{e}\n")
        return

    updated_list = model.list({"account_type": account_type})

    print(f"\n{data['provider']} created.")
    print_table(updated_list)
