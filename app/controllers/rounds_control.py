"""match control module"""
from .controller import Controller
from ..views.view import View
from ..models.player_model import PlayerModel
from ..models.match_model import MatchModel


class RoundsControl(Controller):
    """Rounds control class"""
    def __call__(self):
        self.actual_tournaments_list = self.tournaments_list()
        self.tournament = self.actual_tournaments_list[-1]
        self.rounds_model_list = self.rounds_list()
        self.tournament_rounds_list = []
        for round_model in self.rounds_model_list:
            if round_model.id in self.tournament.round_list:
                self.tournament_rounds_list.append(round_model)
        self.all_players_list = self.players_list()
        self.all_match_list = self.matchs_list()
        self.view = View()
        self.rounds_menu()
            
    def rounds_menu(self):
        """Round menu method"""
        nb_round = 0
        while nb_round < self.tournament.nb_rounds:
            round_model = self.tournament_rounds_list[nb_round]
            if round_model.end:
                nb_round += 1
                continue
            matchs_list = []
            for match in self.all_match_list:
                if match.id in round_model.matchs_list:
                    matchs_list.append(match)
            t_players_list = []
            for player in self.all_players_list:
                if player.id in self.tournament.player_list:
                    t_players_list.append(player)
            title_menu = "Tournament : {}".format(self.tournament.name)
            self.view.add_title_menu(title_menu)
            tab_tournament_players = []
            for player in t_players_list:
                tab_tournament_players.append(PlayerModel.get_id_serialized(player.id))
            elements_columns = ['id', 'first_name', 'last_name','tournament_points' ,'rank']
            self.view.tab_view("Tournament Players", tab_tournament_players, elements_columns) 
            self.view.indication("Round {}".format(nb_round + 1))
            if nb_round == 0:
                t_players_list.sort(key=lambda x: x.rank, reverse=True)
            else:
                t_players_list.sort(key=lambda x: x.tournament_points, reverse=True)
            if not matchs_list:    
                match_list_id = []
                for matchs in range(int(self.tournament.nb_players/2)):
                    match = MatchModel()
                    matchs_list.append(match)   
                    match_list_id.append(match.id)
                    match.player1_id = t_players_list[0].id
                    match.player1_name = (t_players_list[0].first_name + ' ' + t_players_list[0].last_name)
                    for player in range(len(t_players_list)):
                        if match.player1_id not in t_players_list[player].play_with_list:
                            match.player2_id = t_players_list[player].id
                            match.player2_name = (
                                                    t_players_list[player].first_name +
                                                    ' '+ t_players_list[player].last_name
                                                )
                            t_players_list[0].play_with_list.append(match.player2_id)
                            t_players_list[0].update('play_with_list', t_players_list[0].play_with_list)
                            t_players_list[player].play_with_list.append(match.player1_id)
                            t_players_list[player].update('play_with_list', t_players_list[player].play_with_list)
                            break
                    match.save()
            matchs_list_tab = []
            nb_match = 1
            for match in matchs_list:
                print(MatchModel.get_id_serialized(match.id))
                 #matchs_list_tab.append({'nb' : nb_match} + MatchModel.get_id_serialized(match.id))
                nb_match += 1
            elements_columns = ['nb', 'player1_name', 'player2_name' , 'result']
            self.view.tab_view("Matchs", matchs_list_tab, elements_columns)
            self.view.pause()