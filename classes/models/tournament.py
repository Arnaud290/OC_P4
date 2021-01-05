"""Tournament model module"""
import locale
locale.setlocale(locale.LC_TIME,'')
import time
import os
from .settings import NB_PLAYERS, NB_ROUNDS
from .save_loading_data import SaveLoadingData
from ..view import View


class Tournament:
    """Class for tournaments"""
    def __init__(self):
        self.id = SaveLoadingData.nb_tournaments() + 1
        self.name = ""
        self.location = ""
        self.date = time.strftime("%d/%m/%Y")
        self.rounds = NB_ROUNDS
        self.nb_tournament_players = NB_PLAYERS
        self.players = []
        self.time_control = ""
        self.description = ""
        self.nb_days = 1
        self.date_start_tournament = ''
        self.date_finish_tournament = ''
        self.in_progress = False

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def new_tournament(self):
        """Instance method that defines new tournament"""
        Tournament.clear()
        self.name = input("Tournament name : ")
        self.location = input("Tournament location : ")
        self.select_time_control()
        self.description = input("Tournament description : ")
        self.nb_rounds()
        self.nb_players()
        self.select_players()

    def select_time_control(self):
        """Instance method that defines the type of time control"""
        while True:
            time_position = input("Enter type of time (1 = bullet, 2 = blitz, 3 = rapid) : ")
            if time_position not in ('1', '2', '3'):
                continue
            else:
                if time_position == '1':
                    self.time_control = "bullet"
                    break
                elif time_position == '2':
                    self.time_control = "blitz"
                    break
                elif time_position == '3':
                    self.time_control = "rapid"
                    break

    def description(self, description):
        """Instance method that describes the tournament"""
        self.description = description

    def nb_rounds(self):
        while True:
            nb = input("WANT TO CHANGE NUMBERS OF ROUNDS? ACTUAL({}) : ".format(self.rounds))
            if nb:
                try:
                    nb = abs(int(nb))
                except ValueError:
                    input("The number must be valid. Press ENTER ...")
                    continue
                else:
                    if abs(nb) >= 1:
                        self.rounds = nb
                        break
                    else:
                        input("The number of rounds must be at least 1. Press ENTER ...")
                        continue
            else:
                break

    def nb_players(self):
        while True:
            nb = input("WANT TO CHANGE NUMBERS OF PLAYERS? ACTUAL({}) : ".format(self.nb_tournament_players))
            if nb:
                try:
                    nb = abs(int(nb))
                except ValueError:
                    input("The number must be valid. Press ENTER ...")
                    continue
                else:
                    if abs(nb) >= 2:
                        self.nb_tournament_players = nb
                        break
                    else:
                        input("The number of players must be at least 2. Press ENTER ...")
                        continue
            else:
                break

    def select_players(self):
        """Instance method that define list of players"""
        total_players = SaveLoadingData.load_player()
        Tournament_players = []
        for i in range(1, self.nb_tournament_players + 1):
            test = True
            while test:
                Tournament.clear()
                print("LIST OF ACTUALS PLAYERS\n")
                print(View.tab_view(total_players))
                print("\n\nTOURNAMENT PLAYERS LIST")
                if Tournament_players:
                    print(View.tab_view(Tournament_players))
                id_player = input("ENTER ID OF PLAYER {} : ".format(i))
                try:
                    int(id_player)
                except ValueError:
                    input("The number must be valid. Press ENTER ...")
                    continue
                else:
                    for element in total_players:
                        if element['id'] == int(id_player):
                            self.players.append(id_player)
                            Tournament_players.append(element)
                            total_players.remove(element)
                            test = False

    def start_tournament(self):
        self.date_start_tournament = time.strftime("%d/%m/%Y %H:%M:%S")
        self.in_progress = True

    def end_tournament(self):
        self.date_finish_tournament = time.strftime("%d/%m/%Y %H:%M:%S")
        self.in_progress = False

    def serialized_tournament(self):
        serialized_tournament = {
                        'id': self.id,
                        'name': self.name,
                        'location': self.location,
                        'date': self.date,
                        'nb_rounds': self.rounds,
                        'nb_players': self.nb_tournament_players,
                        'id_players': self.players,
                        'time_control': self.time_control,
                        'description': self.description,
                        'nb_days': self.nb_days,
                        'start_date': self.date_start_tournament,
                        'finish_date': self.date_finish_tournament,
                        'in_progress': self.in_progress
                        }
        return serialized_tournament

    def unserialized_tournament(self, tab_tournament):
        unserialized_tournament = tab_tournament[-1]
        self.id = unserialized_tournament['id']
        self.name =  unserialized_tournament['name']
        self.location = unserialized_tournament['location']
        self.date = unserialized_tournament['date']
        self.rounds = unserialized_tournament['nb_rounds']
        self.nb_tournament_players = unserialized_tournament['nb_players']
        self.players = unserialized_tournament['id_players']
        self.time_control = unserialized_tournament['time_control']
        self.nb_days = unserialized_tournament['nb_days']
        self.date_start_tournament = unserialized_tournament['start_date']
        self.date_finish_tournament = unserialized_tournament['finish_date']
        self.in_progress= unserialized_tournament['in_progress':]                
