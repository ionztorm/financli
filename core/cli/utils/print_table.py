from tabulate import tabulate

from utils.loader import get_currency
from utils.helpers import format_currency_fields
from utils.decorators import pretty_output


@pretty_output
def print_table(data: list[dict]) -> None:
    """
    Print a list of dictionaries as a formatted table with spacing.

    Args:
        data (list of dict): The rows to display.
    """
    if not data:
        return

    currency = get_currency()

    currency_fields = ["limiter", "balance", "amount", "monthly_charge"]
    formatted_data = format_currency_fields(
        data, currency_fields, symbol=currency
    )

    print("Your accounts: ")
    print(tabulate(formatted_data, headers="keys", tablefmt="github"))
