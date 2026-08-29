from utils import get_date_str, safe_input, clamp

class EventManager:
    def __init__(self, game):
        self.game = game

    def handle_historical_events(self):
        date_str, year, month = get_date_str(self.game.turn)
        event_key = f"{year}-{month}"
        if event_key in self.game.historical_events_triggered:
            return

        if year == 1904 and month == 2:
            print("\n📰 [ИСТОРИЯ] 1904 год: Начало Русско-японской войны!")
            if self.game.player_name == "Российская Империя":
                self.game.units["пехота"] = max(0, self.game.units["пехота"] - 30)
                self.game.player_gold = max(0, self.game.player_gold - 400)
                self.game.stability = max(0, self.game.stability - 10)
                print("⚠️ Вы теряете ресурсы и солдат на Дальнем Востоке.")
            else:
                print("🌍 Мировые рынки лихорадит из-за конфликта в Азии.")
            self.game.historical_events_triggered.add(event_key)

        elif year == 1914 and month == 7:
            print("\n🚨 [ИСТОРИЯ] ИЮЛЬ 1914 ГОДА: Убийство эрцгерцога! НАЧАЛАСЬ ПЕРВАЯ МИРОВАЯ ВОЙНА!")
            self.game.countries_data["6"]["bloc"] = "Антанта"
            if self.game.player_name == "Королевство Италия":
                self.game.player_bloc = "Антанта"
            entente = ["Российская Империя", "Британская Империя", "Французская Республика", "Королевство Италия"]
            central = ["Германская Империя", "Австро-Венгрия", "Османская Империя"]
            for c in self.game.ai_countries:
                c_bloc = self.game.get_country_bloc(c)
                if self.game.player_bloc in ["Антанта", "Союзники"] and c_bloc == "Центральные державы":
                    self.game.diplomacy[c]["status"] = "Война"
                    self.game.diplomacy[c]["relations"] = -100
                elif self.game.player_bloc == "Центральные державы" and c_bloc in ["Антанта", "Союзники"]:
                    self.game.diplomacy[c]["status"] = "Война"
                    self.game.diplomacy[c]["relations"] = -100
                elif self.game.player_bloc in ["Антанта", "Союзники"] and c_bloc in ["Антанта", "Союзники"]:
                    self.game.diplomacy[c]["status"] = "Союз"
                    self.game.diplomacy[c]["relations"] = 100
                elif self.game.player_bloc == "Центральные державы" and c_bloc == "Центральные державы":
                    self.game.diplomacy[c]["status"] = "Союз"
                    self.game.diplomacy[c]["relations"] = 100
            print("⚔️ Мир раскололся на Антанту и Центральные державы!")
            self.game.historical_events_triggered.add(event_key)

        elif year == 1917 and month == 10:
            print("\n📰 [ИСТОРИЯ] 1917 год: Октябрьская Революция. Кризис старых империй.")
            if self.game.player_name in ["Российская Империя", "Австро-Венгрия", "Османская Империя"]:
                print("В вашей стране назревает революция! Что вы предпримете?")
                print("1. Подавить силой (потеря армии, но сохранение власти)")
                print("2. Провести реформы (снижение дохода, но рост стабильности)")
                print("3. Отречься и уйти (конец игры, но почётный финал)")
                choice = safe_input("Выбор: ", valid_options=["1","2","3"], default="1")
                if choice == "1":
                    self.game.units["пехота"] = max(0, self.game.units["пехота"] - 20)
                    self.game.stability = max(0, self.game.stability - 30)
                    print("💥 Вы подавили восстание, но армия ослаблена, народ недоволен.")
                elif choice == "2":
                    self.game.player_income = max(0, self.game.player_income - 50)
                    self.game.stability = min(100, self.game.stability + 30)
                    print("📜 Реформы проведены, стабильность растёт, но экономика пострадала.")
                else:
                    print("🏳️ Вы передали власть. Игра окончена.")
                    self.game.game_over = True
                    return
            if "США" in self.game.ai_countries:
                print("🇺🇸 США объявляют о вступлении в войну на стороне Антанты!")
                self.game.countries_data["8"]["bloc"] = "Союзники"
                if self.game.player_name == "США":
                    self.game.player_bloc = "Союзники"
                for c in self.game.ai_countries:
                    if self.game.get_country_bloc(c) == "Центральные державы":
                        self.game.diplomacy[c]["status"] = "Война"
                        self.game.diplomacy[c]["relations"] = -100
            self.game.historical_events_triggered.add(event_key)

        elif year == 1918 and month == 11:
            print("\n🕊️ [ИСТОРИЯ] НОЯБРЬ 1918 ГОДА: Компьенское перемирие. Первая мировая война окончена!")
            for c in self.game.ai_countries:
                if self.game.diplomacy[c]["status"] == "Война":
                    self.game.diplomacy[c]["status"] = "Нейтралитет"
                    self.game.diplomacy[c]["relations"] = max(-50, self.game.diplomacy[c]["relations"] - 20)
            print("🌍 Наступил хрупкий Версальский мир.")
            self.game.historical_events_triggered.add(event_key)

        elif year == 1929 and month == 10:
            print("\n📉 [ИСТОРИЯ] ОКТЯБРЬ 1929 ГОДА: Крах на Нью-Йоркской бирже! Началась Великая депрессия.")
            self.game.player_income = max(20, self.game.player_income // 2)
            self.game.player_gold = max(100, self.game.player_gold - 500)
            self.game.stability = max(0, self.game.stability - 15)
            print("💥 Мировой экономический кризис! Ваши доходы урезаны, стабильность падает.")
            self.game.historical_events_triggered.add(event_key)

        elif year == 1939 and month == 9:
            print("\n🚨 [ИСТОРИЯ] СЕНТЯБРЬ 1939 ГОДА: Нападение на Польшу. НАЧАЛАСЬ ВТОРАЯ МИРОВАЯ ВОЙНА!")
            axis = ["Германская Империя", "Королевство Италия"]
            allies = ["Российская Империя", "Британская Империя", "Французская Республика", "США"]
            for c in self.game.ai_countries:
                if c in axis:
                    self.game.countries_data[self.game.get_key_by_name(c)]["bloc"] = "Ось"
                elif c in allies:
                    self.game.countries_data[self.game.get_key_by_name(c)]["bloc"] = "Союзники"
            if self.game.player_name in axis:
                self.game.player_bloc = "Ось"
                for c in self.game.ai_countries:
                    if self.game.get_country_bloc(c) == "Союзники":
                        self.game.diplomacy[c]["status"] = "Война"
                        self.game.diplomacy[c]["relations"] = -100
            elif self.game.player_name in allies:
                self.game.player_bloc = "Союзники"
                for c in self.game.ai_countries:
                    if self.game.get_country_bloc(c) == "Ось":
                        self.game.diplomacy[c]["status"] = "Война"
                        self.game.diplomacy[c]["relations"] = -100
            else:
                print("Вы нейтральны. Вступить в войну?")
                print("1. Присоединиться к Союзникам")
                print("2. Присоединиться к Оси")
                print("3. Остаться нейтральным (риск нападения)")
                ch = safe_input("Выбор: ", valid_options=["1","2","3"], default="3")
                if ch == "1":
                    self.game.player_bloc = "Союзники"
                    for c in self.game.ai_countries:
                        if self.game.get_country_bloc(c) == "Ось":
                            self.game.diplomacy[c]["status"] = "Война"
                            self.game.diplomacy[c]["relations"] = -100
                elif ch == "2":
                    self.game.player_bloc = "Ось"
                    for c in self.game.ai_countries:
                        if self.game.get_country_bloc(c) == "Союзники":
                            self.game.diplomacy[c]["status"] = "Война"
                            self.game.diplomacy[c]["relations"] = -100
                else:
                    print("🤝 Вы остались нейтральны. Но мир нестабилен.")
            print("💥 Фашистский блок бросает вызов всему миру.")
            self.game.historical_events_triggered.add(event_key)

        elif year == 1945 and month == 5:
            print("\n☮️ [ИСТОРИЯ] МАЙ 1945 ГОДА: Разгром Берлина. Вторая мировая война в Европе завершена. Создание ООН.")
            print("ООН предлагает вам членство. Что делать?")
            print("1. Вступить (улучшение отношений со всеми, но снижение суверенитета)")
            print("2. Отказаться (сохранение свободы действий, но изоляция)")
            ch = safe_input("Выбор: ", valid_options=["1","2"], default="1")
            if ch == "1":
                for c in self.game.ai_countries:
                    self.game.diplomacy[c]["relations"] = min(100, self.game.diplomacy[c]["relations"] + 20)
                print("🌍 Вы стали членом ООН. Отношения улучшены.")
            else:
                print("🚫 Вы отказались. Мир смотрит на вас с подозрением.")
            for c in self.game.ai_countries:
                if self.game.diplomacy[c]["status"] == "Война":
                    self.game.diplomacy[c]["status"] = "Нейтралитет"
                    self.game.diplomacy[c]["relations"] = max(0, self.game.diplomacy[c]["relations"] + 10)
            print("🕊️ Начат послевоенный раздел мира.")
            self.game.historical_events_triggered.add(event_key)

        # Дополнительные события (из events.py)
        self.handle_historical_events_extra()

    def handle_historical_events_extra(self):
        date_str, year, month = get_date_str(self.game.turn)
        event_key = f"{year}-{month}"
        if event_key in self.game.historical_events_triggered:
            return

        if year == 1905 and month == 1:
            if self.game.player_name == "Российская Империя":
                print("📰 Кровавое воскресенье – революция 1905!")
                self.game.stability -= 20
                self.game.units["пехота"] = max(0, self.game.units["пехота"] - 15)
            else:
                print("🌍 В России неспокойно, рынки падают.")
            self.game.historical_events_triggered.add(event_key)

        elif year == 1911 and month == 9:
            print("📰 Итало-турецкая война.")
            if self.game.player_name == "Османская Империя":
                self.game.stability -= 10
                self.game.player_gold = max(0, self.game.player_gold - 200)
            self.game.historical_events_triggered.add(event_key)

        elif year == 1936 and month == 7:
            print("📰 Гражданская война в Испании!")
            if self.game.player_name in ["Германская Империя", "Королевство Италия"]:
                self.game.unit_morale["пехота"] = min(100, self.game.unit_morale["пехота"] + 10)
            elif self.game.player_name in ["Российская Империя", "Французская Республика"]:
                self.game.stability = min(100, self.game.stability + 5)
            self.game.historical_events_triggered.add(event_key)

        elif year == 1941 and month == 12:
            print("📰 Перл-Харбор! США вступают в войну.")
            if self.game.player_name == "США":
                self.game.player_bloc = "Союзники"
                for c in self.game.ai_countries:
                    if self.game.get_country_bloc(c) == "Ось":
                        self.game.diplomacy[c]["status"] = "Война"
                        self.game.diplomacy[c]["relations"] = -100
            self.game.historical_events_triggered.add(event_key)

    def peace_conference(self):
        if self.game.stats["battles_won"] + self.game.stats["battles_lost"] >= 3 and not self.game.game_over:
            print("\n🕊️ МИРНАЯ КОНФЕРЕНЦИЯ! Можно получить репарации.")
            enemies = [c for c in self.game.ai_countries if self.game.diplomacy[c]["status"] == "Нейтралитет" and
                       self.game.diplomacy[c]["relations"] < 0]
            if enemies:
                print("Выберите страну для получения репараций:")
                for idx, e in enumerate(enemies, 1):
                    print(f"{idx}. {e}")
                ch = safe_input("Номер: ")
                try:
                    idx = int(ch) - 1
                    target = enemies[idx]
                except:
                    return
                for data in self.game.countries_data.values():
                    if data["name"] == target:
                        gold = data["gold"] // 2
                        self.game.player_gold += gold
                        data["gold"] -= gold
                        print(f"💰 Получено {gold} репараций от {target}.")
                        break