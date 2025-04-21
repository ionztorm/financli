import json

from typing import Callable, NoReturn
from pathlib import Path
from functools import wraps

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
