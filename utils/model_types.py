from typing import Union

from features.payable.base import Payable
from features.accounts.base import Accounts

ModelType = Union[Accounts, Payable]
