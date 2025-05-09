import json
import argparse

from pathlib import Path

from InquirerPy import inquirer

from core.db import get_connection
from utils.helpers import msg
from core.controller import Controller
from utils.constants import EXTENDED_MENU


def register_export_command(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "export", help="Export account data to a file."
    )
    parser.add_argument(
        "--account-type", type=str, help="Type of account to export"
    )
    parser.add_argument(
        "--filetype",
        type=str,
        choices=["json", "csv", "txt"],
        help="Export format",
    )
    parser.add_argument(
        "--path", type=str, help="File path to save exported data"
    )
    parser.set_defaults(func=handle_export)


def handle_export(args: argparse.Namespace) -> None:
    conn = get_connection()
    model = Controller(conn)

    account_type = args.account_type
    if not account_type:
        account_type = inquirer.select(
            message="Choose account type to export:",
            choices=EXTENDED_MENU,
        ).execute()

    records = model.list({"account_type": account_type})
    if not records:
        msg(f"No {account_type} accounts found to export.")
        return

    file_format = args.filetype
    if not file_format:
        file_format = inquirer.select(
            message="Select export format:",
            choices=["json", "csv", "txt"],
        ).execute()

    if args.path:
        output_file = Path(args.path).expanduser().resolve()
    else:
        default_name = f"{account_type}_accounts.{file_format}"
        selected_path = inquirer.filepath(
            message="Choose where to save the file:",
            default=default_name,
            only_files=True,
            validate=lambda p: p.endswith(f".{file_format}"),
        ).execute()
        output_file = Path(selected_path).expanduser().resolve()

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        if file_format == "json":
            output_file.write_text(json.dumps(records, indent=4))
        elif file_format == "csv":
            import csv

            with output_file.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)

        elif file_format == "txt":
            lines = [str(record) for record in records]
            output_file.write_text("\n".join(lines))
        else:
            msg(f"Unsupported format: {file_format}")
            return

        msg(f"{len(records)} {account_type} records exported to {output_file}")
    except Exception as e:
        msg(f"Failed to export data: {e}")
