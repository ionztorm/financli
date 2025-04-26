from typing import Union

from features.payable.base import PayOnly
from features.accounts.base import Accounts

ModelType = Union[Accounts, PayOnly]
