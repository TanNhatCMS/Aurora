import os
import sys
import json
import ctypes

LANG_CODES = {
    "English":    "en",
    "Türkçe":     "tr",
    "中文":        "cn",
    "日本語":      "jp",
    "Español":    "es",
    "Deutsch":    "de",
    "Tiếng Việt": "vi",
    "Nederlands":      "nl",
}
LANG_NAMES = {v: k for k, v in LANG_CODES.items()}

# Config keys — use these instead of raw strings
class Key:
    GAME_PATH         = "game_path"
    LANGUAGE          = "language"
    DEV_MODE          = "dev_mode"
    CENSORSHIP_REMOVE = "csn_rem"
    NO_DRIVE_LINE     = "drv_lin"
    DISCORD_RPC       = "discord_rpc"
    EXTENSIVE_LOGGING = "extensive_logging"
    EXPORT_CONSOLE    = "export_console"
    UI_SCALING        = "ui_scaling"
    UI_MINIMIZATION   = "ui_min"

# Map Windows primary language IDs to Aurora language codes
_PRIMARY_LANG_TO_AURORA = {
    0x09: "en",   # English
    0x07: "de",   # German
    0x0A: "es",   # Spanish
    0x1F: "tr",   # Turkish
    0x2A: "vi",   # Vietnamese
    0x04: "cn",   # Chinese
    0x11: "jp",   # Japanese
}

def detect_system_language() -> str:
    """Detect the Windows display language and return the matching Aurora
    language code. Falls back to 'en' if detection fails or the language
    isn't supported."""
    try:
        # GetUserDefaultUILanguage returns the LANGID of the current user's
        # display language (e.g. 0x0409 for en-US, 0x042a for vi-VN).
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        # Extract the primary language ID (low 10 bits)
        primary = lang_id & 0x03FF
        return _PRIMARY_LANG_TO_AURORA.get(primary, "en")
    except Exception:
        return "en"

DEFAULTS = {
    Key.GAME_PATH:         "",
    Key.LANGUAGE:          "en",
    Key.DEV_MODE:          False,
    Key.CENSORSHIP_REMOVE: True,
    Key.NO_DRIVE_LINE:     False,
    Key.DISCORD_RPC:       True,
    Key.EXTENSIVE_LOGGING: False,
    Key.UI_SCALING:        1.0,
    Key.UI_MINIMIZATION:   True,
}

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(get_app_dir(), "config.json")

def _load_raw() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        if os.path.getsize(CONFIG_FILE) == 0:
            return {}
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def _save_raw(data: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        pass

def get(key: str):
    return _load_raw().get(key, DEFAULTS.get(key))

def set(key: str, value):
    data = _load_raw()
    data[key] = value
    _save_raw(data)
