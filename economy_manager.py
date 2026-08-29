# managers/economy_manager.py
import random
from utils import safe_input, clamp

class EconomyManager:
    def __init__(self, game):
        self.game = game  # ссылка на главный объект игры

    # ---------- ЦЕНЫ НА ЗДАНИЯ ----------
    def get_current_price(self, building_type):
        base_prices = {
            "шахта": 400, "завод": 600, "банк": 600, "военный завод": 500,
            "военная база": 700, "нефтяная вышка": 400, "ферма": 300,
            "железный рудник": 450, "угольная шахта": 420, "лесопилка": 350,
            "урановая шахта": 800, "золотой рудник": 900
        }
        base = base_prices.get(building_type, 500)
        years = self.game.turn // 12
        return int(base * (1 + 0.02 * years))

    # ---------- ПРИМЕНЕНИЕ БОНУСОВ ОТ ЗДАНИЙ ----------
    def apply_building_bonuses(self):
        # Получаем базовый доход игрока из countries_data
        base_income = 0
        for data in self.game.countries_data.values():
            if data["name"] == self.game.player_name:
                base_income = data["income"]
                break

        bonus_income = 0
        percent_bonus = 0
        resource_bonus = {
            "нефть": 0, "сталь": 0, "продовольствие": 0,
            "железо": 0, "уголь": 0, "дерево": 0, "уран": 0, "золото": 0
        }

        for b in self.game.buildings:
            typ = b["type"]
            if typ == "шахта":
                bonus_income += 15
                resource_bonus["сталь"] += 5
                resource_bonus["железо"] += 3
            elif typ == "завод":
                bonus_income += 25
                resource_bonus["сталь"] += 10
            elif typ == "банк":
                percent_bonus += 15
            elif typ == "нефтяная вышка":
                resource_bonus["нефть"] += 10
            elif typ == "ферма":
                resource_bonus["продовольствие"] += 15
            elif typ == "железный рудник":
                resource_bonus["железо"] += 8
                bonus_income += 10
            elif typ == "угольная шахта":
                resource_bonus["уголь"] += 10
                bonus_income += 10
            elif typ == "лесопилка":
                resource_bonus["дерево"] += 12
                bonus_income += 5
            elif typ == "урановая шахта":
                resource_bonus["уран"] += 3
                bonus_income += 20
            elif typ == "золотой рудник":
                resource_bonus["золото"] += 5
                bonus_income += 30

        colony_bonus = self.game.colony_income
        trade_bonus = sum(10 for v in self.game.trade_agreements.values() if v)
        tech_bonuses = self.game.get_tech_bonuses()
        income_add = tech_bonuses.get("income_bonus", 0)
        prod_bonus = tech_bonuses.get("prod_bonus", 0)

        total_income = base_income + bonus_income + colony_bonus + income_add
        total_income = int(total_income * (1 + (percent_bonus + trade_bonus + prod_bonus) / 100))
        total_income -= self.game.unit_maintenance

        if self.game.stability < 30:
            total_income = int(total_income * (0.5 + self.game.stability / 60))
        elif self.game.stability > 80:
            total_income = int(total_income * 1.1)

        self.game.player_income = max(0, total_income)

        # Добавляем ресурсы от зданий
        for res, amount in resource_bonus.items():
            self.game.player_resources[res] = self.game.player_resources.get(res, 0) + amount

        # Ресурсы от регионов игрока
        for region in self.game.regions:
            dev = region.get("development", 1.0)
            for res, amount in region.get("resources", {}).items():
                self.game.player_resources[res] = self.game.player_resources.get(res, 0) + int(amount * dev)

        # Влияние развития регионов на стабильность
        if self.game.regions:
            avg_dev = sum(r["development"] for r in self.game.regions) / len(self.game.regions)
            stability_mod = int((avg_dev - 1.0) * 10)
            self.game.stability = clamp(self.game.stability + stability_mod, 0, 100)
            poor_regions = sum(1 for r in self.game.regions if r["development"] < 0.5)
            if poor_regions > 0:
                self.game.stability = max(0, self.game.stability - poor_regions * 2)

    # ---------- КРЕДИТЫ ----------
    def apply_debt_interest(self):
        total_interest = 0
        if self.game.world_bank_debt > 0:
            interest = int(self.game.world_bank_debt * self.game.world_bank_interest)
            total_interest += interest
            self.game.world_bank_debt += interest
            print(f"🏦 Всемирный банк: начислены проценты {interest}💰, долг теперь {self.game.world_bank_debt}")

        for country, amount in list(self.game.debt_to_countries.items()):
            if amount > 0:
                interest = int(amount * self.game.country_interest)
                total_interest += interest
                self.game.debt_to_countries[country] += interest
                print(f"📜 Долг {country}: начислены проценты {interest}💰, долг теперь {self.game.debt_to_countries[country]}")

        if total_interest > 0:
            if self.game.player_income >= total_interest:
                self.game.player_income -= total_interest
            else:
                deficit = total_interest - self.game.player_income
                self.game.player_income = 0
                self.game.world_bank_debt += deficit
                print(f"⚠️ Доход не покрыл проценты! Долг Всемирному банку увеличен на {deficit}💰")

    def take_world_bank_loan(self):
        print("\n--- КРЕДИТ ВСЕМИРНОГО БАНКА ---")
        print("Максимальная сумма: 5000💰")
        try:
            amount = int(safe_input("Сумма кредита (0 для отмены): ", default="0"))
        except:
            amount = 0
        if amount <= 0:
            return
        if amount > 5000:
            print("❌ Слишком большая сумма!")
            return
        self.game.world_bank_debt += amount
        self.game.player_gold += amount
        print(f"✅ Кредит на {amount}💰 получен. Долг теперь {self.game.world_bank_debt}💰")

    def repay_world_bank_loan(self):
        if self.game.world_bank_debt <= 0:
            print("❌ У вас нет долга перед Всемирным банком.")
            return
        print(f"Текущий долг: {self.game.world_bank_debt}💰")
        try:
            amount = int(safe_input("Сколько погасить? (0 для отмены): ", default="0"))
        except:
            amount = 0
        if amount <= 0:
            return
        if amount > self.game.player_gold:
            print("❌ Недостаточно золота!")
            return
        if amount > self.game.world_bank_debt:
            amount = self.game.world_bank_debt
        self.game.player_gold -= amount
        self.game.world_bank_debt -= amount
        print(f"✅ Погашено {amount}💰. Остаток долга: {self.game.world_bank_debt}💰")

    def take_country_loan(self, country):
        if country not in self.game.diplomacy:
            return
        if self.game.diplomacy[country]["relations"] < 40:
            print("❌ Отношения слишком плохие для кредита (нужно > 40).")
            return
        if self.game.diplomacy[country]["status"] == "Война":
            print("❌ Вы воюете – кредит невозможен.")
            return
        print(f"\n--- КРЕДИТ ОТ {country} ---")
        max_loan = 1000 + self.game.diplomacy[country]["relations"] * 10
        print(f"Максимальная сумма: {max_loan}💰")
        try:
            amount = int(safe_input("Сумма кредита (0 для отмены): ", default="0"))
        except:
            amount = 0
        if amount <= 0:
            return
        if amount > max_loan:
            print("❌ Слишком большая сумма!")
            return
        self.game.debt_to_countries[country] = self.game.debt_to_countries.get(country, 0) + amount
        self.game.player_gold += amount
        self.game.diplomacy[country]["relations"] = min(100, self.game.diplomacy[country]["relations"] + 5)
        print(f"✅ Кредит на {amount}💰 получен от {country}. Долг теперь {self.game.debt_to_countries[country]}💰")

    def repay_country_loan(self, country):
        if country not in self.game.debt_to_countries or self.game.debt_to_countries[country] <= 0:
            print(f"❌ У вас нет долга перед {country}.")
            return
        debt = self.game.debt_to_countries[country]
        print(f"Текущий долг перед {country}: {debt}💰")
        try:
            amount = int(safe_input("Сколько погасить? (0 для отмены): ", default="0"))
        except:
            amount = 0
        if amount <= 0:
            return
        if amount > self.game.player_gold:
            print("❌ Недостаточно золота!")
            return
        if amount > debt:
            amount = debt
        self.game.player_gold -= amount
        self.game.debt_to_countries[country] -= amount
        if self.game.debt_to_countries[country] == 0:
            del self.game.debt_to_countries[country]
        self.game.diplomacy[country]["relations"] = min(100, self.game.diplomacy[country]["relations"] + 10)
        print(f"✅ Погашено {amount}💰 перед {country}.")

    # ---------- СТРОИТЕЛЬСТВО (ГРАЖДАНСКОЕ) ----------
    def build_menu(self):
        while True:
            print("\n--- СТРОИТЕЛЬСТВО (ГРАЖДАНСКИЕ ОБЪЕКТЫ) ---")
            print("1. Шахта (+15 доходу, +5 стали/ход, +3 железа/ход) – {}💰".format(self.get_current_price("шахта")))
            print("2. Завод (+25 доходу, +10 стали/ход) – {}💰".format(self.get_current_price("завод")))
            print("3. Банк (+15% доходу) – {}💰".format(self.get_current_price("банк")))
            print("4. Нефтяная вышка (+10 нефти/ход) – {}💰".format(self.get_current_price("нефтяная вышка")))
            print("5. Ферма (+15 продовольствия/ход) – {}💰".format(self.get_current_price("ферма")))
            print("6. Железный рудник (+8 железа/ход, +10 доходу) – {}💰".format(self.get_current_price("железный рудник")))
            print("7. Угольная шахта (+10 угля/ход, +10 доходу) – {}💰".format(self.get_current_price("угольная шахта")))
            print("8. Лесопилка (+12 дерева/ход, +5 доходу) – {}💰".format(self.get_current_price("лесопилка")))
            print("9. Урановая шахта (+3 урана/ход, +20 доходу) – {}💰".format(self.get_current_price("урановая шахта")))
            print("10. Золотой рудник (+5 золота/ход, +30 доходу) – {}💰".format(self.get_current_price("золотой рудник")))
            print("11. Назад")
            choice = safe_input("Выбор: ", valid_options=["1","2","3","4","5","6","7","8","9","10","11"], default="11")
            if choice == "11":
                break
            
            types = {
                "1": "шахта", "2": "завод", "3": "банк", "4": "нефтяная вышка",
                "5": "ферма", "6": "железный рудник", "7": "угольная шахта",
                "8": "лесопилка", "9": "урановая шахта", "10": "золотой рудник"
            }
            names = {
                "1": "Шахта", "2": "Завод", "3": "Банк", "4": "Нефтяная вышка",
                "5": "Ферма", "6": "Железный рудник", "7": "Угольная шахта",
                "8": "Лесопилка", "9": "Урановая шахта", "10": "Золотой рудник"
            }

            try:
                qty_input = safe_input("Сколько построить? (Макс 10): ", default="1")
                qty = int(qty_input)
                if qty < 1: qty = 1
                if qty > 10: qty = 10
            except:
                qty = 1

            cost = self.get_current_price(types[choice])
            total_cost = cost * qty

            if self.game.player_gold >= total_cost:
                self.game.player_gold -= total_cost
                for _ in range(qty):
                    self.game.buildings.append({"type": types[choice], "name": names[choice]})
                self.game.stats["buildings_constructed"] += qty
                print(f"✅ Построено {qty} шт. {names[choice]} за {total_cost}💰!")
            else:
                print(f"❌ Недостаточно золота! Нужно {total_cost}💰, у вас {self.game.player_gold}💰")

    # ---------- КОЛОНИЗАЦИЯ ----------
    def colonize_menu(self):
        while True:
            print("\n--- КОЛОНИАЛЬНАЯ ЭКСПЕДИЦИЯ ---")
            regions = [
                {"name": "Африка (Конго)", "cost": 800, "army_required": 20, "income": 40, "resources": {"нефть": 10, "сталь": 5, "железо": 6, "уголь": 4, "дерево": 8, "уран": 1, "золото": 3}},
                {"name": "Индия", "cost": 600, "army_required": 15, "income": 30, "resources": {"продовольствие": 20, "дерево": 10, "железо": 4, "уголь": 5}},
                {"name": "Индокитай", "cost": 500, "army_required": 12, "income": 20, "resources": {"продовольствие": 15, "дерево": 12, "железо": 3}},
                {"name": "Ближний Восток", "cost": 700, "army_required": 18, "income": 35, "resources": {"нефть": 20, "уголь": 6, "золото": 2}},
                {"name": "Южная Америка", "cost": 900, "army_required": 25, "income": 50, "resources": {"сталь": 15, "продовольствие": 10, "дерево": 14, "железо": 8, "золото": 4}}
            ]
            available = [r for r in regions if r["name"] not in self.game.colonies]
            if not available:
                print("Все регионы уже колонизированы!")
                break
            for idx, r in enumerate(available, 1):
                print(f"{idx}. {r['name']} | Стоимость: {r['cost']}💰 | Требуется армии: {r['army_required']} | Доход: +{r['income']}")
            print(f"{len(available)+1}. Назад")
            ch = safe_input("Выберите регион: ")
            try:
                idx = int(ch) - 1
                if idx == len(available):
                    break
                region = available[idx]
            except:
                print("❌ Неверный ввод.")
                continue
            if self.game.player_gold < region["cost"]:
                print("❌ Недостаточно золота!")
                continue
            if self.game.total_army_power < region["army_required"]:
                print("❌ Недостаточно армии (сила) для экспедиции!")
                continue
            success_chance = min(100, 50 + (self.game.total_army_power - region["army_required"]) / region["army_required"] * 50)
            if random.random() * 100 < success_chance:
                self.game.player_gold -= region["cost"]
                self.game.colonies.append(region["name"])
                self.game.colony_income += region["income"]
                for res, amount in region["resources"].items():
                    self.game.player_resources[res] = self.game.player_resources.get(res, 0) + amount
                self.game.stats["colonies_established"] += 1
                print(f"✅ Колония {region['name']} успешно основана!")
            else:
                print(f"❌ Экспедиция провалилась. Потеряно {region['cost']//2} золота и часть армии.")
                self.game.player_gold = max(0, self.game.player_gold - region["cost"]//2)
                self.game.units["пехота"] = max(0, self.game.units["пехота"] - 5)

    # ---------- ЯДЕРНАЯ ПРОГРАММА (вынесена сюда из game.py) ----------
    def nuclear_menu(self):
        while True:
            if not self.game.nuclear_researched:
                print("❌ Ядерная физика не исследована.")
                break
            print("\n☢️ ЯДЕРНАЯ ПРОГРАММА")
            print(f"Бомб: {self.game.nuclear_bombs}")
            print("1. Построить ядерную бомбу (требует: 1000💰, 20 стали, 10 нефти)")
            print("2. Применить бомбу против врага (если есть бомба и война)")
            print("3. Назад")
            ch = safe_input("Выбор: ", valid_options=["1","2","3"], default="3")
            if ch == "3":
                break
            if ch == "1":
                if (self.game.player_gold >= 1000 and
                    self.game.player_resources.get("сталь", 0) >= 20 and
                    self.game.player_resources.get("нефть", 0) >= 10):
                    self.game.player_gold -= 1000
                    self.game.player_resources["сталь"] -= 20
                    self.game.player_resources["нефть"] -= 10
                    self.game.nuclear_bombs += 1
                    self.game.stats["nuclear_bombs_built"] += 1
                    print("💣 Бомба построена!")
                else:
                    print("❌ Недостаточно ресурсов или золота.")
            elif ch == "2":
                if self.game.nuclear_bombs <= 0:
                    print("❌ Нет бомб.")
                    continue
                enemies = [c for c in self.game.ai_countries if self.game.diplomacy[c]["status"] == "Война"]
                if not enemies:
                    print("❌ Вы не воюете ни с кем.")
                    continue
                print("Выберите цель:")
                for idx, e in enumerate(enemies, 1):
                    print(f"{idx}. {e}")
                print(f"{len(enemies)+1}. Назад")
                tgt = safe_input("Номер: ")
                try:
                    idx = int(tgt) - 1
                    if idx == len(enemies):
                        continue
                    target = enemies[idx]
                except:
                    print("❌ Неверно.")
                    continue
                self.game.nuclear_bombs -= 1
                print(f"💥 ЯДЕРНЫЙ УДАР по {target}!")
                for data in self.game.countries_data.values():
                    if data["name"] == target:
                        data["army"] = max(0, data["army"] - 80)
                        break
                for c in self.game.ai_countries:
                    if c != target:
                        self.game.diplomacy[c]["relations"] = max(-100, self.game.diplomacy[c]["relations"] - 50)
                        if self.game.diplomacy[c]["status"] != "Война":
                            self.game.diplomacy[c]["status"] = "Нейтралитет"
                self.game.stability = max(0, self.game.stability - 30)
                print("🌍 Мир осудил вас! Отношения ухудшились, стабильность упала.")