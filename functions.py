import random
import json
import os
import time
import telebot
import time
from env import *

bot = telebot.TeleBot(api_token)
file_path = os.path.dirname(os.path.abspath(__file__))

def load_players(chat_id):
    global players
    players = []
    json_file_names = [filename for filename in os.listdir(file_path + "/players") if filename.endswith('.json')]
    bot.send_message(chat_id, json_file_names)
    for player in json_file_names:
        with open (file_path + '/players/' + player, "r", encoding="utf-8") as file:
            players.append(json.load(file))
    print(players)
    return players
    
def show_players(players, chat_id):
    n = 0
    bot.send_message(chat_id, "У вас есть на выбор такие персонажи как:")
    for player in players:
        n+=1
        bot.send_message(chat_id, str(n) + "." + player["name"])
    bot.send_message(chat_id, "Отправте мне 5 vs 2\n Прервое число это первый персонаж из списка\n А последнее это с кем он будет сражатся")

def pick_the_players(message, players):
    if message.text[0] in "1234567890" and message.text[len(message.text)-1] in "1234567890":
        player_1 = players[int(message.text[0]) - 1]
        player_2 = players[int(message.text[len(message.text)-1]) - 1]
        bot.send_message(message.chat.id ,player_1["name"] + " VS " + player_2["name"])
        bot.send_message(message.chat.id ,"Fight!")
        return(player_1, player_2)
    else:
        bot.send_message(message.chat.id, "Извините вы неправильно вели неправильно сообщение.\n Пример ввода: 4 vs 3 или 5 Vs 1, да даже так 5 VS 5")

def fight(attacker, defender, chat_id):
    while is_finish(attacker, defender) == False:
        players_move(attacker, defender, chat_id)
        if is_finish(attacker, defender) == True:
            break
        players_move(attacker, defender, chat_id)
        time.sleep(3)

def is_finish(attacker, defender):
    if attacker["health"] <= 0 or defender["health"] <= 0:
        return True
    else:
        return False

def players_move(attacker, defender, chat_id):
        bot.send_message(chat_id ,"---------------")
        full_attack = get_player_attack(attacker, chat_id)
        bot.send_message(chat_id ,"+++++")
        full_defend = get_player_defend(defender, chat_id)
        if full_attack > full_defend:
            damage = full_attack - full_defend
            defender["health"] -=damage
            bot.send_message(chat_id ,defender["name"] + " получает " + str(damage) + " урона. Остаток здоровья:" + str(defender["health"]))
    
def get_lucky_chance_multiplier(player, chat_id):
    with open(file_path + "/lucky_chance/lucky_chance.json", "r", encoding="utf-8") as file:
        lucky = json.load(file)
        file.close()
    lucky = random.choice(lucky)
    if lucky["name"] != "normal":
        lucky = random.choice(lucky["options"])
        bot.send_message(chat_id ,player["name"] + " " + lucky["name"])
        return lucky["multiplier"]
    else:
        return 1

def get_player_attack(player, chat_id):
    player_attack = random.choice(player["attack"])
    bot.send_message(chat_id ,str(player["name"]) + " делает " + str(player_attack["name"]) + ". Урон " + str(player_attack["value"]))
    multiplier = get_lucky_chance_multiplier(player, chat_id)
    if multiplier != 1:
        bot.send_message(chat_id ,"Коэффициент доп урона: " + str(multiplier))
    full_attack = int(player_attack["value"] * multiplier)
    if multiplier != 1:
        bot.send_message(chat_id ,"Общий урон " + str(full_attack))
    return full_attack

def get_player_defend(player, chat_id):
    player_defend = random.choice(player["defend"])
    bot.send_message(chat_id ,str(player["name"]) + " применяет " + str(player_defend["name"]) + ". Уровень защиты: " + str(player_defend["value"]))
    multiplier = get_lucky_chance_multiplier(player, chat_id)
    if multiplier != 1:
        bot.send_message(chat_id ,"Коэффициент доп защиты: " + str(multiplier))
    full_defend = int(player_defend["value"] * multiplier)
    if multiplier != 1:
        bot.send_message(chat_id ,"Общая защита " + str(full_defend))
    return full_defend


def check_winner(player_1, player_2, chat_id):
    bot.send_message(chat_id ,"-------------------")
    if player_1["health"] <= 0:
        bot.send_message(chat_id ,player_2['name'] + " IS WIN")
    else:
        bot.send_message(chat_id ,player_1['name'] + " IS WIN")
    show_final_logo(chat_id)        
    

def show_final_logo(chat_id):
    time.sleep(3)
    with open(file_path + "/logo/fatality.png", 'rb') as photo: # Открываем файл в бинарном режиме ('rb')!
        bot.send_photo(chat_id, photo)

#def print_text_gradually(text, delay=0.025):
#    for char in text:
#        print(char, end='', flush=True)
#        time.sleep(delay)
#    print()