import random
from utils import safe_input, clamp

class MilitaryManager:
    def __init__(self, game):
        self.game = game

    def init_military(self):
        self.game.unit_stats = {
            "пехота": {"power": 1, "maint": 2, "cost_gold": 50, "resources": {"продовольствие": 2}},
            "танки": {"power": 5, "maint": 10, "cost_gold": 200, "resources": {"сталь": 5}},
            "истребители": {"power": 8, "maint": 15, "cost_gold": 300, "resources": {"нефть": 3}},
            "ракеты": {"power": 12, "maint": 20, "cost_gold": 500, "resources": {"нефть": 2, "сталь": 2}},
            "корабли": {"power": 10, "maint": 18, "cost_gold": 400, "resources": {"сталь": 5}},
            "подлодки": {"power": 9, "maint": 14, "cost_gold": 350, "resources": {"сталь": 3}},
            "авианосцы": {"power": 15, "maint": 30, "cost_gold": 800, "resources": {"сталь": 8, "нефть": 3}},
            "артиллерия": {"power": 6, "maint": 8, "cost_gold": 250, "resources": {"сталь": 4}},
            "ПВО": {"power": 4, "maint": 6, "cost_gold": 300, "resources": {"сталь": 3, "нефть": 1}},
            "транспорт": {"power": 1, "maint": 3, "cost_gold": 150, "resources": {"сталь": 2}},
            "десант": {"power": 5, "maint": 7, "cost_gold": 200, "resources": {"продовольствие": 3}}
        }
        self.game.unit_morale = {unit: 50 for unit in self.game.unit_stats.keys()}

    def recalc_army_power(self):
        power = 0
        maintenance = 0
        tech_bonuses = self.game.get_tech_bonuses()
        for unit, count in self.game.units.items():
            if count > 0:
                stats = self.game.unit_stats.get(unit)
                if not stats:
                    continue
                base_power = stats["power"]
                if unit == "пехота":
                    base_power += tech_bonuses.get("infantry_bonus", 0)
                elif unit == "танки":
                    base_power += tech_bonuses.get("tank_bonus", 0)
                elif unit == "истребители":
                    base_power += tech_bonuses.get("air_bonus", 0)
                elif unit == "ракеты":
                    base_power += tech_bonuses.get("rocket_bonus", 0)
                morale = self.game.unit_morale.get(unit, 50)
                morale_mod = 0.5 + morale / 100
                power += count * base_power * morale_mod
                maintenance += count * stats["maint"]
        art_bonus = tech_bonuses.get("artillery_bonus", 0)
        power = int(power * (1 + art_bonus / 10))
        self.game.total_army_power = power
        self.game.unit_maintenance = maintenance

    def update_morale(self, won, losses):
        for unit in self.game.units:
            if self.game.units[unit] > 0:
                if won:
                    self.game.unit_morale[unit] = min(100, self.game.unit_morale[unit] + 5)
                else:
                    self.game.unit_morale[unit] = max(0, self.game.unit_morale[unit] - 5 - losses//5)

    def buy_units_menu(self):
        while True:
            print("\n--- ЗАКУПКА ЮНИТОВ ---")
            print("1. Пехота – 50💰, 2 прод. (сила 1, обслуж. 2)")
            print("2. Танки – 200💰, 5 стали (сила 5, обслуж. 10)")
            print("3. Истребители – 300💰, 3 нефти (сила 8, обслуж. 15)")
            print("4. Ракеты – 500💰, 2 нефти, 2 стали (сила 12, обслуж. 20)")
            if self.game.player_sea:
                print("5. Корабли – 400💰, 5 стали (сила 10, обслуж. 18)")
                print("6. Подлодки – 350💰, 3 стали (сила 9, обслуж. 14)")
                print("7. Авианосцы – 800💰, 8 стали, 3 нефти (сила 15, обслуж. 30)")
            else:
                print("5-7. ❌ Нет выхода к морю – флот недоступен.")
            print("8. Назад")
            choice = safe_input("Выбор: ", valid_options=["1","2","3","4","5","6","7","8"], default="8")
            if choice == "8":
                break
            if choice in ["5","6","7"] and not self.game.player_sea:
                print("❌ У вас нет выхода к морю!")
                continue
            unit_data = {
                "1": {"name": "пехота", "cost_gold": 50, "resources": {"продовольствие": 2}},
                "2": {"name": "танки", "cost_gold": 200, "resources": {"сталь": 5}},
                "3": {"name": "истребители", "cost_gold": 300, "resources": {"нефть": 3}},
                "4": {"name": "ракеты", "cost_gold": 500, "resources": {"нефть": 2, "сталь": 2}},
                "5": {"name": "корабли", "cost_gold": 400, "resources": {"сталь": 5}},
                "6": {"name": "подлодки", "cost_gold": 350, "resources": {"сталь": 3}},
                "7": {"name": "авианосцы", "cost_gold": 800, "resources": {"сталь": 8, "нефть": 3}}
            }
            data = unit_data[choice]
            discount = 0
            for b in self.game.buildings:
                if b["type"] == "военный завод":
                    discount += 0.1
            price = int(data["cost_gold"] * (1 - min(discount, 0.5)))
            can_buy = True
            for res, amount in data["resources"].items():
                if self.game.player_resources.get(res, 0) < amount:
                    can_buy = False
                    print(f"❌ Недостаточно {res} (нужно {amount})")
                    break
            if not can_buy:
                continue
            limit = 100 + 20 * sum(1 for b in self.game.buildings if b["type"] == "военная база")
            current_total = sum(self.game.units.values())
            if current_total >= limit:
                print("❌ Достигнут лимит армии! Постройте военные базы.")
                continue
            try:
                count = int(safe_input("Сколько купить? (0 для отмены): ", default="0"))
            except:
                count = 0
            if count <= 0:
                continue
            total_cost = price * count
            for res, amount in data["resources"].items():
                if self.game.player_resources.get(res, 0) < amount * count:
                    print(f"❌ Недостаточно {res} для {count} единиц.")
                    break
            else:
                if self.game.player_gold >= total_cost:
                    self.game.player_gold -= total_cost
                    for res, amount in data["resources"].items():
                        self.game.player_resources[res] -= amount * count
                    self.game.units[data["name"]] += count
                    print(f"✅ Куплено {count} {data['name']}")
                else:
                    print("❌ Недостаточно золота!")

    def fortifications_menu(self):
        print("\n--- УКРЕПЛЕНИЯ ---")
        print(f"Траншеи: {self.game.fortifications['траншеи']} (защита +30% каждая)")
        print(f"Бункеры: {self.game.fortifications['бункеры']} (защита +50% каждая)")
        print(f"Линии Мажино: {self.game.fortifications['линии_мажино']} (защита +80% каждая)")
        print("\n1. Построить траншеи (500💰)")
        print("2. Построить бункеры (1000💰)")
        print("3. Построить линии Мажино (2000💰)")
        print("4. Назад")
        ch = safe_input("Выбор: ", valid_options=["1","2","3","4"], default="4")
        if ch == "4":
            return
        cost = 500 if ch == "1" else (1000 if ch == "2" else 2000)
        key = "траншеи" if ch == "1" else ("бункеры" if ch == "2" else "линии_мажино")
        if self.game.player_gold >= cost:
            self.game.player_gold -= cost
            self.game.fortifications[key] += 1
            print(f"✅ {key.capitalize()} построены!")
        else:
            print("❌ Недостаточно золота!")

    def military_infrastructure_menu(self):
        while True:
            print("\n--- ВОЕННАЯ ИНФРАСТРУКТУРА ---")
            print("1. Военная база (+20 лимита армии) – {}💰".format(self.game.economy.get_current_price("военная база")))
            print("2. Военный завод (-10% стоимости юнитов) – {}💰".format(self.game.economy.get_current_price("военный завод")))
            print("3. Назад")
            ch = safe_input("Выбор: ", valid_options=["1","2","3"], default="3")
            if ch == "3":
                break
            typ = "военная база" if ch == "1" else "военный завод"
            cost = self.game.economy.get_current_price(typ)
            if self.game.player_gold >= cost:
                self.game.player_gold -= cost
                self.game.buildings.append({"type": typ, "name": typ.capitalize()})
                self.game.stats["buildings_constructed"] += 1
                print(f"✅ {typ.capitalize()} построена!")
            else:
                print("❌ Недостаточно золота!")