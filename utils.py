import random

def get_date_str(turn):
    total_months = turn
    year = 1900 + (total_months // 12)
    month_idx = total_months % 12
    months = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    return f"{months[month_idx]} {year} года", year, month_idx + 1

def safe_input(prompt, valid_options=None, default=None):
    while True:
        user_input = input(prompt).strip()
        if not user_input and default is not None:
            return default
        if valid_options is None:
            return user_input
        if user_input in valid_options:
            return user_input
        print("❌ Неверный ввод. Попробуйте снова.")

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))