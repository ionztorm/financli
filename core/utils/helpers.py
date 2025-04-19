import json
from pathlib import Path
from typing import Callable, NoReturn
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
    domain_exc: type[Exception], prefix: str
) -> Callable[[Exception], NoReturn]:
    def wrapper(e: Exception) -> NoReturn:
        raise domain_exc(f"{prefix}: {e}") from e

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
