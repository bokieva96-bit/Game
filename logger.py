# logger.py
import sys
from datetime import datetime

class Logger:
    def __init__(self, filename="game.log", enabled=True):
        self.filename = filename
        self.enabled = enabled
        self.file = None
        if enabled:
            try:
                self.file = open(filename, "a", encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Не удалось открыть лог-файл: {e}")
                self.enabled = False

    def log(self, message, level="INFO"):
        if not self.enabled:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}\n"
        if self.file:
            self.file.write(line)
            self.file.flush()
        # Также выводим в консоль (можно убрать, если дублирует)
        print(f"📝 {message}")

    def close(self):
        if self.file:
            self.file.close()

# Глобальный экземпляр (создаётся в game.py)
logger = None