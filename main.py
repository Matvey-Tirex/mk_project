import functions as functions

players=functions.load_players()
functions.show_players(players)
players_1_2 = functions.pick_the_players(players)
functions.fight(players_1_2[0], players_1_2[1])
functions.check_winner(players_1_2[0], players_1_2[1])