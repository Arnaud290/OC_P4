"""service module for matchs"""
import operator
import time
from .get_model_service import GetModelService
from .tournament_service import TournamentService


class MatchService:
    """class for match services"""

    @classmethod
    def match_table(cls, match_list):
        """method to create a table of matchs"""
        match_list_table = []
        match_nb = 1
        for matchs in match_list:
            player_1 = GetModelService.get_model('PlayerModel', matchs[0][0])
            player_2 = GetModelService.get_model('PlayerModel', matchs[1][0])
            match_list_table.append(
                                {
                                    'id': match_nb,
                                    'player1': str(player_1.id) + '_' + player_1.first_name + ' ' + player_1.last_name,
                                    'score1': matchs[0][1],
                                    'player2': str(player_2.id) + '_' + player_2.first_name + ' ' + player_2.last_name,
                                    'score2': matchs[1][1]
                                }
                                )
            match_nb += 1
        return match_list_table

    @classmethod
    def create_matchs(cls, tournament, rounds):
        """Method to create matches for a round"""
        p_match = TournamentService.tournament_players_list(tournament)
        t_players_id = GetModelService.get_models_id(p_match)
        p_match.sort(key=operator.attrgetter('tournament_points', 'rank'), reverse=True)
        for player in p_match:
            player.no_vs = []
            for id_player in t_players_id:
                if player.id != id_player and id_player not in player.vs:
                    player.no_vs.append(id_player)
            player.update('no_vs', player.no_vs)
        if rounds.count == 1:
            while p_match:
                middle = int(len(p_match)/2)
                player_1 = p_match[0]
                player_2 = p_match[middle]
                player_1.vs.append(player_2.id)
                player_1.update('vs', player_1.vs)
                player_2.vs.append(player_1.id)
                player_2.update('vs', player_2.vs)
                match = ([player_1.id, 0], [player_2.id, 0])
                rounds.matchs_list.append(match)
                del p_match[middle]
                del p_match[0]
            rounds.update('matchs_list', rounds.matchs_list)
        else:
            pos_player = 0
            while True:
                p_match.sort(key=operator.attrgetter('tournament_points', 'rank'), reverse=True)
                player_1 = p_match[pos_player]
                del p_match[pos_player]
                for player_model in p_match:
                    try:
                        if player_model.id == player_1.no_vs[pos_player]:
                            player_2 = player_model
                            p_match.remove(player_model)
                            break
                    except IndexError:
                        if player_model.id == player_1.no_vs[-1]:
                            player_2 = player_model
                            p_match.remove(player_model)
                            break
                player_1.vs.append(player_2.id)
                player_1.update('vs', player_1.vs)
                player_2.vs.append(player_1.id)
                player_2.update('vs', player_2.vs)
                match = ([player_1.id, 0], [player_2.id, 0])
                rounds.matchs_list.append(match)
                while p_match:
                    player_1 = p_match[0]
                    del p_match[0]
                    for player_model in p_match:
                        if player_model.id in player_1.no_vs:
                            player_2 = player_model
                            p_match.remove(player_model)
                            break
                    player_1.vs.append(player_2.id)
                    player_1.update('vs', player_1.vs)
                    player_2.vs.append(player_1.id)
                    player_2.update('vs', player_2.vs)
                    match = ([player_1.id, 0], [player_2.id, 0])
                    rounds.matchs_list.append(match)
                if len(rounds.matchs_list) > int(tournament.nb_players/2):
                    p_match = TournamentService.tournament_players_list(tournament)
                    for player in p_match:
                        while len(player.vs) >= rounds.count:
                            del player.vs[-1]
                            player.update('vs', player.vs)
                    rounds.matchs_list = []
                    rounds.update('matchs_list', rounds.matchs_list)
                    pos_player += 1
                    continue
                else:
                    rounds.update('matchs_list', rounds.matchs_list)
                    break

    @classmethod
    def management_match(cls, tournament, rounds, match_select, result_select):
        """Method of managing a match during results"""
        tournament_players = TournamentService.tournament_players_list(tournament)
        if result_select == '1':
            rounds.matchs_list[match_select][0][1] += 1
            for player in tournament_players:
                if player.id == rounds.matchs_list[match_select][0][0]:
                    player.tournament_points += 1
                    player.update('tournament_points', player.tournament_points)
        if result_select == '2':
            rounds.matchs_list[match_select][1][1] += 1
            for player in tournament_players:
                if player.id == rounds.matchs_list[match_select][1][0]:
                    player.tournament_points += 1
                    player.update('tournament_points', player.tournament_points)
        if result_select == '3':
            rounds.matchs_list[match_select][0][1] += 0.5
            rounds.matchs_list[match_select][1][1] += 0.5
            for player in tournament_players:
                if player.id == rounds.matchs_list[match_select][0][0]:
                    player.tournament_points += 0.5
                    player.update('tournament_points', player.tournament_points)
            for player in tournament_players:
                if player.id == rounds.matchs_list[match_select][1][0]:
                    player.tournament_points += 0.5
                    player.update('tournament_points', player.tournament_points)
        rounds.update('matchs_list', rounds.matchs_list)
        rounds.finish_matchs.append(match_select)
        rounds.update('finish_matchs', rounds.finish_matchs)
        if len(rounds.finish_matchs) == int(tournament.nb_players/2):
            rounds.start = False
            rounds.update('start', rounds.start)
            rounds.finish = True
            rounds.update('finish', rounds.finish)
            rounds.date_finish = time.strftime("%d/%m/%Y %H:%M:%S")
            rounds.update('date_finish', rounds.date_finish)
            tournament.tab_results = TournamentService.tournament_results_table(tournament)
            tournament.update('results', tournament.tab_results)
