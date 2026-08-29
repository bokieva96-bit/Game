import random
from utils import safe_input, clamp
import logger

class DiplomacyManager:
    def __init__(self, game):
        self.game = game

    def trade_resources_menu(self):
        print("\n--- МИРОВОЙ РЫНОК РЕСУРСОВ ---")
        prices = {
            "нефть": random.randint(20, 50),
            "сталь": random.randint(15, 40),
            "продовольствие": random.randint(10, 30)
        }
        print(f"Цены: Нефть={prices['нефть']}💰, Сталь={prices['сталь']}💰, Продовольствие={prices['продовольствие']}💰")
        print("1. Купить ресурс")
        print("2. Продать ресурс")
        print("3. Назад")
        ch = safe_input("Выбор: ", valid_options=["1","2","3"], default="3")
        if ch == "3":
            return
        res_name = safe_input("Какой ресурс? (нефть/сталь/продовольствие): ")
        if res_name not in prices:
            print("❌ Неверный ресурс.")
            return
        try:
            amount = int(safe_input("Количество: ", default="0"))
        except:
            amount = 0
        if amount <= 0:
            return
        cost = amount * prices[res_name]
        if ch == "1":
            if self.game.player_gold >= cost:
                self.game.player_gold -= cost
                self.game.player_resources[res_name] = self.game.player_resources.get(res_name, 0) + amount
                print(f"✅ Куплено {amount} {res_name} за {cost}💰")
                logger.log(f"Куплено {amount} {res_name} за {cost}", "INFO")
            else:
                print("❌ Недостаточно золота.")
        else:
            if self.game.player_resources.get(res_name, 0) >= amount:
                self.game.player_resources[res_name] -= amount
                self.game.player_gold += cost
                print(f"✅ Продано {amount} {res_name} за {cost}💰")
                logger.log(f"Продано {amount} {res_name} за {cost}", "INFO")
            else:
                print("❌ Недостаточно ресурса.")

    def offer_peace(self, enemy):
        if enemy not in self.game.diplomacy or self.game.diplomacy[enemy]["status"] != "Война":
            return
        print(f"\n🕊️ Мирные переговоры с {enemy}")
        print("1. Мир без условий")
        print("2. Контрибуция (требовать 50% золота врага)")
        print("3. Аннексия (забрать всё, враг исчезает)")
        print("4. Отмена")
        ch = safe_input("Ваш выбор: ", valid_options=["1","2","3","4"], default="4")
        if ch == "4":
            return
        enemy_data = None
        for k, d in self.game.countries_data.items():
            if d["name"] == enemy:
                enemy_data = d
                break
        if not enemy_data:
            return
        if ch == "1":
            self.game.diplomacy[enemy]["status"] = "Нейтралитет"
            self.game.diplomacy[enemy]["relations"] = 0
            print(f"☮️ Мир подписан с {enemy}.")
            logger.log(f"Мир с {enemy}", "INFO")
        elif ch == "2":
            gold_taken = enemy_data["gold"] // 2
            self.game.player_gold += gold_taken
            enemy_data["gold"] -= gold_taken
            self.game.diplomacy[enemy]["status"] = "Нейтралитет"
            print(f"💰 {enemy} выплачивает контрибуцию {gold_taken}💰.")
            logger.log(f"Контрибуция от {enemy}: {gold_taken}", "INFO")
        elif ch == "3":
            self.game.player_gold += enemy_data["gold"]
            for res in self.game.player_resources:
                self.game.player_resources[res] += enemy_data["resources"].get(res, 0)
            del self.game.countries_data[self.game.get_key_by_name(enemy)]
            self.game.ai_countries.remove(enemy)
            del self.game.diplomacy[enemy]
            print(f"🏴 {enemy} аннексирована!")
            logger.log(f"{enemy} аннексирована", "WARNING")

    def ai_turn_extra(self):
        for country in self.game.ai_countries:
            if country not in self.game.diplomacy:
                continue
            rel = self.game.diplomacy[country]["relations"]
            status = self.game.diplomacy[country]["status"]

            # 1. Предложение союза
            if rel > 60 and status != "Союз" and random.random() < 0.1:
                print(f"🤝 {country} предлагает военный союз!")
                self.game.diplomacy[country]["status"] = "Союз"
                logger.log(f"ИИ {country} предложил союз (принят)", "INFO")

            # 2. Угрозы
            if rel < -40 and self.game.total_army_power < self.game.get_country_army(country) and random.random() < 0.05:
                print(f"💢 {country} угрожает войной, если вы не улучшите отношения!")
                self.game.diplomacy[country]["relations"] -= 10
                logger.log(f"ИИ {country} угрожает войной", "WARNING")

            # 3. Торговля
            if rel > 30 and not self.game.diplomacy[country].get("trade", False) and random.random() < 0.15:
                print(f"📈 {country} предлагает торговое соглашение.")
                self.game.diplomacy[country]["trade"] = True
                self.game.trade_agreements[country] = True
                logger.log(f"ИИ {country} заключил торговлю", "INFO")

            # 4. Если страна воюет с игроком, может попросить мира (если слаба)
            if status == "Война" and self.game.get_country_army(country) < self.game.total_army_power * 0.5 and random.random() < 0.1:
                print(f"🕊️ {country} просит мира!")
                self.offer_peace(country)

    def diplomacy_menu(self):
        while True:
            print("\n--- ДИПЛОМАТИЧЕСКИЙ КОРПУС ---")
            ai_list = [c for c in self.game.ai_countries if c in self.game.diplomacy]
            
            for idx, c in enumerate(ai_list, 1):
                info = self.game.diplomacy[c]
                bloc = self.game.get_country_bloc(c)
                trade = "📜" if info.get("trade", False) else ""
                print(f"{idx}. {c} (блок: {bloc}) {trade} | Отн.: {info['relations']} | Статус: {info['status']}")
            print(f"{len(ai_list)+1}. Влияние на нейтральные страны")
            print(f"{len(ai_list)+2}. Торговля ресурсами")
            print(f"{len(ai_list)+3}. Купить регион у ИИ")
            print(f"{len(ai_list)+4}. Продать регион ИИ")
            print(f"{len(ai_list)+5}. Назад")

            choice = safe_input("Выберите: ")
            try:
                idx = int(choice) - 1
                if idx == len(ai_list):
                    self.neutral_influence_menu()
                    continue
                elif idx == len(ai_list)+1:
                    self.trade_resources_menu()
                    continue
                elif idx == len(ai_list)+2:
                    self.game.region_manager.buy_region_from_ai_menu()
                    continue
                elif idx == len(ai_list)+3:
                    self.game.region_manager.sell_region_to_ai_menu()
                    continue
                elif idx == len(ai_list)+4:
                    break
                target = ai_list[idx]
            except:
                print("❌ Неверный номер.")
                continue

            while True:
                if target not in self.game.diplomacy:
                    print("Эта страна больше не доступна для дипломатии.")
                    break
                
                current = self.game.diplomacy[target]
                print(f"\nДействия с {target} (отношения: {current['relations']}, статус: {current['status']}):")
                print("1. Улучшить отношения (-120 💰, +25 отношений)")
                print("2. Пакт о ненападении (требуется отношения > 25)")
                print("3. Заключить Союз (требуется отношения > 65)")
                print("4. Торговое соглашение (требуется отношения > 30, +10% доходу обеим)")
                print("5. Военная операция (если в состоянии войны)")
                print("6. Взять кредит у страны (требуется отношения > 40)")
                print("7. Погасить долг перед страной")
                print("8. Объявить войну!")
                print("9. 🚢 Ввести блокаду")
                print("10. 🚫 Ввести эмбарго")
                print("11. Назад")
                act = safe_input("Ваш выбор: ", valid_options=["1","2","3","4","5","6","7","8","9","10","11"], default="11")
                if act == "11":
                    break
                elif act == "1":
                    if self.game.player_gold >= 120:
                        self.game.player_gold -= 120
                        current["relations"] = min(100, current["relations"] + 25)
                        print("🕊️ Отношения улучшены.")
                        logger.log(f"Улучшены отношения с {target}", "INFO")
                    else:
                        print("❌ Недостаточно золота!")
                elif act == "2":
                    if current["relations"] >= 25:
                        current["status"] = "Пакт"
                        print("📜 Пакт о ненападении подписан.")
                        logger.log(f"Пакт о ненападении с {target}", "INFO")
                    else:
                        print("❌ Отношения недостаточны.")
                elif act == "3":
                    if current["relations"] >= 65:
                        current["status"] = "Союз"
                        print("👑 Военный альянс заключён!")
                        logger.log(f"Союз с {target}", "INFO")
                    else:
                        print("❌ Отношения недостаточны.")
                elif act == "4":
                    if current["relations"] >= 30:
                        if current.get("trade", False):
                            print("⚠️ Соглашение уже действует.")
                        else:
                            current["trade"] = True
                            self.game.trade_agreements[target] = True
                            print("📈 Торговое соглашение заключено! Обе стороны получают +10% к доходу.")
                            logger.log(f"Торговое соглашение с {target}", "INFO")
                    else:
                        print("❌ Отношения недостаточны.")
                elif act == "5":
                    if current["status"] == "Война":
                        self.military_operation(target)
                    else:
                        print("❌ Вы не в состоянии войны с этой страной.")
                elif act == "6":
                    self.game.economy.take_country_loan(target)
                elif act == "7":
                    self.game.economy.repay_country_loan(target)
                elif act == "8":
                    current["relations"] = -100
                    current["status"] = "Война"
                    self.game.stats["wars_declared"] += 1
                    print(f"⚔️ Война объявлена {target}!")
                    logger.log(f"ОБЪЯВЛЕНА ВОЙНА {target}", "WARNING")
                elif act == "9":
                    if self.game.units["корабли"] + self.game.units["подлодки"] <= 0:
                        print("❌ У вас нет флота для блокады!")
                    elif not self.game.get_country_sea(target):
                        print(f"❌ У {target} нет выхода к морю!")
                    else:
                        self.game.naval_blockades[target] = True
                        print(f"🚢 Введена морская блокада {target}!")
                        logger.log(f"Блокада {target}", "INFO")
                elif act == "10":
                    current["embargo"] = True
                    self.game.player_income = int(self.game.player_income * 0.9)
                    for data in self.game.countries_data.values():
                        if data["name"] == target:
                            data["income"] = int(data["income"] * 0.85)
                            break
                    print(f"🚫 Эмбарго против {target} введено! Ваш доход -10%.")
                    logger.log(f"Эмбарго против {target}", "INFO")

    def neutral_influence_menu(self):
        while True:
            print("\n--- ВЛИЯНИЕ НА НЕЙТРАЛЬНЫЕ СТРАНЫ ---")
            for name, data in self.game.neutral_countries.items():
                print(f"{name} | Влияние: {data['influence']} | Статус: {data['status']}")
            print("\n1. Улучшить влияние (-200💰, +20 влияния)")
            print("2. Угрожать (-100💰, +10 влияния, но риск конфликта)")
            print("3. Назад")
            ch = safe_input("Выбор: ", valid_options=["1","2","3"], default="3")
            if ch == "3":
                break
            print("Выберите страну:")
            nations = list(self.game.neutral_countries.keys())
            for idx, n in enumerate(nations, 1):
                print(f"{idx}. {n}")
            print(f"{len(nations)+1}. Назад")
            ctry = safe_input("Номер: ")
            try:
                idx = int(ctry) - 1
                if idx == len(nations):
                    break
                target = nations[idx]
            except:
                print("❌ Неверно.")
                continue
            if ch == "1":
                if self.game.player_gold >= 200:
                    self.game.player_gold -= 200
                    self.game.neutral_countries[target]["influence"] = min(100, self.game.neutral_countries[target]["influence"] + 20)
                    if self.game.neutral_countries[target]["influence"] > 70:
                        self.game.neutral_countries[target]["status"] = "союзник"
                        print(f"🤝 {target} стал вашим союзником!")
                        logger.log(f"{target} стал союзником", "INFO")
                    else:
                        print(f"✅ Влияние на {target} увеличено.")
                else:
                    print("❌ Недостаточно золота.")
            elif ch == "2":
                if self.game.player_gold >= 100:
                    self.game.player_gold -= 100
                    self.game.neutral_countries[target]["influence"] = min(100, self.game.neutral_countries[target]["influence"] + 10)
                    if random.random() < 0.2:
                        self.game.neutral_countries[target]["status"] = "враждебный"
                        print(f"💢 {target} воспринял угрозы в штыки и стал враждебным!")
                        logger.log(f"{target} стал враждебным", "WARNING")
                    else:
                        print(f"✅ Влияние на {target} увеличено (угрозы).")
                else:
                    print("❌ Недостаточно золота.")

    def military_operation(self, enemy):
        while True:
            print(f"\n⚔️ ВОЕННАЯ ОПЕРАЦИЯ против {enemy}")
            print("Выберите стратегию:")
            print("1. Наступление (высокий успех, большие потери)")
            print("2. Оборона (малые потери, низкий успех)")
            print("3. Блицкриг (требует танков, быстрый успех)")
            print("4. Партизанская война (истощает врага, медленно)")
            print("5. Назад")
            strategy = safe_input("Выбор (1-5): ", valid_options=["1","2","3","4","5"], default="5")
            if strategy == "5":
                break
            enemy_power = 0
            enemy_data = None
            for data in self.game.countries_data.values():
                if data["name"] == enemy:
                    enemy_power = data.get("army", 50)
                    enemy_data = data
                    break
            if not enemy_data:
                print("❌ Враг не найден.")
                break
            my_power = self.game.total_army_power

            def_bonus = (self.game.fortifications["траншеи"] * 0.3 +
                         self.game.fortifications["бункеры"] * 0.5 +
                         self.game.fortifications["линии_мажино"] * 0.8)
            if strategy == "2":
                def_bonus = def_bonus * 2

            if strategy == "1":
                success_mod = 1.2
                loss_mod = 1.5
            elif strategy == "2":
                success_mod = 0.6
                loss_mod = 0.5
            elif strategy == "3":
                if self.game.units["танки"] > 0:
                    success_mod = 1.5
                    loss_mod = 1.2
                else:
                    print("❌ Нет танков! Блицкриг невозможен.")
                    continue
            else:
                success_mod = 0.8
                loss_mod = 0.3
            base_chance = 50 + (my_power - enemy_power) * 0.5
            chance = clamp(base_chance * success_mod - def_bonus, 10, 90)
            if random.random() * 100 < chance:
                self.game.stats["battles_won"] += 1
                print(f"✅ Победа! Вы нанесли урон врагу.")
                enemy_data["army"] = max(10, enemy_data["army"] - int(20 * success_mod))
                loss = int(10 * loss_mod)
                self.game.units["пехота"] = max(0, self.game.units["пехота"] - loss//2)
                self.game.units["танки"] = max(0, self.game.units["танки"] - loss//4)
                self.game.stability = max(0, self.game.stability - 5)
                
                # Опыт
                for unit in self.game.units:
                    if self.game.units[unit] > 0:
                        self.game.unit_exp[unit] += 2
                        # Повышение уровня
                        if self.game.unit_exp[unit] >= 25 and self.game.unit_levels[unit] < 2:
                            self.game.unit_levels[unit] = 2
                            print(f"🏅 {unit.capitalize()} стала Элитой! (+20% силы)")
                        elif self.game.unit_exp[unit] >= 10 and self.game.unit_levels[unit] < 1:
                            self.game.unit_levels[unit] = 1
                            print(f"🎖 {unit.capitalize()} стала Ветеранами! (+10% силы)")

                self.game.military.update_morale(True, loss)
                logger.log(f"Победа над {enemy}", "INFO")
                if enemy_data["army"] <= 10:
                    print(f"🏳️ Армия {enemy} полностью разгромлена!")
                    print("Вы можете захватить регион врага. Хотите?")
                    print("1. Да (получить регион)")
                    print("2. Нет (просто мир)")
                    ch2 = safe_input("Выбор: ", valid_options=["1","2"], default="2")
                    if ch2 == "1":
                        self.game.region_manager.capture_region_from_enemy(enemy)
                    self.offer_peace(enemy)
                    break
                else:
                    if random.random() < 0.15:
                        print("🏴 Вы захватили стратегический регион врага!")
                        self.game.region_manager.capture_region_from_enemy(enemy)
            else:
                self.game.stats["battles_lost"] += 1
                print(f"❌ Поражение. Вы понесли потери.")
                loss = int(15 * loss_mod)
                self.game.units["пехота"] = max(0, self.game.units["пехота"] - loss)
                self.game.units["танки"] = max(0, self.game.units["танки"] - loss//3)
                self.game.stability = max(0, self.game.stability - 10)
                self.game.military.update_morale(False, loss)
                logger.log(f"Поражение от {enemy}", "WARNING")
            break