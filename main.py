import telebot 
from config import token
from logic import Pokemon, Wizard, Fighter
import random

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])   
def start(message):
    bot.reply_to(message, "Сначала создай покемона командой /go . Воспользуйся командой /help для списка команд")

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        
        chance = random.randint(1, 5)
        if chance == 1:
            pokemon = Wizard(message.from_user.username)
            pokemon_type = "Волшебник"
        elif chance == 2:
            pokemon = Fighter(message.from_user.username)
            pokemon_type = "Боец"
        else:
            pokemon = Pokemon(message.from_user.username)
            pokemon_type = "Обычный"
        
        bot.send_message(message.chat.id, f"{pokemon_type} покемон создан!\n{pokemon.info()}")
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
       
        if isinstance(pokemon, Wizard):
            pokemon_type = "Волшебник"
        elif isinstance(pokemon, Fighter):
            pokemon_type = "Боец"
        else:
            pokemon_type = "Обычный"
        
        bot.send_message(message.chat.id, f"{pokemon_type}\n{pokemon.info()}")
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, " Сначала создай покемона командой /go")

@bot.message_handler(commands=['train'])
def train(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.train()
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, " Сначала создай покемона командой /go")

@bot.message_handler(commands=['heal'])
def heal(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.heal()
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, " Сначала создай покемона командой /go")

@bot.message_handler(commands=['evolve'])
def evolve(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        if pokemon.level >= 3:
            result = pokemon.evolve()
            bot.send_message(message.chat.id, result)
            bot.send_photo(message.chat.id, pokemon.show_img())
        else:
            bot.reply_to(message, " Нужен как минимум 3 уровень для эволюции!")
    else:
        bot.reply_to(message, " Сначала создай покемона командой /go")

@bot.message_handler(commands=['rename'])
def rename(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        try:
            new_name = message.text.split(' ', 1)[1]
            if len(new_name) > 20:
                bot.reply_to(message, " Имя слишком длинное (макс. 20 символов)")
                return
            pokemon = Pokemon.pokemons[message.from_user.username]
            result = pokemon.rename(new_name)
            bot.send_message(message.chat.id, result)
        except IndexError:
            bot.reply_to(message, " Использование: /rename НовоеИмя")
    else:
        bot.reply_to(message, " Сначала создай покемона командой /go")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        attacker_username = message.from_user.username
        defender_username = message.reply_to_message.from_user.username
        
        if attacker_username == defender_username:
            bot.send_message(message.chat.id, " Нельзя атаковать самого себя!")
            return
            
        if attacker_username in Pokemon.pokemons.keys() and defender_username in Pokemon.pokemons.keys():
            attacker = Pokemon.pokemons[attacker_username]
            defender = Pokemon.pokemons[defender_username]
            
            
            if defender.hp <= 0:
                bot.send_message(message.chat.id, f" {defender.name} уже повержен и не может быть атакован!")
                return
                
            result = attacker.attack(defender)
            bot.send_message(message.chat.id, result)
            
       е
            if defender.hp <= 0:
                bot.send_message(message.chat.id, 
                               f"{defender.name} повержен! Используй /heal для восстановления.")
        else:
            bot.send_message(message.chat.id, "Оба игрока должны иметь покемонов для сражения")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, ответь на сообщение игрока командой /attack")

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Команды покемон-бота:\n"
        "/go - создать покемона (случайный тип)\n"
        "/info - информация о покемоне\n"
        "/train - тренировать покемона (+опыт)\n"
        "/heal - восстановить здоровье\n"
        "/attack - атаковать (ответь на сообщение игрока)\n"
        "/evolve - эволюционировать (требуется 3+ уровень)\n"
        "/rename - переименовать покемона\n"
        "\nТипы покемонов:\n"
        "Волшебник - магический щит, двойной урон\n"
        "Боец - повышенное HP, супер-удар\n"
        "Обычный - стандартные характеристики"
    )
    bot.send_message(message.chat.id, help_text)

if __name__ == "__main__":
    print("Запуск бота...")
    try:
        bot.infinity_polling()
        print("Бот успешно запущен")
    except Exception as e:
        print(f"Ошибка запуска: {e}")
