"""Match list module"""
import operator
from .get_model_service import GetModelService


class MatchService:
    """Make match class"""

    @classmethod
    def match_list_tab(cls, match_list):
        """Create match list table method"""
        match_list_tab = []
        match_nb = 1
        for matchs in match_list:
                    player_1 = GetModelService.get_model('PlayerModel', matchs[0][0])
                    player_2 = GetModelService.get_model('PlayerModel', matchs[1][0])
                    match_list_tab.append(
                                    {
                                        'id': match_nb,
                                        'player1': player_1.first_name + ' ' + player_1.last_name,
                                        'score1': matchs[0][1],
                                        'player2': player_2.first_name + ' ' + player_2.last_name,
                                        'score2': matchs[1][1]
                                    }
                                    )
                    match_nb += 1
        return match_list_tab
    