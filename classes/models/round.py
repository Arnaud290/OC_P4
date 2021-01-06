"""round model module"""
import os
from .save_loading_data import SaveLoadingData
from .match import Match

class Round:
    """Class for Rounds"""
    def __init__(self, players, nb_rounds):
        self.players = players
        self.nb_round = nb_rounds
        self.group_a = []
        self.group_b = []
        self.match_list = []

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    def init_weight_players(self):
        self.players.sort(key=lambda x: x.rank, reverse=True)
        weight = len(self.players)
        for player in self.players:
            player.weight = weight
            weight -= 1

    def pairs(self):
        self.players.sort(key=lambda x: x.weight, reverse=True)
        for i in range(int(len(self.players)/2)):
           self.group_a.append(self.players[i])
        for i in range(int(len(self.players)/2), int(len(self.players))):
           self.group_b.append(self.players[i])
       
    def rounds(self):
        self.init_weight_players()
        for i in range(self.nb_round):
            self.match_list = []
            round_in_progress = True
            self.pairs()
            Round.clear()
            print("ROUND {} IN PROGRESS\n\n".format(i + 1))
            for j in range(int(len(self.players)/2)):
                match = Match(self.group_a[j], self.group_b[j])
                self.match_list.append(match)
            while round_in_progress:
                for j in range(int(len(self.players)/2)):
                    player1_name = self.match_list[j].player1.first_name + ' ' + self.match_list[j].player1.last_name
                    player2_name = self.match_list[j].player2.first_name + ' ' + self.match_list[j].player2.last_name
                    finish = str(self.match_list[j].end)
                    print("MATCH {} : {} VS {} FINISH : {} ".format((j + 1), player1_name, player2_name, finish))
                nb_match_finish = int(input("\n\nMATCH FINISH ? ENTER MATCH NUMBER : ")) - 1
                player1_name = self.match_list[nb_match_finish].player1.first_name + ' ' + self.match_list[nb_match_finish].player1.last_name
                player2_name = self.match_list[nb_match_finish].player2.first_name + ' ' + self.match_list[nb_match_finish].player2.last_name
                match_result = input("\n\nIF {} WIN ENTER 1, IF {} WIN ENTER 2, FOR NULL ENTER 0".format(player1_name, player2_name))
                self.match_list[nb_match_finish].end_match(match_result)
                for matchs in self.match_list:
                    if not matchs.end:
                        round_in_progress = True
                    else:
                        round_in_progress = False
