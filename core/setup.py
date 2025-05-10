from utils.loader import get_settings
from features.settings.settings import SettingsManager


def setup() -> SettingsManager:
    return get_settings()
