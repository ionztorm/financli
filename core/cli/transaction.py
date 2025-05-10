import argparse

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from core.db import get_connection
from utils.helpers import msg
from core.controller import Controller
from utils.constants import ACCOUNT_TYPES, TRANSACTION_TYPES
from core.utils.validator import TYPE_VALIDATORS
from core.cli.utils.print_table import print_table

transaction_type_map = {
    "withdraw": "withdraw",
    "deposit": "deposit",
    "pay another account": "transfer",
    "payment": "pay_only",
}


def register_transact_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "transaction",
        help=(
            "Add a transaction such as a withdrawal, "
            "deposit, pay a bill, or make a purchase."
        ),
    )

    parser.add_argument("--date", type=str, help="The date of the transaction")

    parser.add_argument("--type", type=str, help="Type of transaction")

    parser.add_argument(
        "--source-type",
        type=str,
        help="Type of account that is the source of the funds",
    )

    parser.add_argument(
        "--source-id",
        type=int,
        help="ID of the account that is the source of the funds",
    )

    parser.add_argument(
        "--source-provider",
        type=str,
        help="The name of the provider of the source account",
    )

    parser.add_argument(
        "--destination-type",
        type=str,
        help="Type of account that will receive the funds",
    )

    parser.add_argument(
        "--destination-id",
        type=int,
        help="ID of the account that will receive the funds",
    )

    parser.add_argument(
        "--destination-provider",
        type=str,
        help="The name of the provider that will receive the amount",
    )

    parser.add_argument(
        "--description", type=str, help="Transaction description"
    )

    parser.add_argument(
        "--amount", type=float, help="The value of the transaction"
    )

    parser.set_defaults(func=handle_transaction)


int_validator = TYPE_VALIDATORS.get(int, EmptyInputValidator())
str_validator = TYPE_VALIDATORS.get(str, EmptyInputValidator())
float_validator = TYPE_VALIDATORS.get(float, EmptyInputValidator())


def handle_transaction(args: argparse.Namespace) -> None:
    conn = get_connection()
    model = Controller(conn)

    date = args.date
    transaction_type = args.type
    source_type = args.source_type
    source_id = args.source_id
    source_provider = args.source_provider
    destination_type = args.destination_type
    destination_id = args.destination_id
    destination_provider = args.destination_provider
    description = args.description
    amount = args.amount

    if not date:
        date = inquirer.text(
            message="What was the date of the transaction? (mm/dd/yy): "
        ).execute()

    if not transaction_type:
        transaction_type = inquirer.select(
            message="Choose a transaction type: ",
            choices=list(TRANSACTION_TYPES),
        ).execute()

    if transaction_type_map[transaction_type] != "deposit":
        source_data = _handle_accounts(source_id, source_type, "source", model)
        source_type = source_data["account_type"]
        source_id = source_data["id"]
        source_provider = source_data["provider"]

    if transaction_type_map[transaction_type] != "withdraw":
        destination_data = _handle_accounts(
            destination_id, destination_type, "destination", model
        )
        destination_type = destination_data["account_type"]
        destination_id = destination_data["id"]
        destination_provider = destination_data["provider"]

    if not description:
        description = inquirer.text(
            message="Describe the transaction: ", validate=str_validator
        ).execute()

    if not amount:
        amount = inquirer.text(
            message="Enter the value of the transaction: ",
            validate=float_validator,
        ).execute()

    data = {
        "date": date,
        "transaction_type": transaction_type_map[transaction_type],
        "source_type": source_type,
        "source_id": source_id,
        "source_provider": source_provider,
        "destination_type": destination_type,
        "destination_id": destination_id,
        "destination_provider": destination_provider,
        "description": description,
        "amount": amount,
    }

    try:
        model.transaction(data)
    except Exception as e:
        msg(f"{e}")
        return

    msg("Transaction logged!")
    print_table(model.list({"account_type": "transaction"}))


def _handle_accounts(
    id: int, account_type: str, transaction: str, model: Controller
) -> dict:
    data = {}

    if not account_type:
        data["account_type"] = inquirer.select(
            message=f"Select the funds {transaction} account type: ",
            choices=ACCOUNT_TYPES,
        ).execute()

    print(f"Account Type: {account_type}")
    accounts = model.list({"account_type": data["account_type"]})

    if not accounts:
        msg(
            f"There are currently no {account_type} accounts. "
            "Try opening one first"
        )
        return {}

    print_table(accounts)

    if not id:
        data["id"] = inquirer.text(
            message=f"Enter the ID of the {transaction} account: ",
            validate=int_validator,
        ).execute()

    account = model.list(
        {"account_type": data["account_type"], "id": data["id"]}
    )
    if not account:
        msg(f"Cannot find {account_type} id {id}")
        return {}

    alias = account[0].get("alias")
    data["provider"] = (
        f"{account[0]['provider']} ({alias})"
        if alias
        else account[0]["provider"]
    )

    return data
