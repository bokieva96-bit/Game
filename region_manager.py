from utils import safe_input

class RegionManager:
    def __init__(self, game):
        self.game = game

    def get_regions_for_country(self, country_name):
        regions_by_country = {
            "Российская Империя": [
                {"name": "Московская губ.", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 4, "железо": 1, "уголь": 1, "дерево": 3, "уран": 0, "золото": 1}, "development": 1.2},
                {"name": "Санкт-Петербургская губ.", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 3, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.1},
                {"name": "Уральский край", "resources": {"нефть": 3, "сталь": 7, "продовольствие": 2, "железо": 10, "уголь": 8, "дерево": 5, "уран": 1, "золото": 2}, "development": 1.0},
                {"name": "Сибирь", "resources": {"нефть": 8, "сталь": 4, "продовольствие": 2, "железо": 5, "уголь": 6, "дерево": 12, "уран": 2, "золото": 1}, "development": 0.5},
                {"name": "Украина", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 8, "железо": 3, "уголь": 4, "дерево": 4, "уран": 0, "золото": 1}, "development": 1.0},
                {"name": "Кавказ", "resources": {"нефть": 6, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Средняя Азия", "resources": {"нефть": 2, "сталь": 1, "продовольствие": 2, "железо": 1, "уголь": 1, "дерево": 1, "уран": 0, "золото": 2}, "development": 0.4},
                {"name": "Дальний Восток", "resources": {"нефть": 3, "сталь": 2, "продовольствие": 1, "железо": 2, "уголь": 3, "дерево": 6, "уран": 0, "золото": 0}, "development": 0.5},
                {"name": "Прибалтика", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 1, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Польша (Царство Польское)", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 3, "железо": 2, "уголь": 4, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Финляндия", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 2, "железо": 1, "уголь": 1, "дерево": 5, "уран": 0, "золото": 0}, "development": 0.8}
            ],
            "Германская Империя": [
                {"name": "Пруссия", "resources": {"нефть": 0, "сталь": 6, "продовольствие": 2, "железо": 4, "уголь": 8, "дерево": 2, "уран": 0, "золото": 1}, "development": 1.8},
                {"name": "Бавария", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 4, "железо": 2, "уголь": 3, "дерево": 5, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Саксония", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 3, "железо": 3, "уголь": 5, "дерево": 3, "уран": 0, "золото": 0}, "development": 1.2},
                {"name": "Вюртемберг", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 2, "железо": 1, "уголь": 2, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Баден", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Рейнская область", "resources": {"нефть": 0, "сталь": 8, "продовольствие": 2, "железо": 5, "уголь": 10, "дерево": 2, "уран": 0, "золото": 1}, "development": 2.0},
                {"name": "Силезия", "resources": {"нефть": 0, "сталь": 4, "продовольствие": 2, "железо": 5, "уголь": 7, "дерево": 3, "уран": 0, "золото": 0}, "development": 1.1},
                {"name": "Померания", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 3, "железо": 1, "уголь": 2, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.8}
            ],
            "Британская Империя": [
                {"name": "Англия", "resources": {"нефть": 2, "сталь": 5, "продовольствие": 4, "железо": 4, "уголь": 8, "дерево": 2, "уран": 0, "золото": 4}, "development": 2.0},
                {"name": "Шотландия", "resources": {"нефть": 3, "сталь": 3, "продовольствие": 3, "железо": 4, "уголь": 5, "дерево": 4, "уран": 0, "золото": 1}, "development": 0.9},
                {"name": "Уэльс", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 2, "железо": 3, "уголь": 6, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Ирландия", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 4, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.7},
                {"name": "Канада", "resources": {"нефть": 3, "сталь": 2, "продовольствие": 3, "железо": 3, "уголь": 4, "дерево": 8, "уран": 1, "золото": 1}, "development": 0.8},
                {"name": "Австралия", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 2, "железо": 4, "уголь": 3, "дерево": 3, "уран": 2, "золото": 3}, "development": 0.6},
                {"name": "Новая Зеландия", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 2, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.5},
                {"name": "Южная Африка", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 2, "железо": 3, "уголь": 2, "дерево": 2, "уран": 0, "золото": 5}, "development": 0.6},
                {"name": "Индия", "resources": {"нефть": 2, "сталь": 3, "продовольствие": 10, "железо": 4, "уголь": 5, "дерево": 6, "уран": 0, "золото": 2}, "development": 0.7}
            ],
            "Французская Республика": [
                {"name": "Иль-де-Франс", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 3, "железо": 2, "уголь": 2, "дерево": 2, "уран": 0, "золото": 2}, "development": 1.5},
                {"name": "Лоррейн", "resources": {"нефть": 0, "сталь": 7, "продовольствие": 2, "железо": 6, "уголь": 8, "дерево": 2, "уран": 0, "золото": 1}, "development": 1.2},
                {"name": "Эльзас", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 2, "железо": 2, "уголь": 4, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Нормандия", "resources": {"нефть": 1, "сталь": 1, "продовольствие": 5, "железо": 1, "уголь": 1, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Бретань", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 4, "железо": 1, "уголь": 1, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Прованс", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 4, "железо": 2, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Лионский регион", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 3, "железо": 2, "уголь": 3, "дерево": 3, "уран": 0, "золото": 0}, "development": 1.0}
            ],
            "Австро-Венгрия": [
                {"name": "Нижняя Австрия", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 4, "железо": 2, "уголь": 4, "дерево": 3, "уран": 0, "золото": 1}, "development": 1.1},
                {"name": "Венгрия", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 6, "железо": 2, "уголь": 3, "дерево": 5, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Богемия", "resources": {"нефть": 0, "сталь": 4, "продовольствие": 3, "железо": 4, "уголь": 6, "дерево": 4, "уран": 0, "золото": 1}, "development": 1.2},
                {"name": "Моравия", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 3, "железо": 3, "уголь": 5, "дерево": 4, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Словакия", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 4, "железо": 2, "уголь": 3, "дерево": 5, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Галиция", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 4, "железо": 2, "уголь": 4, "дерево": 5, "уран": 0, "золото": 0}, "development": 0.7},
                {"name": "Трансильвания", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 5, "железо": 2, "уголь": 3, "дерево": 6, "уран": 0, "золото": 0}, "development": 0.8}
            ],
            "Королевство Италия": [
                {"name": "Ломбардия", "resources": {"нефть": 0, "сталь": 4, "продовольствие": 3, "железо": 3, "уголь": 3, "дерево": 3, "уран": 0, "золото": 1}, "development": 1.3},
                {"name": "Венеция", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 3, "железо": 2, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Тоскана", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 4, "железо": 2, "уголь": 2, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Неаполь", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 5, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Сицилия", "resources": {"нефть": 1, "сталь": 1, "продовольствие": 4, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.6},
                {"name": "Пьемонт", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 3, "железо": 2, "уголь": 3, "дерево": 4, "уран": 0, "золото": 0}, "development": 1.0}
            ],
            "Османская Империя": [
                {"name": "Стамбул", "resources": {"нефть": 2, "сталь": 3, "продовольствие": 4, "железо": 2, "уголь": 3, "дерево": 2, "уран": 0, "золото": 2}, "development": 1.2},
                {"name": "Анатолия", "resources": {"нефть": 3, "сталь": 2, "продовольствие": 4, "железо": 2, "уголь": 3, "дерево": 3, "уран": 0, "золото": 1}, "development": 0.9},
                {"name": "Месопотамия", "resources": {"нефть": 8, "сталь": 1, "продовольствие": 2, "железо": 1, "уголь": 1, "дерево": 1, "уран": 0, "золото": 0}, "development": 0.6},
                {"name": "Сирия", "resources": {"нефть": 2, "сталь": 1, "продовольствие": 4, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.7},
                {"name": "Египет", "resources": {"нефть": 1, "сталь": 1, "продовольствие": 6, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 1}, "development": 0.5},
                {"name": "Аравия", "resources": {"нефть": 6, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 0, "дерево": 0, "уран": 0, "золото": 0}, "development": 0.3}
            ],
            "США": [
                {"name": "Нью-Йорк", "resources": {"нефть": 2, "сталь": 5, "продовольствие": 4, "железо": 4, "уголь": 5, "дерево": 3, "уран": 0, "золото": 5}, "development": 2.0},
                {"name": "Пенсильвания", "resources": {"нефть": 1, "сталь": 7, "продовольствие": 3, "железо": 6, "уголь": 8, "дерево": 3, "уран": 0, "золото": 2}, "development": 1.8},
                {"name": "Техас", "resources": {"нефть": 12, "сталь": 3, "продовольствие": 3, "железо": 2, "уголь": 3, "дерево": 2, "уран": 0, "золото": 2}, "development": 1.0},
                {"name": "Калифорния", "resources": {"нефть": 5, "сталь": 3, "продовольствие": 6, "железо": 3, "уголь": 2, "дерево": 8, "уран": 0, "золото": 6}, "development": 1.3},
                {"name": "Иллинойс", "resources": {"нефть": 1, "сталь": 4, "продовольствие": 6, "железо": 3, "уголь": 5, "дерево": 3, "уран": 0, "золото": 1}, "development": 1.2},
                {"name": "Флорида", "resources": {"нефть": 2, "сталь": 1, "продовольствие": 5, "железо": 1, "уголь": 1, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.6},
                {"name": "Огайо", "resources": {"нефть": 1, "сталь": 5, "продовольствие": 4, "железо": 4, "уголь": 6, "дерево": 4, "уран": 0, "золото": 1}, "development": 1.1}
            ],
            "Испания": [
                {"name": "Кастилия", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 4, "железо": 2, "уголь": 3, "дерево": 2, "уран": 0, "золото": 1}, "development": 1.0},
                {"name": "Каталония", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 3, "железо": 2, "уголь": 2, "дерево": 4, "уран": 0, "золото": 0}, "development": 1.2},
                {"name": "Арагон", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Андалусия", "resources": {"нефть": 1, "сталь": 1, "продовольствие": 5, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.7},
                {"name": "Валенсия", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 4, "железо": 1, "уголь": 1, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.8}
            ],
            "Португалия": [
                {"name": "Лиссабон", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 4, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 1}, "development": 1.0},
                {"name": "Порту", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 1, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Коимбра", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 2, "железо": 1, "уголь": 1, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.7}
            ],
            "Бельгия": [
                {"name": "Брюссель", "resources": {"нефть": 0, "сталь": 3, "продовольствие": 2, "железо": 2, "уголь": 4, "дерево": 1, "уран": 0, "золото": 1}, "development": 1.5},
                {"name": "Антверпен", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 3, "железо": 1, "уголь": 3, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.2},
                {"name": "Льеж", "resources": {"нефть": 0, "сталь": 4, "продовольствие": 2, "железо": 3, "уголь": 5, "дерево": 1, "уран": 0, "золото": 0}, "development": 1.1}
            ],
            "Нидерланды": [
                {"name": "Амстердам", "resources": {"нефть": 1, "сталь": 2, "продовольствие": 4, "железо": 1, "уголь": 2, "дерево": 2, "уран": 0, "золото": 2}, "development": 1.3},
                {"name": "Роттердам", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Гаага", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 2, "железо": 0, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.9}
            ],
            "Швейцария": [
                {"name": "Берн", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 1, "дерево": 3, "уран": 0, "золото": 3}, "development": 1.0},
                {"name": "Цюрих", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 2, "железо": 0, "уголь": 0, "дерево": 2, "уран": 0, "золото": 4}, "development": 1.5},
                {"name": "Женева", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 2, "железо": 0, "уголь": 0, "дерево": 2, "уран": 0, "золото": 2}, "development": 1.2}
            ],
            "Швеция": [
                {"name": "Стокгольм", "resources": {"нефть": 1, "сталь": 3, "продовольствие": 3, "железо": 4, "уголь": 2, "дерево": 5, "уран": 0, "золото": 1}, "development": 1.0},
                {"name": "Гётеборг", "resources": {"нефть": 0, "сталь": 2, "продовольствие": 2, "железо": 3, "уголь": 2, "дерево": 4, "уран": 0, "золото": 0}, "development": 0.9},
                {"name": "Мальмё", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 2, "уголь": 1, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.7}
            ],
            "Норвегия": [
                {"name": "Осло", "resources": {"нефть": 1, "сталь": 1, "продовольствие": 2, "железо": 1, "уголь": 0, "дерево": 4, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Берген", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 0, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Тронхейм", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 0, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.7}
            ],
            "Дания": [
                {"name": "Копенгаген", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Орхус", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 2, "железо": 0, "уголь": 0, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.7},
                {"name": "Оденсе", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 2, "железо": 0, "уголь": 0, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.6}
            ],
            "Греция": [
                {"name": "Аттика", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 4, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Пелопоннес", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 3, "железо": 0, "уголь": 0, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.7},
                {"name": "Македония", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.8}
            ],
            "Болгария": [
                {"name": "София", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 2, "дерево": 2, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Пловдив", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 2, "железо": 0, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.7},
                {"name": "Варна", "resources": {"нефть": 1, "сталь": 0, "продовольствие": 2, "железо": 0, "уголь": 0, "дерево": 1, "уран": 0, "золото": 0}, "development": 0.6}
            ],
            "Сербия": [
                {"name": "Белград", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 2, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Ниш", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 1, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.6},
                {"name": "Крагуевац", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 0, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.5}
            ],
            "Румыния": [
                {"name": "Бухарест", "resources": {"нефть": 3, "сталь": 1, "продовольствие": 3, "железо": 1, "уголь": 2, "дерево": 3, "уран": 0, "золото": 0}, "development": 1.0},
                {"name": "Плоешти", "resources": {"нефть": 5, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 1, "дерево": 1, "уран": 0, "золото": 0}, "development": 0.8},
                {"name": "Яссы", "resources": {"нефть": 0, "сталь": 1, "продовольствие": 2, "железо": 1, "уголь": 1, "дерево": 3, "уран": 0, "золото": 0}, "development": 0.7}
            ],
            "Черногория": [
                {"name": "Цетине", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 0, "дерево": 2, "уран": 0, "золото": 0}, "development": 0.5},
                {"name": "Подгорица", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 1, "железо": 0, "уголь": 0, "дерево": 1, "уран": 0, "золото": 0}, "development": 0.4},
                {"name": "Никшич", "resources": {"нефть": 0, "сталь": 0, "продовольствие": 0, "железо": 0, "уголь": 0, "дерево": 1, "уран": 0, "золото": 0}, "development": 0.3}
            ]
        }
        default = [{"name": "Столица", "resources": {"нефть": 2, "сталь": 2, "продовольствие": 2, "железо": 2, "уголь": 2, "дерево": 2, "уран": 0, "золото": 1}, "development": 1.0}]
        return regions_by_country.get(country_name, default)

    def regions_menu(self):
        while True:
            print("\n--- УПРАВЛЕНИЕ РЕГИОНАМИ ---")
            if not self.game.regions:
                print("Нет регионов.")
                input("Нажмите Enter для продолжения...")
                break
            total_prod = self.calc_total_region_production()
            print(f"📊 Суммарная добыча ресурсов из регионов: {total_prod} ед./ход")
            for idx, region in enumerate(self.game.regions, 1):
                dev = region["development"]
                res_str = ", ".join([f"{k}: {int(v*dev)}" for k, v in region["resources"].items()])
                print(f"{idx}. {region['name']} | Развитие: {dev:.1f} | Ресурсы (добыча): {res_str}")
            print(f"{len(self.game.regions)+1}. Инвестировать в развитие региона (100💰 за +0.2)")
            print(f"{len(self.game.regions)+2}. Назад")
            choice = safe_input("Выберите: ")
            try:
                idx = int(choice) - 1
                if idx == len(self.game.regions):
                    self.invest_in_region()
                    continue
                elif idx == len(self.game.regions) + 1:
                    break
                region = self.game.regions[idx]
                print(f"\nРегион {region['name']}:")
                print(f"  Развитие: {region['development']:.1f}")
                print("  Базовые ресурсы (до умножения на развитие):")
                for res, val in region["resources"].items():
                    print(f"    {res}: {val} (добыча {int(val*region['development'])}")
                input("Нажмите Enter для продолжения...")
            except:
                print("❌ Неверный выбор.")

    def invest_in_region(self):
        if not self.game.regions:
            print("Нет регионов.")
            return
        print("\nВыберите регион для инвестиций:")
        for idx, region in enumerate(self.game.regions, 1):
            print(f"{idx}. {region['name']} (развитие {region['development']:.1f})")
        print(f"{len(self.game.regions)+1}. Отмена")
        choice = safe_input("Номер: ")
        try:
            idx = int(choice) - 1
            if idx == len(self.game.regions):
                return
            region = self.game.regions[idx]
        except:
            print("❌ Неверный выбор.")
            return
        if self.game.player_gold < 100:
            print("❌ Недостаточно золота!")
            return
        self.game.player_gold -= 100
        region["development"] += 0.2
        print(f"✅ Развитие {region['name']} увеличено до {region['development']:.1f}!")

    def calc_total_region_production(self):
        total = {res: 0 for res in self.game.player_resources.keys()}
        for region in self.game.regions:
            dev = region.get("development", 1.0)
            for res, amount in region.get("resources", {}).items():
                total[res] = total.get(res, 0) + int(amount * dev)
        return total

    def capture_region_from_enemy(self, enemy):
        enemy_data = None
        for data in self.game.countries_data.values():
            if data["name"] == enemy:
                enemy_data = data
                break
        if not enemy_data:
            return False
        if enemy_data.get("regions") and len(enemy_data["regions"]) > 0:
            captured_region = enemy_data["regions"][0]
            enemy_data["regions"].remove(captured_region)
            self.game.regions.append(captured_region)
            self.game.stats["regions_captured"] += 1
            print(f"🏴 Вы захватили регион {captured_region['name']} у {enemy}!")
        else:
            fake_region = {
                "name": f"Территория {enemy}",
                "resources": {res: max(1, val // 5) for res, val in enemy_data.get("resources", {}).items()},
                "development": 0.5
            }
            self.game.regions.append(fake_region)
            self.game.stats["regions_captured"] += 1
            print(f"🏴 Вы захватили регион {fake_region['name']} у {enemy}!")
        return True

    def buy_region_from_ai(self, country):
        if country not in self.game.ai_countries:
            print("❌ Нет такой страны.")
            return
        if self.game.diplomacy[country]["relations"] < 30:
            print("❌ Отношения слишком низкие (нужно > 30).")
            return
        country_data = None
        for data in self.game.countries_data.values():
            if data["name"] == country:
                country_data = data
                break
        if not country_data or not country_data.get("regions"):
            print("❌ У этой страны нет регионов для продажи.")
            return
        print(f"\nДоступные регионы {country} для покупки:")
        regions = country_data["regions"]
        for idx, reg in enumerate(regions, 1):
            dev = reg.get("development", 1.0)
            res_str = ", ".join([f"{k}: {int(v*dev)}" for k, v in reg["resources"].items()])
            print(f"{idx}. {reg['name']} (развитие {dev:.1f}, ресурсы: {res_str})")
        print(f"{len(regions)+1}. Отмена")
        ch = safe_input("Выберите номер региона: ")
        try:
            idx = int(ch) - 1
            if idx == len(regions):
                return
            selected_region = regions[idx]
        except:
            print("❌ Неверный выбор.")
            return
        base_price = 3000 + int(selected_region["development"] * 1000)
        for res, val in selected_region["resources"].items():
            base_price += val * 50
        print(f"Стоимость региона {selected_region['name']}: {base_price}💰")
        print("1. Купить")
        print("2. Отказаться")
        ch2 = safe_input("Выбор: ", valid_options=["1","2"], default="2")
        if ch2 == "1":
            if self.game.player_gold < base_price:
                print("❌ Недостаточно золота!")
                return
            self.game.player_gold -= base_price
            country_data["regions"].remove(selected_region)
            self.game.regions.append(selected_region)
            self.game.stats["regions_bought"] += 1
            self.game.diplomacy[country]["relations"] = min(100, self.game.diplomacy[country]["relations"] + 15)
            print(f"✅ Вы купили регион {selected_region['name']} у {country}!")

    def sell_region_to_ai(self, country):
        if not self.game.regions:
            print("❌ У вас нет регионов для продажи.")
            return
        if country not in self.game.ai_countries:
            print("❌ Нет такой страны.")
            return
        if self.game.diplomacy[country]["relations"] < 30:
            print("❌ Отношения слишком низкие (нужно > 30).")
            return
        print("\nВыберите регион для продажи:")
        for idx, region in enumerate(self.game.regions, 1):
            print(f"{idx}. {region['name']} (развитие {region['development']:.1f})")
        print(f"{len(self.game.regions)+1}. Отмена")
        choice = safe_input("Номер: ")
        try:
            idx = int(choice) - 1
            if idx == len(self.game.regions):
                return
            selected_region = self.game.regions[idx]
        except:
            print("❌ Неверный выбор.")
            return
        base_price = 2000 + int(selected_region["development"] * 1000)
        for res, val in selected_region["resources"].items():
            base_price += val * 50
        print(f"{country} предлагает {base_price}💰 за регион {selected_region['name']}.")
        print("1. Принять")
        print("2. Отказаться")
        ch = safe_input("Выбор: ", valid_options=["1","2"], default="2")
        if ch == "1":
            self.game.player_gold += base_price
            self.game.regions.remove(selected_region)
            country_data = None
            for data in self.game.countries_data.values():
                if data["name"] == country:
                    country_data = data
                    break
            if country_data:
                if "regions" not in country_data:
                    country_data["regions"] = []
                country_data["regions"].append(selected_region)
            self.game.stats["regions_sold"] += 1
            self.game.diplomacy[country]["relations"] = min(100, self.game.diplomacy[country]["relations"] + 10)
            print(f"✅ Вы продали регион {country} за {base_price}💰!")

    def buy_region_from_ai_menu(self):
        print("\nВыберите страну, у которой хотите купить регион:")
        countries = [c for c in self.game.ai_countries if self.game.diplomacy[c]["relations"] >= 30 and self.game.diplomacy[c]["status"] != "Война"]
        if not countries:
            print("Нет стран с достаточно хорошими отношениями.")
            return
        for idx, c in enumerate(countries, 1):
            print(f"{idx}. {c}")
        print(f"{len(countries)+1}. Назад")
        ch = safe_input("Номер: ")
        try:
            idx = int(ch) - 1
            if idx == len(countries):
                return
            target = countries[idx]
        except:
            print("❌ Неверно.")
            return
        self.buy_region_from_ai(target)

    def sell_region_to_ai_menu(self):
        print("\nВыберите страну, которой хотите продать регион:")
        countries = [c for c in self.game.ai_countries if self.game.diplomacy[c]["relations"] >= 30 and self.game.diplomacy[c]["status"] != "Война"]
        if not countries:
            print("Нет стран с достаточно хорошими отношениями.")
            return
        for idx, c in enumerate(countries, 1):
            print(f"{idx}. {c}")
        print(f"{len(countries)+1}. Назад")
        ch = safe_input("Номер: ")
        try:
            idx = int(ch) - 1
            if idx == len(countries):
                return
            target = countries[idx]
        except:
            print("❌ Неверно.")
            return
        self.sell_region_to_ai(target)