"""Service module for rounds"""
from ..models.round_model import RoundModel
from . import tournament_service
from .get_model_service import GetModelService
from .table_service import TableService
from . import match_service
from ..views.view import View


class RoundService:
    """Class for round service"""

    @classmethod
    def round_table(cls, tournament, rounds):
        """method of creating round tables"""
        title_menu = "Tournament : {}".format(tournament.name)
        View.add_title_menu(title_menu)
        tab_t_players = []
        t_players = tournament_service.TournamentService.tournament_players_list(tournament)
        for player in t_players:
            tab_t_players.append(GetModelService.get_serialized('PlayerModel', player.id))
        TableService.table(
                            title="Tournament Players",
                            columns=['tournament_points', 'rank', 'first_name', 'last_name', 'number'],
                            table=tab_t_players
                        )
        TableService.table(
                            title="Round {}".format(rounds.count),
                            columns=['number', 'player1', 'score1', 'player2', 'score2'],
                            table=match_service.MatchService.match_table(rounds.matchs_list)
                        )

    @classmethod
    def create_rounds(cls, tournament):
        """round creation method"""
        rounds_nb = 1
        for nb_rounds in range(tournament.nb_rounds):
            round_game = RoundModel()
            round_game.id_tourament = tournament.id
            round_game.count = rounds_nb
            round_game.name = 'Round ' + str(rounds_nb)
            tournament.round_list.append(round_game.id)
            round_game.save()
            rounds_nb += 1
        tournament.in_progress = True
        tournament.update('in_progress', tournament.in_progress)
        tournament.update('round_list', tournament.round_list)
