"""match control module"""
from .controller import Controller
from .main_menu_control import ManagePlayerControl
from ..views.view import View
from ..models.player_model import PlayerModel
from ..models.match_model import MatchModel


class RoundsControl(Controller):
    """Rounds control class"""
    def __call__(self):
        self.select = ''
        self.actual_tournaments_list = self.tournaments_list()
        self.tournament = self.actual_tournaments_list[-1]
        self.rounds_model_list = self.rounds_list()
        self.t_rounds = []
        for round_model in self.rounds_model_list:
            if round_model.id in self.tournament.round_list:
                self.t_rounds.append(round_model)
        self.all_players_list = self.players_list()
        self.view = View()
        self.rounds_menu()
        self.control = None
        self.tab_matchs = []
            
    def rounds_menu(self):
        """Round menu method"""
        while True:
            self.t_players = []
            for player in self.all_players_list:
                if player.id in self.tournament.player_list:
                    self.t_players.append(player)
            title_menu = "Tournament : {}".format(self.tournament.name)
            self.view.add_title_menu(title_menu)
            tab_t_players = []
            for player in self.t_players:
                tab_t_players.append(PlayerModel.get_id_serialized(player.id))
            elements_columns = ['id', 'first_name', 'last_name','tournament_points' ,'rank']
            self.matchs_list = []
            self.rounds()
            self.view.tab_view("Tournament Players", tab_t_players, elements_columns) 
            self.all_matchs_list = self.matchs_list()
            for match in 



            self.view.add_menu_line("Finish Match ?")
            self.view.add_menu_line("Manage tournament informations")
            self.view.add_menu_line("Manage players tournament")
            self.view.add_menu_line("Quit")
            self.select = self.view.get_choice()
            if self.select not in ('1', '2', '3', '4'):
                continue
            if select == '1':
                pass
            if select == '2':
                pass
            if select == '3':
                pass
            if select == '4':
                break
    self.control = MainMenuControl()
    self.control()

    def rounds(self):
        for rounds in self.t_rounds:
            if not rounds.in_progress:
                if not rounds.matchs_list:
                    if rounds.count == '1'
                        self.t_players_list.sort(key=lambda x: x.rank, reverse=True)
                        match_nb = 1
                        for players in range(len(self.t_players)):
                            middle = int(len(self.t_players_list)/2)
                            match = MatchModel()
                            match.id_round = rounds.id
                            rounds.matchs_list.append(match.id)
                            rounds.update('matchs_list',rounds.matchs_list)
                            match.match_nb = match_nb
                            match.p1_id = self.t_players_list[0].id
                            match.p2_id = self.t_players_list[middle].id
                            match.save()
                            self.t_players_list[0].vs.append(match.p2_id)
                            self.t_players_list[0].update('vs', self.t_players_list[0].vs)
                            self.t_players_list[middle].play_with_list.append(match.p1_id)
                            self.t_players_list[middle].update('vs', self.t_players_list[middle].vs)
                            del self.t_players_list[0]
                            del self.t_players_list[int(len(self.t_players_list)/2)]
                            match_nb += 1
                            self.match_list.append(match)
                    else:
                        match_nb = 1
                        self.t_players_list.sort(key=lambda x: x.tournament_points, reverse=True)
                        for players in range(len(self.t_players)):
                            match = MatchModel()
                            match.id_round = rounds.id
                            rounds.update('matchs_list',rounds.matchs_list)
                            match.match_nb = match_nb
                            match.p1_id = self.t_players_list[0].id
                            for player in range(len(self.t_players)):
                                if match.p1_id not in self.t_players[player + 1].vs:
                                    match.p2_id = self.t_players[player + 1].id
                                    match.save()
                                    self.t_players_list[0].vs.append(match.p2_id)
                                    self.t_players_list[0].update('vs', self.t_players_list[0].vs)
                                    self.t_players_list[player + 1].play_with_list.append(match.p1_id)
                                    self.t_players_list[player + 1].update('vs', self.t_players_list[player + 1].vs)
                                    del self.t_players_list[0]
                                    del self.t_players_list[player + 1]
                                    break
                            match_nb += 1
                            match.save()
                            self.match_list.append(match)
                    rounds.in_progress = True
            else:
                all_matchs_list = self.matchs_list()
                for match in all_matchs_list:
                    if match.id in rounds.matchs_list:
                        self.match_list.append(match)
                break
                # list des match model du round


            























                
                