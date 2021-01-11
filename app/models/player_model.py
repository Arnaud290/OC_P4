"""player model module"""
from model import Model


class PlayerModel(Model):
    """Player model class"""
    def __init__(self, first_name, last_name, birth_date, sex, rank):
        self.id = self.get_number()
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.rank = rank
        self.tournament_points = 0.0
        self.tournament_list = []


player1 = PlayerModel('arnaud', 'manach', '03/09/1984', 'M', '2000')
player1.save()


player1.update('rank', '2500')

print(PlayerModel.get())