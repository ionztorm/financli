import sqlite3

from utils.types import IDKeys, TableName, AccountRole, AccountTypeKeys
from utils.constants import TYPE_CONFIG
from utils.model_types import ModelType
from features.payable.bill.model import Bills
from features.accounts.bank.model import Bank
from features.accounts.store_card.model import StoreCard
from features.accounts.credit_card.model import CreditCard
from features.payable.subscription.model import Subscriptions


class UtilityService:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.bank_model = Bank(db_connection)
        self.credit_card_model = CreditCard(db_connection)
        self.store_card_model = StoreCard(db_connection)
        self.bill_model = Bills(db_connection)
        self.subscription_model = Subscriptions(db_connection)

        self.valid_account_types = self._get_valid_account_types()
        self.source_types = self.valid_account_types["source_types"]
        self.destination_types = self.valid_account_types["dest_types"]

        self._model_map: dict[str, ModelType] = {
            TYPE_CONFIG[TableName.BANKS]["display_name"]: self.bank_model,
            TYPE_CONFIG[TableName.CREDITCARDS][
                "display_name"
            ]: self.credit_card_model,
            TYPE_CONFIG[TableName.STORECARDS][
                "display_name"
            ]: self.store_card_model,
        }

    def _get_valid_account_types(self) -> dict:
        source_types = []
        dest_types = []
        for config in TYPE_CONFIG.values():
            if config.get("is_source"):
                source_types.append(config.get("display_name"))
            if config.get("is_destination"):
                dest_types.append(config.get("display_name"))
        return {
            "source_types": source_types,
            "dest_types": dest_types,
        }

    def _require_non_empty_str(self, value: object, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        return value

    def _get_account_type_and_id(
        self, data: dict, expected_role: AccountRole
    ) -> tuple[str, int]:
        if expected_role == AccountRole.SOURCE:
            account_type = self._get_account_type(
                data, AccountTypeKeys.SOURCE_TYPE
            )
            account_id = self._get_id(data, IDKeys.SOURCE_ID)
        elif expected_role == AccountRole.DESTINATION:
            account_type = self._get_account_type(
                data, AccountTypeKeys.DESTINATION_TYPE
            )
            account_id = self._get_id(data, IDKeys.DESTINATION_ID)
        else:
            raise ValueError(f"Invalid account role: {expected_role.value}")

        return account_type, account_id

    def _get_account_type(
        self, data: dict, expected_key: AccountTypeKeys
    ) -> str:
        account_type = data.get(expected_key.value)
        if not account_type:
            raise ValueError(f"{expected_key.value} not found in the data.")
        return self._require_non_empty_str(account_type, "Account type")

    def _get_id(self, data: dict, expected_key: IDKeys) -> int:
        account_id = data.get(expected_key.value)
        if account_id is None:
            raise ValueError(f"{expected_key.value} not found in the data.")
        try:
            return int(account_id)
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"{expected_key.value} must be convertible to an integer."
            ) from e

    def _get_amount(self, data: dict) -> float:
        amount_raw = data.get("amount")
        if amount_raw is None:
            raise ValueError("Amount is required.")
        try:
            return float(amount_raw)
        except (ValueError, TypeError) as e:
            raise ValueError("Amount must be convertible to a float.") from e

    def _get_model(self, account_type: str) -> ModelType:
        model = self._model_map.get(account_type)
        if not model:
            raise ValueError(f"No model found for account type: {account_type}")
        return model

    def _get_source_model(self, account_type: str) -> ModelType:
        if account_type not in self.source_types:
            raise ValueError(f"Unsupported source account type: {account_type}")
        return self._get_model(account_type)

    def _get_destination_model(self, account_type: str) -> ModelType:
        if account_type not in self.destination_types:
            raise ValueError(
                f"Unsupported destination account type: {account_type}"
            )
        return self._get_model(account_type)
