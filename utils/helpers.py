from typing import Callable

from utils.decorators import pretty_output


@pretty_output
def msg(message: str) -> None:
    print(message)


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
