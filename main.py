import functions as functions
from env import *
import telebot

bot = telebot.TeleBot(api_token)

@bot.message_handler(commands=["start"])
def main(message):
    global players
    players=functions.load_players(message.chat.id)
    functions.show_players(players, message.chat.id)

@bot.message_handler(content_types=["text"])
def start_fight(message):
    players_1_2 = functions.pick_the_players(message, players)
    print(players_1_2[0])
    print(players_1_2[1])
    functions.fight(players_1_2[0], players_1_2[1], message.chat.id)
    functions.check_winner(players_1_2[0], players_1_2[1], message.chat.id)

bot.polling(True)