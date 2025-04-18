from typing import Callable, NoReturn
from functools import wraps


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
