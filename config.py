# config.py
# Параметры игры, которые можно менять без правки кода

START_YEAR = 1900
END_YEAR = 1950
MAX_TURNS = (END_YEAR - START_YEAR) * 12  # 612

# Сложность (влияет на доход ИИ, агрессивность)
DIFFICULTY = "normal"  # "easy", "normal", "hard"

# Множители для игрока и ИИ
PLAYER_INCOME_MULTIPLIER = 1.0
AI_INCOME_MULTIPLIER = 1.0 if DIFFICULTY == "normal" else (0.8 if DIFFICULTY == "easy" else 1.2)
AI_AGGRESSIVENESS = 0.3 if DIFFICULTY == "normal" else (0.2 if DIFFICULTY == "easy" else 0.5)

# Логирование
LOG_TO_FILE = True
LOG_FILE = "game.log"

# Стартовые условия (можно переопределить в начале игры)
START_GOLD_MULTIPLIER = 1.0