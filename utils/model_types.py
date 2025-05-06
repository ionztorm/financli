from typing import Union

from features.payable.base import PayOnly
from features.accounts.base import Accounts
from features.transactions.model import Transaction

ModelType = Union[Accounts, PayOnly, Transaction]
