from typing import Callable
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
