import random
import pickle
import os
import sys
import json
from collections import defaultdict

from utils import get_date_str, safe_input, clamp
import config
import logger as logmod

# Глобальный логгер
logger = logmod.Logger(config.LOG_FILE, config.LOG_TO_FILE)

from managers.economy_manager import EconomyManager
from managers.military_manager import MilitaryManager
from managers.diplomacy_manager import DiplomacyManager
from managers.tech_manager import TechManager
from managers.region_manager import RegionManager
from managers.event_manager import EventManager
from managers.ui_manager import UIManager

class GlobalStrategyGame:
    def __init__(self):
        # Загружаем страны из JSON
        with open("data/countries.json", "r", encoding="utf-8") as f:
            self.countries_data = json.load(f)
        # Корректируем блоки (как было в старом коде)
        self.countries_data["6"]["bloc"] = "Антанта"
        self.countries_data["8"]["bloc"] = "Союзники"

        self.player_name = ""
        self.player_gold = 0
        self.player_income = 0
        self.player_bloc = ""
        self.player_sea = False
        self.player_resources = {"нефть": 0, "сталь": 0, "продовольствие": 0, "железо": 0, "уголь": 0, "дерево": 0, "уран": 0, "золото": 0}
        self.stability = 70
        self.buildings = []
        self.units = {
            "пехота": 0,
            "танки": 0,
            "истребители": 0,
            "ракеты": 0,
            "корабли": 0,
            "подлодки": 0,
            "авианосцы": 0
        }
        self.unit_maintenance = 0
        self.total_army_power = 0

        self.ai_countries = []
        self.diplomacy = {}
        self.trade_agreements = {}

        self.techs = {}
        self.active_research = None
        self.research_progress = 0

        self.colonies = []
        self.colony_income = 0

        self.personalities = []
        self.available_personalities = []

        self.nuclear_bombs = 0
        self.nuclear_researched = False

        self.stats = {
            "wars_declared": 0,
            "buildings_constructed": 0,
            "techs_researched": 0,
            "colonies_established": 0,
            "nuclear_bombs_built": 0,
            "battles_won": 0,
            "battles_lost": 0,
            "regions_captured": 0,
            "regions_sold": 0,
            "regions_bought": 0
        }
        self.achievements = []

        self.neutral_countries = {
            "Испания": {"influence": 0, "status": "нейтральная"},
            "Швеция": {"influence": 0, "status": "нейтральная"},
            "Швейцария": {"influence": 0, "status": "нейтральная"},
            "Турция": {"influence": 0, "status": "нейтральная"},
            "Япония": {"influence": 0, "status": "нейтральная"},
            "Норвегия": {"influence": 0, "status": "нейтральная"},
            "Дания": {"influence": 0, "status": "нейтральная"},
            "Греция": {"influence": 0, "status": "нейтральная"},
            "Болгария": {"influence": 0, "status": "нейтральная"},
            "Сербия": {"influence": 0, "status": "нейтральная"},
            "Румыния": {"influence": 0, "status": "нейтральная"},
            "Черногория": {"influence": 0, "status": "нейтральная"},
            "Португалия": {"influence": 0, "status": "нейтральная"},
            "Бельгия": {"influence": 0, "status": "нейтральная"},
            "Нидерланды": {"influence": 0, "status": "нейтральная"}
        }

        self.map_regions = {
            "Европа": ["Российская Империя", "Германская Империя", "Британская Империя", "Французская Республика", "Австро-Венгрия", "Королевство Италия", "Испания", "Португалия", "Бельгия", "Нидерланды", "Швейцария", "Швеция", "Норвегия", "Дания", "Греция", "Болгария", "Сербия", "Румыния", "Черногория"],
            "Азия": ["Османская Империя", "Япония"],
            "Америка": ["США"]
        }

        self.turn = 0
        self.max_turns = config.MAX_TURNS
        self.historical_events_triggered = set()
        self.game_over = False
        self.event_flags = {}

        self.world_bank_debt = 0
        self.world_bank_interest = 0.05
        self.debt_to_countries = {}
        self.country_interest = 0.03

        self.history_gold = []
        self.history_army = []
        self.history_stability = []

        self.naval_blockades = {}
        self.fortifications = {"траншеи": 0, "бункеры": 0, "линии_мажино": 0}
        self.unit_exp = {"пехота": 0, "танки": 0, "истребители": 0, "ракеты": 0, "корабли": 0, "подлодки": 0, "авианосцы": 0}
        self.market_prices = {"нефть": 10, "сталь": 8, "продовольствие": 5, "железо": 7, "уголь": 6, "дерево": 4, "уран": 20, "золото": 30}
        self.breakthrough_conveyor = False
        self.breakthrough_carrier = False

        self.regions = []

        # Создаём менеджеры
        self.economy = EconomyManager(self)
        self.military = MilitaryManager(self)
        self.diplomacy_manager = DiplomacyManager(self)
        self.tech = TechManager(self)
        self.region_manager = RegionManager(self)
        self.event_manager = EventManager(self)
        self.ui = UIManager(self)
        self.military.init_military()

        logger.log("Игра инициализирована", "INFO")

    def get_current_price(self, building_type):
        return self.economy.get_current_price(building_type)

    def recalc_army_power(self):
        self.military.recalc_army_power()

    def get_tech_bonuses(self):
        return self.tech.get_tech_bonuses()

    def save_game(self, filename="savegame.pkl"):
        try:
            data = self.__dict__.copy()
            for key in ['economy', 'military', 'diplomacy_manager', 'tech', 'region_manager', 'event_manager', 'ui']:
                if key in data:
                    del data[key]
            with open(filename, "wb") as f:
                pickle.dump(data, f)
            logger.log(f"Игра сохранена в {filename}", "INFO")
            print("✅ Игра сохранена.")
        except Exception as e:
            logger.log(f"Ошибка сохранения: {e}", "ERROR")
            print(f"❌ Ошибка сохранения: {e}")

    def load_game(self, filename="savegame.pkl"):
        try:
            if not os.path.exists(filename):
                print("❌ Файл сохранения не найден.")
                return False
            with open(filename, "rb") as f:
                data = pickle.load(f)
            self.__dict__.update(data)
            self.economy = EconomyManager(self)
            self.military = MilitaryManager(self)
            self.diplomacy_manager = DiplomacyManager(self)
            self.tech = TechManager(self)
            self.region_manager = RegionManager(self)
            self.event_manager = EventManager(self)
            self.ui = UIManager(self)
            logger.log(f"Игра загружена из {filename}", "INFO")
            print("✅ Игра загружена.")
            return True
        except Exception as e:
            logger.log(f"Ошибка загрузки: {e}", "ERROR")
            print(f"❌ Ошибка загрузки: {e}")
            return False

    def main_menu(self):
        while True:
            print("\n" + "=" * 60)
            print("   GLOBAL STRATEGY: HISTORICAL CHRONICLES (1900-1950)   ")
            print("=" * 60)
            print("1. Начать новую игру")
            print("2. Загрузить сохранённую игру")
            print("3. Выход")
            choice = safe_input("Выберите действие: ", valid_options=["1","2","3"], default="1")
            if choice == "1":
                self.new_game()
                break
            elif choice == "2":
                if self.load_game():
                    self.run()
                    break
                else:
                    print("Не удалось загрузить игру. Попробуйте снова.")
            elif choice == "3":
                print("До свидания!")
                sys.exit()

    def new_game(self):
        self.__init__()
        self.setup()
        self.run()

    def setup(self):
        print("\n" + "=" * 60)
        print("   GLOBAL STRATEGY: HISTORICAL CHRONICLES (1900-1950)   ")
        print("=" * 60)

        print("\nВыберите вашу страну:")
        for key, data in self.countries_data.items():
            print(f"{key}. {data['name']} — {data['desc']}")

        choice = safe_input("Введите номер страны: ", valid_options=list(self.countries_data.keys()), default="1")
        chosen = self.countries_data[choice]
        self.player_name = chosen["name"]
        self.player_gold = chosen["gold"]
        self.player_income = chosen["income"]
        self.player_bloc = chosen["bloc"]
        self.player_sea = chosen["sea"]
        self.player_resources = chosen["resources"].copy()
        self.units["пехота"] = chosen["army"]
        self.stability = 70

        self.ai_countries = [data["name"] for data in self.countries_data.values() if data["name"] != self.player_name]
        self.diplomacy = {c: {"relations": 0, "status": "Нейтралитет", "trade": False} for c in self.ai_countries}
        self.trade_agreements = {}

        self.tech.init_techs()  # загружает из JSON

        for key, data in self.countries_data.items():
            data["regions"] = self.region_manager.get_regions_for_country(data["name"])

        self.regions = self.region_manager.get_regions_for_country(self.player_name)

        logger.log(f"Игра начата: {self.player_name}, сложность {config.DIFFICULTY}", "INFO")
        print(f"\n✅ Вы возглавили государство: {self.player_name}!")
        print("📅 Игра завершится в декабре 1950 года. История творится вашими руками!")
        input("\nНажмите Enter, чтобы начать...")

    def economy_menu(self):
        while True:
            print("\n--- ГОСУДАРСТВЕННОЕ УПРАВЛЕНИЕ ---")
            print(f"💰 Золото: {self.player_gold}, доход: +{self.player_income}, стабильность: {self.stability}%")
            print(f"🏗️ Построек: {len(self.buildings)}")
            print(f"🏦 Долг Всемирному банку: {self.world_bank_debt}💰")
            if self.debt_to_countries:
                print("📜 Долги странам:")
                for c, amt in self.debt_to_countries.items():
                    print(f"   {c}: {amt}💰")
            print("\n1. Построить здание")
            print("2. Пропаганда (+10 стабильности, -100💰)")
            print("3. Колониальная экспедиция")
            print("4. ☢️ Ядерная программа")
            print("5. 💰 Взять кредит во Всемирном банке")
            print("6. 💸 Погасить долг Всемирному банку")
            print("7. 🧑‍🏫 Наём исторических личностей")
            print("8. 📊 Торговля ресурсами")
            print("9. 🏙️ Управление регионами")
            print("10. Назад")
            choice = safe_input("Действие: ", valid_options=["1","2","3","4","5","6","7","8","9","10"], default="10")
            if choice == "10":
                break
            elif choice == "1":
                self.economy.build_menu()
            elif choice == "2":
                if self.player_gold >= 100:
                    self.player_gold -= 100
                    self.stability = min(100, self.stability + 10)
                    logger.log("Проведена пропаганда (+10 стабильности)", "INFO")
                    print("📢 Пропаганда проведена, стабильность повышена.")
                else:
                    print("❌ Недостаточно золота!")
            elif choice == "3":
                self.economy.colonize_menu()
            elif choice == "4":
                self.economy.nuclear_menu()
            elif choice == "5":
                self.economy.take_world_bank_loan()
            elif choice == "6":
                self.economy.repay_world_bank_loan()
            elif choice == "7":
                self.hire_personality_menu()
            elif choice == "8":
                self.diplomacy_manager.trade_resources_menu()
            elif choice == "9":
                self.region_manager.regions_menu()

    def update_available_personalities(self, year):
        all_persons = [
            {"name": "Жуков", "year": 1941, "bonus": "general", "effect": 20, "cost": 300},
            {"name": "Черчилль", "year": 1940, "bonus": "politician", "effect": 15, "cost": 400},
            {"name": "Гитлер", "year": 1933, "bonus": "dictator", "effect": 10, "cost": 200},
            {"name": "Сталин", "year": 1924, "bonus": "dictator", "effect": 10, "cost": 200},
            {"name": "Кейнс", "year": 1936, "bonus": "economist", "effect": 25, "cost": 350},
            {"name": "Тесла", "year": 1900, "bonus": "scientist", "effect": 20, "cost": 500}
        ]
        hired_names = [p["name"] for p in self.personalities]
        available_names = [p["name"] for p in self.available_personalities]

        for p in all_persons:
            if p["year"] == year and p["name"] not in hired_names and p["name"] not in available_names:
                if p["name"] in ["Гитлер", "Сталин"] and self.player_bloc not in ["Ось", "Центральные державы"]:
                    continue
                self.available_personalities.append(p)
                print(f"📜 Стала доступна личность: {p['name']} (бонус: {p['bonus']} +{p['effect']})")

    def hire_personality_menu(self):
        if not self.available_personalities:
            print("❌ В данный момент нет доступных личностей.")
            return
        print("\n--- НАЁМ ИСТОРИЧЕСКИХ ЛИЧНОСТЕЙ ---")
        for idx, p in enumerate(self.available_personalities, 1):
            print(f"{idx}. {p['name']} | Бонус: {p['bonus']} +{p['effect']} | Стоимость: {p['cost']}💰")
        print(f"{len(self.available_personalities)+1}. Назад")
        choice = safe_input("Выберите личность: ")
        try:
            idx = int(choice) - 1
            if idx == len(self.available_personalities):
                return
            person = self.available_personalities[idx]
        except:
            print("❌ Неверный выбор.")
            return
        if self.player_gold < person["cost"]:
            print("❌ Недостаточно золота!")
            return
        self.player_gold -= person["cost"]
        self.personalities.append({"name": person["name"], "bonus": person["bonus"], "effect": person["effect"]})
        self.available_personalities.remove(person)
        print(f"✅ {person['name']} нанят!")
        logger.log(f"Нанята личность: {person['name']}", "INFO")
        if person["bonus"] == "general":
            self.total_army_power = int(self.total_army_power * (1 + person["effect"]/100))
        elif person["bonus"] == "economist":
            self.player_income += person["effect"]
        elif person["bonus"] == "scientist":
            if self.active_research:
                self.techs[self.active_research]["time"] = max(1, self.techs[self.active_research]["time"] - 2)
                print("🔬 Скорость исследований увеличена!")

    def army_menu(self):
        while True:
            print("\n--- ВОЕННОЕ ДЕЛО ---")
            print("1. Купить юниты")
            print("2. Управление укреплениями (траншеи, бункеры, линии Мажино)")
            print("3. Военные базы / заводы (построить)")
            print("4. Назад")
            choice = safe_input("Выбор: ", valid_options=["1","2","3","4"], default="4")
            if choice == "4":
                break
            elif choice == "1":
                self.military.buy_units_menu()
            elif choice == "2":
                self.military.fortifications_menu()
            elif choice == "3":
                self.military.military_infrastructure_menu()

    def diplomacy_menu(self):
        self.diplomacy_manager.diplomacy_menu()

    def tech_menu(self):
        self.tech.tech_menu()

    def advance_research(self):
        self.tech.advance_research()

    def map_menu(self):
        while True:
            print("\n--- ТЕКСТОВАЯ КАРТА МИРА ---")
            for region, countries in self.map_regions.items():
                print(f"🌍 {region}:")
                for c in countries:
                    if c == self.player_name:
                        marker = "👉"
                    else:
                        marker = "  "
                    col = " (колония)" if c in self.colonies else ""
                    print(f"   {marker} {c}{col}")
            print("\nВаши колонии:", ", ".join(self.colonies) if self.colonies else "нет")
            print("Доход от колоний: +{}💰".format(self.colony_income))
            print("\n1. Назад")
            if safe_input("Введите 1 для выхода: ", valid_options=["1"], default="1") == "1":
                break

    def spy_menu(self):
        while True:
            print("\n🕵️ РАЗВЕДКА")
            targets = [c for c in self.ai_countries if self.diplomacy[c]["status"] == "Война"]
            if not targets:
                targets = list(self.ai_countries)
            for idx, e in enumerate(targets, 1):
                print(f"{idx}. {e}")
            print(f"{len(targets)+1}. Назад")
            ch = safe_input("Выберите цель: ")
            try:
                idx = int(ch) - 1
                if idx == len(targets): break
                target = targets[idx]
            except:
                continue
            
            print(f"Действия против {target}:")
            print("1. Украсть золото (500💰, шанс 70%)")
            print("2. Украсть технологию (300💰, шанс 50%)")
            print("3. Диверсия на заводе (400💰, шанс 60%)")
            print("4. Украсть ядерные чертежи (1000💰, шанс 20%)")
            act = safe_input("Выбор: ", valid_options=["1","2","3","4"], default="1")
            
            cost = [500, 300, 400, 1000][int(act)-1]
            success = [70, 50, 60, 20][int(act)-1]
            if self.player_gold < cost:
                print("❌ Недостаточно золота!")
                continue
            
            self.player_gold -= cost
            if random.random() * 100 < success:
                if act == "1":
                    gain = random.randint(200, 600)
                    self.player_gold += gain
                    print(f"✅ Золото украдено! Вы получили {gain}💰.")
                    logger.log(f"Украдено золото у {target}: {gain}", "INFO")
                elif act == "2":
                    available_techs = [t for t, d in self.techs.items() if not d["researched"]]
                    if available_techs:
                        stolen = random.choice(available_techs)
                        self.techs[stolen]["researched"] = True
                        print(f"✅ Чертежи украдены! Вы получили технологию {stolen}!")
                        logger.log(f"Украдена технология {stolen} у {target}", "INFO")
                    else:
                        print("✅ Технологий больше нет.")
                elif act == "3":
                    self.diplomacy[target]["relations"] -= 10
                    for data in self.countries_data.values():
                        if data["name"] == target:
                            data["income"] = max(20, data["income"] - 20)
                            break
                    print(f"✅ Диверсия удалась! Экономика врага пострадала.")
                    logger.log(f"Диверсия против {target}", "INFO")
                else:
                    if "Ядерная физика" in self.techs and self.techs["Ядерная физика"]["researched"]:
                        self.nuclear_bombs += 1
                        print("☢️ Вы украли ядерные чертежи и построили бомбу!")
                        logger.log("Украдены ядерные чертежи", "WARNING")
                    else:
                        print("❌ У врага еще нет ядерного оружия.")
            else:
                self.diplomacy[target]["relations"] -= 40
                self.stability = max(0, self.stability - 5)
                print("❌ Шпион пойман! Отношения резко упали, стабильность пострадала.")
                logger.log(f"Шпион пойман в {target}", "WARNING")

    def league_nations_menu(self):
        year = get_date_str(self.turn)[1]
        if year < 1920:
            print("Лига Наций еще не создана (1920 год).")
            return
        print("\n🌐 ЛИГА НАЦИЙ / ООН")
        print("1. Предложить санкции против врага (500💰, шанс 50%)")
        print("2. Подкупить голоса (снять санкции с себя, 800💰)")
        print("3. Пропаганда (улучшить репутацию) - 300💰")
        print("4. Назад")
        ch = safe_input("Выбор: ", valid_options=["1","2","3","4"], default="4")
        
        if ch == "1":
            enemies = [c for c in self.ai_countries if self.diplomacy[c]["status"] == "Война"]
            if not enemies:
                print("Нет врагов.")
                return
            print("Выберите врага:")
            for idx, e in enumerate(enemies, 1): print(f"{idx}. {e}")
            try:
                target = enemies[int(safe_input("Номер: "))-1]
            except:
                return
            if self.player_gold >= 500:
                self.player_gold -= 500
                if random.random() < 0.5:
                    for data in self.countries_data.values():
                        if data["name"] == target:
                            data["income"] = int(data["income"] * 0.5)
                            break
                    print(f"✅ Санкции против {target} приняты! Его доход упал на 50%.")
                    logger.log(f"Санкции против {target}", "INFO")
                else:
                    print("❌ Санкции отклонены. Деньги потрачены впустую.")
            else:
                print("❌ Недостаточно золота!")
        elif ch == "2":
            if self.player_gold >= 800:
                self.player_gold -= 800
                self.stability = min(100, self.stability + 10)
                print("✅ Голоса подкуплены, санкции сняты.")
                logger.log("Подкуплены голоса в Лиге Наций", "INFO")
            else:
                print("❌ Недостаточно золота!")
        elif ch == "3":
            if self.player_gold >= 300:
                self.player_gold -= 300
                for c in self.ai_countries:
                    self.diplomacy[c]["relations"] = min(100, self.diplomacy[c]["relations"] + 10)
                print("✅ Мировая пропаганда успешна!")
                logger.log("Проведена мировая пропаганда", "INFO")
            else:
                print("❌ Недостаточно золота!")

    def check_achievements(self):
        ach = []
        if self.stats["wars_declared"] >= 5:
            ach.append("Мировой гегемон (5+ войн)")
        if self.stats["buildings_constructed"] >= 10:
            ach.append("Индустриализатор (10+ построек)")
        if self.stats["techs_researched"] >= 8:
            ach.append("Технократ (8+ технологий)")
        if self.stats["colonies_established"] >= 3:
            ach.append("Империалист (3+ колонии)")
        if self.nuclear_bombs >= 1:
            ach.append("Ядерная держава")
        if self.total_army_power >= 200:
            ach.append("Военная мощь (сила армии >200)")
        if self.player_gold >= 10000:
            ach.append("Золотой запас (10к золота)")
        if self.stability >= 90:
            ach.append("Стабильное государство")
        for a in ach:
            if a not in self.achievements:
                self.achievements.append(a)
                print(f"🏆 Достижение разблокировано: {a}!")
                logger.log(f"Достижение: {a}", "INFO")

    def save_load_menu(self):
        print("\n--- СОХРАНЕНИЕ / ЗАГРУЗКА ---")
        print("1. Сохранить игру")
        print("2. Загрузить игру")
        print("3. Назад")
        choice = safe_input("Выбор: ", valid_options=["1","2","3"], default="3")
        if choice == "1":
            self.save_game()
        elif choice == "2":
            self.load_game()

    def update_market_prices(self):
        war_count = sum(1 for v in self.diplomacy.values() if v["status"] == "Война")
        if war_count > 0:
            self.market_prices["нефть"] = min(50, self.market_prices["нефть"] + 2)
            self.market_prices["сталь"] = min(40, self.market_prices["сталь"] + 1)
        else:
            self.market_prices["нефть"] = max(5, self.market_prices["нефть"] - 1)
            self.market_prices["сталь"] = max(5, self.market_prices["сталь"] - 1)

    def apply_naval_blockades(self):
        for enemy, active in list(self.naval_blockades.items()):
            if not active: continue
            if enemy not in self.diplomacy:
                del self.naval_blockades[enemy]
                continue
            if self.diplomacy[enemy]["status"] != "Война":
                self.naval_blockades[enemy] = False
                continue
            if self.units["корабли"] + self.units["подлодки"] <= 0:
                self.naval_blockades[enemy] = False
                print(f"💥 Ваш флот уничтожен! Блокада {enemy} провалена.")
                logger.log(f"Блокада {enemy} провалена (флот уничтожен)", "WARNING")
                continue
            print(f"🚢 Блокада {enemy}: враг теряет доход.")
            for data in self.countries_data.values():
                if data["name"] == enemy:
                    data["income"] = int(data["income"] * 0.7)
                    break
            if random.random() < 0.15:
                loss = random.randint(1, 3)
                self.units["корабли"] = max(0, self.units["корабли"] - loss)
                print(f"⚔️ Враг прорвал блокаду! Вы потеряли {loss} кораблей.")
                logger.log(f"Блокада {enemy} прорвана, потеряно {loss} кораблей", "WARNING")

    def check_scientific_breakthroughs(self):
        factories = sum(1 for b in self.buildings if b["type"] == "завод")
        if factories >= 3 and not self.breakthrough_conveyor and random.random() < 0.05:
            self.player_income += 50
            self.breakthrough_conveyor = True
            print("🔬 Научный прорыв! Ученые изобрели Конвейер (+50💰 к доходу)")
            logger.log("Научный прорыв: Конвейер", "INFO")
        if self.units["корабли"] >= 5 and not self.breakthrough_carrier and random.random() < 0.03:
            self.units["авианосцы"] += 3
            self.breakthrough_carrier = True
            print("✈️ Научный прорыв! Созданы Авианосцы! (+3 авианосца)")
            logger.log("Научный прорыв: Авианосцы", "INFO")

    def ai_turn(self):
        for country in self.ai_countries:
            country_data = None
            for k, d in self.countries_data.items():
                if d["name"] == country:
                    country_data = d
                    break
            if not country_data:
                continue

            ai_gold = country_data["gold"]
            ai_income = country_data["income"]
            ai_army = country_data.get("army", 50)
            ai_res = country_data.get("resources", {}).copy()

            r = random.random()
            if r < 0.10:
                if ai_gold >= 400:
                    ai_gold -= 400
                    ai_income += 15
            elif r < 0.18:
                if ai_gold >= 200 and ai_res.get("сталь", 0) >= 5:
                    ai_gold -= 200
                    ai_res["сталь"] -= 5
                    ai_army += 5
            elif r < 0.22:
                if self.diplomacy[country]["relations"] < 0:
                    self.diplomacy[country]["relations"] = min(100, self.diplomacy[country]["relations"] + 10)
            elif r < 0.26:
                if self.diplomacy[country]["relations"] > 30 and not self.diplomacy[country].get("trade", False):
                    self.diplomacy[country]["trade"] = True
                    self.trade_agreements[country] = True
                    print(f"📈 {country} предлагает торговлю (принято).")
                    logger.log(f"{country} заключил торговое соглашение", "INFO")

            if self.diplomacy[country]["status"] == "Война" and self.total_army_power > 0:
                if random.random() < 0.05:
                    loss = random.randint(1, 5)
                    self.units["пехота"] = max(0, self.units["пехота"] - loss)
                    print(f"⚔️ {country} атакует ваши позиции, потеряно {loss} пехоты.")
                    logger.log(f"{country} атаковал, потеряно {loss} пехоты", "WARNING")

            country_data["gold"] = ai_gold
            country_data["income"] = ai_income
            country_data["army"] = ai_army
            country_data["resources"] = ai_res

        self.diplomacy_manager.ai_turn_extra()

    def run(self):
        while self.turn < self.max_turns and not self.game_over:
            date_str, year, month = get_date_str(self.turn)
            self.event_manager.handle_historical_events()
            if self.game_over:
                break

            self.economy.apply_building_bonuses()
            self.recalc_army_power()
            self.update_available_personalities(year)
            self.update_market_prices()
            self.apply_naval_blockades()
            self.check_scientific_breakthroughs()

            print("\n" + "=" * 50)
            print(f" СВОДКА: {date_str} (Ход {self.turn + 1}/{self.max_turns})")
            print(f" Страна: {self.player_name} | Бюджет: {self.player_gold} 💰 | Доход: +{self.player_income}/мес")
            print(f" Стабильность: {self.stability}% | Сила: {self.total_army_power} ⚔️ (обслуж.: {self.unit_maintenance}💰)")
            res_str = ", ".join([f"{k}: {self.player_resources.get(k,0)}" for k in ["нефть","сталь","продовольствие","железо","уголь","дерево","уран","золото"]])
            print(f" Ресурсы: {res_str}")
            region_prod = self.region_manager.calc_total_region_production()
            prod_str = ", ".join([f"{k}: +{v}" for k, v in region_prod.items() if v > 0])
            if prod_str:
                print(f" Добыча регионов: {prod_str}")
            mods = self.ui.get_active_modifiers()
            if mods:
                print(" Модификаторы: " + ", ".join(mods))
            print("=" * 50)

            while True:
                print("\nДОСТУПНЫЕ ДЕЙСТВИЯ:")
                print("1. 🏛️ Государственное управление")
                print("2. ⚔️ Военное дело")
                print("3. 🤝 Дипломатия")
                print("4. 🌍 Карта и колонии")
                print("5. 🔬 Технологии")
                print("6. ⏩ Завершить ход")
                print("7. 💾 Сохранить / загрузить")
                print("8. 🕵️ Шпионаж")
                print("9. 🌐 Лига Наций")

                action = safe_input("Выберите (1-9): ", valid_options=["1","2","3","4","5","6","7","8","9"], default="6")
                if action == "6":
                    break
                elif action == "1":
                    self.economy_menu()
                elif action == "2":
                    self.army_menu()
                elif action == "3":
                    self.diplomacy_menu()
                elif action == "4":
                    self.map_menu()
                elif action == "5":
                    self.tech_menu()
                elif action == "7":
                    self.save_load_menu()
                elif action == "8":
                    self.spy_menu()
                elif action == "9":
                    self.league_nations_menu()

            self.player_gold += self.player_income
            if self.player_gold < 0:
                self.player_gold = 0

            self.check_stability_events()
            self.ai_turn()
            self.advance_research()
            self.check_achievements()
            self.economy.apply_debt_interest()

            self.history_gold.append(self.player_gold)
            self.history_army.append(self.total_army_power)
            self.history_stability.append(self.stability)

            self.event_manager.peace_conference()

            self.turn += 1

        self.final_screen()

    def check_stability_events(self):
        if self.stability < 20 and random.random() < 0.1:
            print("💥 Восстание! Потеряно 10 пехоты и 100 золота.")
            self.units["пехота"] = max(0, self.units["пехота"] - 10)
            self.player_gold = max(0, self.player_gold - 100)
            self.stability = max(0, self.stability - 5)
            logger.log("Восстание! Потеряно 10 пехоты и 100 золота", "WARNING")
        if self.stability < 10 and self.colonies:
            lost = random.choice(self.colonies)
            self.colonies.remove(lost)
            self.colony_income -= 30
            print(f"🏴 Колония {lost} объявила независимость!")
            logger.log(f"Колония {lost} объявила независимость", "WARNING")

    def final_screen(self):
        print("\n" + "=" * 60)
        print("        ИСТОРИЯ ЗАВЕРШЕНА! ДЕКАБРЬ 1950 ГОДА.        ")
        print("=" * 60)
        print(f"\n🏁 Итоги вашего правления страной {self.player_name}:")
        print(f"💰 Итоговый бюджет: {self.player_gold}")
        print(f"📈 Итоговый доход: {self.player_income}")
        print(f"⚔️ Сила армии: {self.total_army_power}")
        print(f"🏗️ Построек: {self.stats['buildings_constructed']}")
        print(f"📚 Технологий исследовано: {self.stats['techs_researched']}")
        print(f"🌍 Колоний: {self.stats['colonies_established']}")
        print(f"☢️ Ядерных бомб: {self.stats['nuclear_bombs_built']}")
        print(f"⚔️ Побед в битвах: {self.stats['battles_won']}, поражений: {self.stats['battles_lost']}")
        print(f"🕊️ Стабильность: {self.stability}%")
        print(f"🏴 Регионов захвачено: {self.stats.get('regions_captured', 0)}")
        print(f"💰 Регионов куплено: {self.stats.get('regions_bought', 0)}")
        print(f"💰 Регионов продано: {self.stats.get('regions_sold', 0)}")
        print("\n🏆 Достижения:")
        if self.achievements:
            for a in self.achievements:
                print(f"   - {a}")
        else:
            print("   (нет)")
        print("\n📋 Статистика:")
        print(f"   Всего войн объявлено: {self.stats['wars_declared']}")
        print(f"   Активных союзников: {sum(1 for v in self.diplomacy.values() if v['status'] == 'Союз')}")
        print(f"   Активных врагов: {sum(1 for v in self.diplomacy.values() if v['status'] == 'Война')}")
        print("\nСпасибо за игру! Создавайте свою альтернативную историю заново.")
        self.ui.show_statistics_graphs()
        logger.log("Игра завершена", "INFO")
        logger.close()
        input("\nНажмите Enter для выхода...")