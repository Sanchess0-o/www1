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
        self.hp = randint(60, 100)  
        self.power = randint(10, 30)  
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

    def attack(self, enemy):
       
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return f" {enemy.name} использовал магический щит и уклонился от атаки!"
        
        damage = max(1, self.power - enemy.defense // 2)
        
        if enemy.hp > damage:
            enemy.hp -= damage
            return f" {self.name} атаковал {enemy.name} и нанес {damage} урона!\nУ {enemy.name} осталось {enemy.hp} HP"
        else:
            enemy.hp = 0
          
            exp_gain = randint(20, 40)
            level_up = self.add_experience(exp_gain)
            return f"🎉 {self.name} победил {enemy.name}!\n{level_up}"

    def set_name(self, new_name):
        self.name = new_name
        return f"Имя покемона изменено на: {self.name}"

    def set_ability(self, new_ability):
        self.ability = new_ability
        return f"Способность изменена на: {self.ability}"

    def change_level(self, amount):
        self.level += amount
        if self.level < 1:
            self.level = 1
        return f"Уровень изменен: {self.level}"

    def add_experience(self, exp):
        self.experience += exp
        levels_gained = self.experience // 100
        if levels_gained > 0:
            self.level += levels_gained
            self.experience %= 100
           
            self.hp += levels_gained * 10
            self.power += levels_gained * 3
            self.defense += levels_gained * 2
            return f"Получено {exp} опыта! Повышен уровень до {self.level}!"
        return f"Получено {exp} опыта. Текущий опыт: {self.experience}/100"

    def modify_attack(self, amount):
        self.power += amount
        if self.power < 1:
            self.power = 1
        return f"Атака изменена: {self.power}"

    def modify_defense(self, amount):
        self.defense += amount
        if self.defense < 1:
            self.defense = 1
        return f"Защита изменена: {self.defense}"

    def heal(self):
        heal_amount = randint(15, 30)
        self.hp += heal_amount
        max_hp = 60 + (self.level - 1) * 10
        if self.hp > max_hp:
            self.hp = max_hp
        return f" {self.name} восстановил {heal_amount} HP. Теперь у него {self.hp}/{max_hp} HP"

    def evolve(self):
        old_name = self.name
        self.pokemon_number = randint(1, 1000) 
        self.img = self.get_img()
        self.name = self.get_name()
        self.ability = self.get_ability()
        
        self.level += 3
        self.hp += 20
        self.power += 10
        self.defense += 8
        
        return f" {old_name} эволюционировал в {self.name}! Уровень: {self.level}, HP: {self.hp}"

    def rename(self, new_name):
        old_name = self.name
        self.name = new_name
        return f"Покемон {old_name} переименован в {self.name}"

    def train(self):
        self.power += randint(1, 3)
        self.defense += randint(1, 2)
        exp_gained = randint(5, 15)
        return self.add_experience(exp_gained) + f" Атака: {self.power}, Защита: {self.defense}"

    def info(self):
        max_hp = 60 + (self.level - 1) * 10
        return (
            f"Имя: {self.name}\n"
            f"Уровень: {self.level}\n"
            f"Опыт: {self.experience}/100\n"
            f"HP: {self.hp}/{max_hp}\n"
            f"Атака: {self.power}\n"
            f"Защита: {self.defense}\n"
            f"Способность: {self.ability}\n"
            f"Рост: {self.height}\n"
            f"Вес: {self.weight}"
        )

    def show_img(self):
        return self.img

    def __str__(self):
        return f"Pokemon({self.name}, Lvl: {self.level}, HP: {self.hp})"


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power += 5  
        self.ability = "Магический щит"

    def attack(self, enemy):
        # Волшебники имеют шанс на двойной урон
        chance = randint(1, 4)
        if chance == 1:
            original_power = self.power
            self.power *= 2
            result = super().attack(enemy)
            self.power = original_power
            return result + f" {self.name} использовал магическую атаку 2x!"
        return super().attack(enemy)


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp += 20 
        self.ability = "Супер-удар"

    def attack(self, enemy):
       
        super_power = randint(5, 15)
        original_power = self.power
        self.power += super_power
        result = super().attack(enemy)
        self.power = original_power
        
        if "уклонился" not in result:
            return result + f"Боец применил супер-удар силой: +{super_power}"
        return result
