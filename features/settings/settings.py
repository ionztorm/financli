import json

from pathlib import Path

from utils.helpers import msg
from utils.constants import SETTINGS_PATH


class SettingsManager:
    def __init__(self, path: Path = SETTINGS_PATH) -> None:
        self.path = path
        self.settings = self._load_or_create_settings()
        self._verify_required_settings()

    def _load_or_create_settings(self) -> dict:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            settings = self._prompt_for_initial_settings()
            self._save_settings(settings)
            print(f"✅ Settings saved to {self.path}")
        else:
            with self.path.open() as f:
                settings = json.load(f)
        return settings

    def _prompt_for_initial_settings(self) -> dict:
        return {
            "currency_symbol": self._get_currency_symbol(),
            "export_path": self._get_export_path(),
        }

    def _verify_required_settings(self) -> None:
        if (
            "currency_symbol" not in self.settings
            or not self.settings["currency_symbol"].strip()
        ):
            msg("⚠️  Missing 'currency_symbol'.")
            self.set("currency_symbol", self._get_currency_symbol())

        if (
            "export_path" not in self.settings
            or not self.settings["export_path"].strip()
        ):
            msg("⚠️  Missing 'export_path'.")
            self.set("export_path", self._get_export_path())

    def _save_settings(self, settings: dict) -> None:
        with self.path.open("w") as f:
            json.dump(settings, f, indent=2)

    def _get_currency_symbol(self) -> str:
        return (
            input(
                "💱 Enter your preferred currency symbol (e.g. £, $, €): "
            ).strip()
            or "£"
        )

    def _get_export_path(self) -> str:
        path = input(
            "📁 Enter your preferred export path (default: ~/exports): "
        ).strip()
        resolved = Path(path or Path.home() / "exports").expanduser()

        resolved.mkdir(parents=True, exist_ok=True)

        return str(resolved)

    def get(self, key: str) -> str | None:
        if key not in self.settings:
            msg(f"{key} not found!")
            return None
        return self.settings[key]

    def set(self, key: str, value: str) -> None:
        self.settings[key] = value
        self._save_settings(self.settings)
