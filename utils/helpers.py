import json

from typing import Callable
from pathlib import Path
from functools import wraps

from tabulate import tabulate

CONFIG_DIR = Path.home() / ".config" / "budget_cli"
SETTINGS_PATH = CONFIG_DIR / "settings.json"


def pretty_output(func: Callable[..., None]) -> Callable[..., None]:
    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        print("\n")
        func(*args, **kwargs)
        print("\n")

    return wrapper


@pretty_output
def msg(message: str) -> None:
    print(message)


@pretty_output
def print_table(data: list[dict]) -> None:
    """
    Print a list of dictionaries as a formatted table with spacing.

    Args:
        data (list of dict): The rows to display.
    """
    if not data:
        return

    currency = load_or_create_settings().get("currency_symbol", "£")

    currency_fields = ["limiter", "balance", "amount", "monthly_charge"]
    formatted_data = format_currency_fields(
        data, currency_fields, symbol=currency
    )

    print(tabulate(formatted_data, headers="keys", tablefmt="github"))


def format_currency_fields(
    data: list[dict], fields: list[str], symbol: str = "£"
) -> list[dict]:
    for row in data:
        for field in fields:
            if field in row and isinstance(row[field], (int, float)):
                row[field] = f"{symbol}{row[field]:,.2f}"
    return data


def wrap_error(
    domain_exc: type[Exception],
    message: str = "",
) -> Callable[[Exception], Exception]:
    def wrapper(original_exc: Exception) -> Exception:
        clean_msg = message.rstrip(".: ")
        if original_exc.args:
            if clean_msg:
                clean_msg += f": {original_exc}"
            else:
                clean_msg = str(original_exc)
        return domain_exc(clean_msg)

    return wrapper


def load_or_create_settings() -> dict:
    if not SETTINGS_PATH.exists():
        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        currency = (
            input(
                "💱 Enter your preferred currency symbol (e.g. £, $, €): "
            ).strip()
            or "£"
        )
        settings = {"currency_symbol": currency}
        with SETTINGS_PATH.open("w") as f:
            json.dump(settings, f, indent=2)
        print(f"✅ Settings saved to {SETTINGS_PATH}")
        return settings
    with SETTINGS_PATH.open() as f:
        return json.load(f)
