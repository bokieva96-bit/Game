from utils import get_date_str, safe_input

class TechManager:
    def __init__(self, game):
        self.game = game

    def init_techs(self):
        tech_list = {
            "Пехота II": {"cost": 300, "time": 6, "effect": "infantry_bonus", "value": 2},
            "Пехота III": {"cost": 500, "time": 8, "effect": "infantry_bonus", "value": 3, "requires": "Пехота II"},
            "Танки I": {"cost": 400, "time": 7, "effect": "tank_bonus", "value": 2},
            "Танки II": {"cost": 600, "time": 9, "effect": "tank_bonus", "value": 3, "requires": "Танки I"},
            "Авиация I": {"cost": 350, "time": 6, "effect": "air_bonus", "value": 2},
            "Авиация II": {"cost": 550, "time": 8, "effect": "air_bonus", "value": 3, "requires": "Авиация I"},
            "Ракетостроение": {"cost": 700, "time": 10, "effect": "rocket_bonus", "value": 2},
            "Артиллерия": {"cost": 300, "time": 5, "effect": "artillery_bonus", "value": 3},
            "Экономика I": {"cost": 200, "time": 4, "effect": "income_bonus", "value": 20},
            "Экономика II": {"cost": 400, "time": 6, "effect": "income_bonus", "value": 30, "requires": "Экономика I"},
            "Промышленность": {"cost": 500, "time": 7, "effect": "prod_bonus", "value": 10},
            "Ядерная физика": {"cost": 1000, "time": 15, "effect": "nuclear_unlock", "value": 1, "year_required": 1943},
            "Радары": {"cost": 400, "time": 6, "effect": "radar_bonus", "value": 10, "requires": "Экономика I"},
            "Шифрование": {"cost": 300, "time": 5, "effect": "spy_defense", "value": 20},
            "Ядерный реактор": {"cost": 1200, "time": 12, "effect": "income_bonus", "value": 100, "requires": "Ядерная физика"},
            "Зенитные орудия": {"cost": 350, "time": 5, "effect": "aa_bonus", "value": 5}
        }
        self.game.techs = {}
        for name, data in tech_list.items():
            self.game.techs[name] = {"researched": False, "progress": 0, "cost": data["cost"], "time": data["time"],
                                     "effect": data["effect"], "value": data["value"], "requires": data.get("requires", None),
                                     "year_required": data.get("year_required", 1900)}

    def get_tech_bonuses(self):
        bonuses = {}
        for tech, data in self.game.techs.items():
            if data["researched"]:
                effect = data["effect"]
                value = data["value"]
                if effect in ["infantry_bonus", "tank_bonus", "air_bonus", "rocket_bonus", "artillery_bonus"]:
                    bonuses[effect] = bonuses.get(effect, 0) + value
                elif effect == "income_bonus":
                    bonuses["income_bonus"] = bonuses.get("income_bonus", 0) + value
                elif effect == "prod_bonus":
                    bonuses["prod_bonus"] = bonuses.get("prod_bonus", 0) + value
                elif effect == "nuclear_unlock":
                    bonuses["nuclear_unlock"] = True
        return bonuses

    def tech_menu(self):
        while True:
            print("\n--- ТЕХНОЛОГИЧЕСКОЕ ДЕРЕВО ---")
            print("Текущие исследования: ", self.game.active_research if self.game.active_research else "нет")
            if self.game.active_research:
                print("Прогресс: {}/{}".format(self.game.research_progress, self.game.techs[self.game.active_research]["time"]))
            print("\nДоступные технологии:")
            idx = 1
            tech_list = []
            for tech, data in self.game.techs.items():
                if data["researched"]:
                    continue
                req = data.get("requires")
                if req and not self.game.techs[req]["researched"]:
                    continue
                if data.get("year_required", 1900) > get_date_str(self.game.turn)[1]:
                    continue
                tech_list.append(tech)
                print(f"{idx}. {tech} | Стоимость: {data['cost']}💰 | Время: {data['time']} мес")
                idx += 1
            if not tech_list:
                print("Нет доступных технологий.")
            print(f"{len(tech_list)+1}. Назад")
            choice = safe_input("Выберите технологию для исследования или выход: ")
            try:
                ch = int(choice) - 1
                if ch == len(tech_list):
                    break
                selected = tech_list[ch]
            except:
                print("❌ Неверно.")
                continue
            if self.game.active_research:
                print("⚠️ Вы уже исследуете технологию. Дождитесь завершения или отмените (пока не реализовано).")
                continue
            if self.game.player_gold < self.game.techs[selected]["cost"]:
                print("❌ Недостаточно золота!")
                continue
            self.game.player_gold -= self.game.techs[selected]["cost"]
            self.game.active_research = selected
            self.game.research_progress = 0
            print(f"🔬 Начато исследование {selected}")

    def advance_research(self):
        if self.game.active_research:
            self.game.research_progress += 1
            tech = self.game.active_research
            if self.game.research_progress >= self.game.techs[tech]["time"]:
                self.game.techs[tech]["researched"] = True
                self.game.stats["techs_researched"] += 1
                print(f"✅ Исследована технология {tech}!")
                if self.game.techs[tech]["effect"] == "nuclear_unlock":
                    self.game.nuclear_researched = True
                    print("☢️ Теперь доступна ядерная программа!")
                self.game.active_research = None
                self.game.research_progress = 0