import argparse

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from core.db import get_connection
from utils.helpers import msg, print_table
from core.controller import Controller
from utils.constants import FIELD_MAP, ACCOUNT_TYPES
from core.utils.validator import TYPE_VALIDATORS


def register_update_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("update", help="Update an accounts details.")
    parser.add_argument(
        "--account-type",
        type=str,
        help="The type of account you want to update",
    )

    parser.add_argument(
        "--id", type=int, help="The ID of the account you want to update"
    )

    parser.set_defaults(func=handle_update)


def handle_update(args: argparse.Namespace) -> None:
    conn = get_connection()
    model = Controller(conn)

    # 1) TODO: check for account type presence. Inquirer get if not
    account_type = args.account_type
    if not account_type:
        account_type = inquirer.select(
            message="Choose account type: ", choices=ACCOUNT_TYPES
        ).execute()

    # 2) TODO: display list of accounts with
    accounts = model.list({"account_type": account_type})

    if not accounts:
        msg(f"You do not currently have any {account_type} accounts.")
        return

    print_table(accounts)

    # 3) TODO: get ID of account to update
    validator = TYPE_VALIDATORS.get(int, EmptyInputValidator())

    id = args.id
    if not id:
        id = inquirer.text(
            message="Enter the ID of the account to update: ",
            validate=validator,
        ).execute()

    # 4) TODO: confirm correct account
    account = model.list({"account_type": account_type, "id": id})
    if not account:
        msg(f"No account was found with an ID of {id}")
        return

    print_table(account)

    confirmation = input(
        "You are updating this account. Is this correct? (y/n)"
    )
    if confirmation.lower() == "y":
        # 5) TODO: get updates
        # create map of required fields based on account type
        # loop through to create list of fields
        # use inquirer.select to allow user to select which field to update
        # after each selection, confirm if they want to update another field
        fields_with_types = FIELD_MAP.get(account_type.lower())
        if not fields_with_types:
            msg(f"No updatable fields defined for account type: {account_type}")
            return

        fields = [field for field, _ in fields_with_types]

        if not fields:
            msg(f"No updatable fields defined for account type: {account_type}")
            return

        updates = {}
        while True:
            field_to_update = inquirer.select(
                message="Select a field to update:",
                choices=[*fields, "Done"],
            ).execute()

            if field_to_update == "Done":
                break

            new_value = inquirer.text(
                message=f"Enter new value for '{field_to_update}':",
                validate=EmptyInputValidator(),
            ).execute()

            updates[field_to_update] = new_value

            continue_updating = inquirer.confirm(
                message="Update another field?", default=True
            ).execute()

            if not continue_updating:
                break

        # 6) TODO: try/except update
        data = {
            "account_type": account_type,
            "id": id,
            **updates,
        }

        try:
            model.update(data)
            msg("Account updated successfully.")
        except Exception as e:
            msg(f"Failed to update account: {e}")

        updated_account = model.list({"account_type": account_type, "id": id})

        if not updated_account:
            msg(f"Couldn't get the updated account details for {id} to display")
            return

        print_table(updated_account)
