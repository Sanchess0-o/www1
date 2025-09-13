from random import randint, choice
import requests

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.ability = self.get_ability()
        self.height = self.get_height()
        self.weight = self.get_weight()
        self.level = 1
        self.experience = 0
        self.attack = randint(10, 30)
        self.defense = randint(5, 20)
        Pokemon.pokemons[pokemon_trainer] = self

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['sprites']['other']['official-artwork']['front_default']
        except:
            pass
        return "https://png.pngtree.com/png-vector/20221125/ourmid/pngtree-no-image-available-icon-flatvector-illustration-pic-design-profile-vector-png-image_40966566.jpg"
    
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['forms'][0]['name']
        except:
            pass
        return "Pikachu"
    
    def get_ability(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['abilities']:
                    return data['abilities'][0]['ability']['name']
        except:
            pass
        return "Не удалось получить способность"
    
    def get_height(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['height']
        except:
            pass
        return 0
    
    def get_weight(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['weight']
        except:
            pass
        return 0

    #..........................................
    def set_name(self, new_name):
        """Изменяет имя покемона"""
        self.name = new_name
        return f"Имя покемона изменено на: {self.name}"

    def set_ability(self, new_ability):
        """Изменяет способность покемона"""
        self.ability = new_ability
        return f"Способность изменена на: {self.ability}"

    def change_level(self, amount):
        """Изменяет уровень покемона"""
        self.level += amount
        if self.level < 1:
            self.level = 1
        return f"Уровень изменен: {self.level}"

    def add_experience(self, exp):
        """Добавляет опыт покемону"""
        self.experience += exp
       
        levels_gained = self.experience // 100
        if levels_gained > 0:
            self.level += levels_gained
            self.experience %= 100
            return f"Получено {exp} опыта! Повышен уровень до {self.level}!"
        return f"Получено {exp} опыта. Текущий опыт: {self.experience}/100"



    def modify_attack(self, amount):
        """Изменяет атаку покемона"""
        self.attack += amount
        if self.attack < 1:
            self.attack = 1
        return f"Атака изменена: {self.attack}"

    def modify_defense(self, amount):
        """Изменяет защиту покемона"""
        self.defense += amount
        if self.defense < 1:
            self.defense = 1
        return f"Защита изменена: {self.defense}"

    def evolve(self):
        """Эволюционирует покемона (увеличивает характеристики)"""
        old_name = self.name
        self.pokemon_number = randint(1, 1000) 
        self.img = self.get_img()
        self.name = self.get_name()
        self.ability = self.get_ability()
        
        
        self.level += 5
        self.attack += 15
        self.defense += 10
        self.health = 100
        
        return f"🎉 {old_name} эволюционировал в {self.name}! Уровень: {self.level}, Атака: {self.attack}"

    def rename(self, new_name):
        """Переименовывает покемона"""
        old_name = self.name
        self.name = new_name
        return f"Покемон {old_name} переименован в {self.name}"

    def train(self):
        """Тренировка покемона (увеличивает характеристики)"""
        self.attack += randint(1, 3)
        self.defense += randint(1, 2)
        exp_gained = randint(5, 15)
        return self.add_experience(exp_gained) + f"\nАтака: {self.attack}, Защита: {self.defense}"

    def info(self):
        """Возвращает полную информацию о покемоне"""
        return (
            f"Имя: {self.name}\n"
            f"Уровень: {self.level}\n"
            f"Опыт: {self.experience}/100\n"
            f"Атака: {self.attack}\n"
            f"Защита: {self.defense}\n"
            f"Способность: {self.ability}\n"
            f"Рост: {self.height}\n"
            f"Вес: {self.weight}"
        )

    def show_img(self):
        return self.img

    def __str__(self):
        return f"Pokemon({self.name}, Lvl: {self.level})"
