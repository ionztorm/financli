from functools import lru_cache

from features.settings.settings import SettingsManager


@lru_cache(maxsize=1)
def get_settings() -> SettingsManager:
    return SettingsManager()


def get_currency() -> str:
    return get_settings().get("currency_symbol") or "£"
