import random
from utils import safe_input, clamp
import logger
import config

class InternalPolicyManager:
    def __init__(self, game):
        self.game = game

    def policy_menu(self):
        while True:
            print("\n--- ВНУТРЕННЯЯ ПОЛИТИКА ---")
            print(f"Налоговая ставка: {self.game.tax_rate}")
            print(f"Военная реформа: {'✅' if self.game.reforms['military'] else '❌'}")
            print(f"Экономическая реформа: {'✅' if self.game.reforms['economic'] else '❌'}")
            print(f"Социальная реформа: {'✅' if self.game.reforms['social'] else '❌'}")
            print("\n1. Изменить налоги")
            print("2. Провести военную реформу (1000💰, +15% к силе армии)")
            print("3. Провести экономическую реформу (1500💰, +20% к доходу)")
            print("4. Провести социальную реформу (800💰, +15 к стабильности)")
            print("5. Назначить наследника (если есть)")
            print("6. Назад")
            choice = safe_input("Выбор: ", valid_options=["1","2","3","4","5","6"], default="6")
            if choice == "6":
                break
            elif choice == "1":
                self.change_tax_rate()
            elif choice == "2":
                self.apply_reform("military")
            elif choice == "3":
                self.apply_reform("economic")
            elif choice == "4":
                self.apply_reform("social")
            elif choice == "5":
                self.set_heir()

    def change_tax_rate(self):
        print("\nТекущая налоговая ставка:", self.game.tax_rate)
        print("1. Низкая (доход -20%, стабильность +15)")
        print("2. Средняя (без изменений)")
        print("3. Высокая (доход +20%, стабильность -15)")
        choice = safe_input("Выбор: ", valid_options=["1","2","3"], default="2")
        if choice == "1":
            self.game.tax_rate = "низкая"
            self.game.player_income = int(self.game.player_income * 0.8)
            self.game.stability = min(100, self.game.stability + 15)
            logger.log("Налоги снижены до низких", "INFO")
        elif choice == "2":
            self.game.tax_rate = "средняя"
            logger.log("Налоги средние", "INFO")
        elif choice == "3":
            self.game.tax_rate = "высокая"
            self.game.player_income = int(self.game.player_income * 1.2)
            self.game.stability = max(0, self.game.stability - 15)
            logger.log("Налоги повышены до высоких", "WARNING")
        print(f"✅ Налоговая ставка изменена на {self.game.tax_rate}")

    def apply_reform(self, reform_type):
        if self.game.reforms[reform_type]:
            print("Эта реформа уже проведена!")
            return
        cost = 1000 if reform_type == "military" else (1500 if reform_type == "economic" else 800)
        if self.game.player_gold < cost:
            print(f"❌ Недостаточно золота! Нужно {cost}💰")
            return
        self.game.player_gold -= cost
        self.game.reforms[reform_type] = True
        if reform_type == "military":
            self.game.total_army_power = int(self.game.total_army_power * 1.15)
            print("✅ Военная реформа проведена! Сила армии +15%.")
        elif reform_type == "economic":
            self.game.player_income = int(self.game.player_income * 1.2)
            print("✅ Экономическая реформа проведена! Доход +20%.")
        elif reform_type == "social":
            self.game.stability = min(100, self.game.stability + 15)
            print("✅ Социальная реформа проведена! Стабильность +15.")
        logger.log(f"Проведена реформа: {reform_type}", "INFO")

    def set_heir(self):
        print("\nВыберите наследника:")
        names = ["Александр", "Николай", "Пётр", "Екатерина", "Анна", "Иван", "Константин"]
        bonuses = ["military", "economist", "diplomat", "scientist"]
        for idx, name in enumerate(names, 1):
            print(f"{idx}. {name}")
        print(f"{len(names)+1}. Назад")
        choice = safe_input("Выбор: ")
        try:
            idx = int(choice) - 1
            if idx == len(names):
                return
            name = names[idx]
        except:
            return
        bonus = random.choice(bonuses)
        effect = random.randint(5, 15)
        self.game.heir = {"name": name, "bonus": bonus, "effect": effect, "age": 20, "years_rule": 0}
        print(f"👑 Наследник назначен: {name} ({bonus} +{effect})")
        logger.log(f"Назначен наследник: {name}", "INFO")

    def apply_policy_effects(self):
        # Применяем эффекты от налогов и реформ каждый ход
        if self.game.tax_rate == "низкая":
            self.game.stability = min(100, self.game.stability + 1)
        elif self.game.tax_rate == "высокая":
            self.game.stability = max(0, self.game.stability - 1)