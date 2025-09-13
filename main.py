import telebot 
from config import token
from logic import Pokemon
import random

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def go (message):
    bot.reply_to(message, "Сначала создай покемона командой /go . Воспользуйя командой /help")

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

@bot.message_handler(commands=['train'])
def train(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.train()
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

@bot.message_handler(commands=['evolve'])
def evolve(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        if pokemon.level >= 5:
            result = pokemon.evolve()
            bot.send_message(message.chat.id, result)
            bot.send_photo(message.chat.id, pokemon.show_img())
        else:
            bot.reply_to(message, "Нужен как минимум 5 уровень для эволюции!")
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

@bot.message_handler(commands=['rename'])
def rename(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        try:
            new_name = message.text.split(' ', 1)[1]
            pokemon = Pokemon.pokemons[message.from_user.username]
            result = pokemon.rename(new_name)
            bot.send_message(message.chat.id, result)
        except IndexError:
            bot.reply_to(message, "Использование: /rename НовоеИмя")
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")



@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🎮 Команды покемон-бота:\n"
        "/go - создать покемона\n"
        "/info - информация о покемоне\n"
        "/train - тренировать покемона\n"
        "/battle - сразиться в битве\n"
        "/evolve - эволюционировать (требуется 5+ уровень)\n"
        "/rename - переименовать покемона\n"
    )
    bot.send_message(message.chat.id, help_text)

bot.infinity_polling(none_stop=True)
if __name__ == "__main__":
    print("Запуск бота...")
    try:
        bot.infinity_polling()
        print("Бот успешно запущен")
    except Exception as e:
        print(f"Ошибка запуска: {e}")
