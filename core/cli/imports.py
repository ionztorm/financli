import csv
import json
import argparse

from pathlib import Path

from InquirerPy import inquirer

from core.db import get_connection
from utils.helpers import msg
from core.controller import Controller
from utils.constants import EXTENDED_MENU


def register_import_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "import", help="Import account data from a file."
    )
    parser.add_argument(
        "--account-type", type=str, help="Type of account to import into"
    )
    parser.add_argument("--file", type=str, help="Path to the JSON or CSV file")
    parser.set_defaults(func=handle_import)


def handle_import(args: argparse.Namespace) -> None:
    conn = get_connection()
    model = Controller(conn)

    file_path = (
        args.file
        or inquirer.filepath(
            message="Select file to import:",
            only_files=True,
            validate=lambda p: p.endswith(".json") or p.endswith(".csv"),
        ).execute()
    )

    file = Path(file_path).expanduser().resolve()
    if not file.exists():
        msg(f"File not found: {file}")
        return

    account_type = (
        args.account_type
        or inquirer.select(
            message="Select account type to import into:",
            choices=EXTENDED_MENU,
        ).execute()
    )

    try:
        if file.suffix == ".json":
            records = json.loads(file.read_text())
        elif file.suffix == ".csv":
            with file.open(newline="") as f:
                reader = csv.DictReader(f)
                records = list(reader)
        else:
            msg("Unsupported file format.")
            return
    except Exception as e:
        msg(f"Failed to read file: {e}")
        return

    if not records:
        msg("No data found in file.")
        return

    success = 0
    for record in records:
        try:
            model.open({"account_type": account_type, **record})
            success += 1
        except Exception as e:
            msg(f"Failed to import record: {record}\nReason: {e}")

    msg(f"Imported {success} of {len(records)} records into {account_type}.")
