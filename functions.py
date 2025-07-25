import random
import json
import os
import time

file_path = os.path.dirname(os.path.abspath(__file__))

def load_players():
    players = []
    json_file_names = [filename for filename in os.listdir(file_path + "/players") if filename.endswith('.json')]
    print(json_file_names)
    for player in json_file_names:
        with open (file_path + '/players/' + player, "r", encoding="utf-8") as file:
            players.append(json.load(file))
    print(players)
    return players
    
def show_players(players):
    n = 0
    print_text_gradually("Бойцы:")
    for player in players:
        n+=1
        print_text_gradually(str(n) + "." + player["name"])

def pick_the_players(players):
    choose_player_1 = input("Ввыбери бойца 1 ")
    choose_player_2 = input("Ввыбери бойца 2 ")
    player_1 = players[int(choose_player_1) - 1]
    player_2 = players[int(choose_player_2) - 1]
    print_text_gradually(player_1["name"] + " VS " + player_2["name"])
    print_text_gradually("Fight!")
    return [player_1, player_2]

def fight(attacker, defender):
        while is_finish(attacker, defender) == False:
            players_move(attacker, defender)
            if is_finish(attacker, defender) == True:
                break
            players_move(defender, attacker)

def is_finish(attacker, defender):
    if attacker["health"] <= 0 or defender["health"] <= 0:
        return True
    return False

def players_move(attacker, defender):
        print("---------------")
        full_attack = get_player_attack(attacker)
        print("+++++")
        full_defend = get_player_defend(defender)
        if full_attack > full_defend:
            damage = full_attack - full_defend
            defender["health"] -=damage
            print_text_gradually(defender["name"] + " получает " + str(damage) + " урона. Остаток здоровья:" + str(defender["health"]))
    
def get_lucky_chance_multiplier(player):
    with open(file_path + "/lucky_chance/lucky_chance.json", "r", encoding="utf-8") as file:
        lucky = json.load(file)
        file.close()
    lucky = random.choice(lucky)
    if lucky["name"] != "normal":
        lucky = random.choice(lucky["options"])
        print_text_gradually(player["name"] + " " + lucky["name"])
        return lucky["multiplier"]
    else:
        return 1

def get_player_attack(player):
    player_attack = random.choice(player["attack"])
    print_text_gradually(str(player["name"]) + " делает " + str(player_attack["name"]) + ". Урон " + str(player_attack["value"]))
    multiplier = get_lucky_chance_multiplier(player)
    if multiplier != 1:
        print_text_gradually("Коэффициент доп урона: " + str(multiplier))
    full_attack = int(player_attack["value"] * multiplier)
    if multiplier != 1:
        print_text_gradually("Общий урон " + str(full_attack))
    return full_attack

def get_player_defend(player):
    player_defend = random.choice(player["defend"])
    print_text_gradually(str(player["name"]) + " применяет " + str(player_defend["name"]) + ". Уровень защиты: " + str(player_defend["value"]))
    multiplier = get_lucky_chance_multiplier(player)
    if multiplier != 1:
        print_text_gradually("Коэффициент доп защиты: " + str(multiplier))
    full_defend = int(player_defend["value"] * multiplier)
    if multiplier != 1:
        print_text_gradually("Общая защита " + str(full_defend))
    return full_defend


def check_winner(player_1, player_2):
    if player_1["health"] <= 0:
        print_text_gradually(player_2['name'] + " IS WIN")
    else:
        print_text_gradually(player_1['name'] + " IS WIN")
    show_final_logo()        
    

def show_final_logo():
    time.sleep(3)
    with open(file_path + "/logo/fatality.txt", 'r') as file:
        content = file.read()
        print(content)

def print_text_gradually(text, delay=0.025):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()