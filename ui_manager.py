class UIManager:
    def __init__(self, game):
        self.game = game

    def get_active_modifiers(self):
        mods = []
        bonuses = self.game.get_tech_bonuses()
        if bonuses.get("infantry_bonus"):
            mods.append(f"Пехота +{bonuses['infantry_bonus']} силы")
        if bonuses.get("tank_bonus"):
            mods.append(f"Танки +{bonuses['tank_bonus']} силы")
        if bonuses.get("air_bonus"):
            mods.append(f"Авиация +{bonuses['air_bonus']} силы")
        if bonuses.get("rocket_bonus"):
            mods.append(f"Ракеты +{bonuses['rocket_bonus']} силы")
        if bonuses.get("artillery_bonus"):
            mods.append(f"Артиллерия +{bonuses['artillery_bonus']} силы")
        if bonuses.get("income_bonus"):
            mods.append(f"Доход +{bonuses['income_bonus']}💰")
        if self.game.trade_agreements:
            mods.append(f"Торговля с {len(self.game.trade_agreements)} странами (+{len(self.game.trade_agreements)*10}% дохода)")
        for p in self.game.personalities:
            mods.append(f"Личность {p['name']}: {p['bonus']} +{p['effect']}")
        return mods

    def draw_graph(self, values, label, width=40):
        if not values:
            return
        max_val = max(values) if max(values) > 0 else 1
        print(f"\n{label}:")
        for i, v in enumerate(values):
            bar = "#" * int(v / max_val * width)
            print(f"{i:3} | {bar}")

    def show_statistics_graphs(self):
        if hasattr(self.game, 'history_gold') and self.game.history_gold:
            self.draw_graph(self.game.history_gold, "Золото")
            self.draw_graph(self.game.history_army, "Армия")
            self.draw_graph(self.game.history_stability, "Стабильность")