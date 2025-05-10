import csv
import json
import argparse

from pathlib import Path
from datetime import datetime

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
    settings = args.settings

    account_type = (
        args.account_type
        or inquirer.select(
            message="Choose account type to export:",
            choices=EXTENDED_MENU,
        ).execute()
    )

    records = model.list({"account_type": account_type})
    if not records:
        msg(f"No {account_type} accounts found to export.")
        return

    file_format = (
        args.filetype
        or inquirer.select(
            message="Select export format:",
            choices=["json", "csv", "txt"],
        ).execute()
    )

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename = f"{timestamp}-{account_type}_accounts.{file_format}"

    output_file: Path | None = None

    if args.path:
        output_file = Path(args.path).expanduser().resolve()
    else:
        default_dir = Path(settings.get("export_path"))
        default_path = default_dir / filename

        choices = [
            {
                "name": "📁 Use default export path from settings",
                "value": "default",
            },
            {
                "name": "✏️  Enter a custom export path (one time)",
                "value": "custom",
            },
            {"name": "🛠  Set a new default export path", "value": "update"},
        ]
        export_choice = inquirer.select(
            message="Choose export path option:",
            choices=choices,
        ).execute()

        if export_choice == "default":
            output_file = default_path

        elif export_choice == "custom":
            custom_path = inquirer.filepath(
                message="Enter custom file path:",
                default=str(default_path),
                only_files=True,
                validate=lambda p: p.endswith(f".{file_format}"),
            ).execute()
            output_file = Path(custom_path).expanduser().resolve()

        elif export_choice == "update":
            new_default_dir = inquirer.filepath(
                message="Enter new default directory path:",
                default=str(default_dir),
                only_directories=True,
            ).execute()
            settings.set("export_path", str(Path(new_default_dir).expanduser()))
            output_file = Path(new_default_dir).expanduser() / filename

    if output_file is None:
        raise RuntimeError("Output file path could not be determined.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        if file_format == "json":
            output_file.write_text(json.dumps(records, indent=4))
        elif file_format == "csv":
            with output_file.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
        elif file_format == "txt":
            lines = [str(r) for r in records]
            output_file.write_text("\n".join(lines))

        msg(f"✅ Exported {len(records)} records to {output_file}")
    except Exception as e:
        msg(f"❌ Failed to export data: {e}")
