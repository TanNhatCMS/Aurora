import os
import sys
import json
from src.logger import logger
from PyQt6.QtCore import QObject, pyqtSignal
from src.utils import resource_path

class _Translator(QObject):
    language_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._strings: dict = {}
        self._lang: str = "en"
        
        self._lang_dir = resource_path("Lang")

    def load(self, lang_code: str):
        path = os.path.join(self._lang_dir, f"{lang_code}.json")
        
        if not os.path.exists(path):
            logger.warning(f"Language file not found ({path}), Aurora will fall to English translation.")
            path = os.path.join(self._lang_dir, "en.json")
            lang_code = "en"
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._strings = json.load(f)
            self._lang = lang_code
        except Exception as e:
            print(f"Error loading translation: {e}")
            self._strings = {}
            
        self.language_changed.emit()

    def t(self, key: str) -> str:
        return self._strings.get(key, key)

Translator = _Translator()
t = Translator.t
