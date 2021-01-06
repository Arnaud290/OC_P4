"""Player model module"""
from .save_loading_data import SaveLoadingData


class Player:
    """Class for players"""

    def __init__(self, id, id_tournament):
        self.id = id
        self.last_name = ""
        self.first_name = ""
        self.date_of_birth = ""
        self.sex = ""
        self.rank = 0
        self.weight = 0
        self.id_tournament = id_tournament

    def new_player(self):
        """player information instance method"""
        self.last_name = input("Enter player last name : ")
        self.first_name = input("Enter player first name : ")
        self.date_of_birth = input("Enter player birth date (format dd/mm/yyyy) : ")
        self.sex = input("enter player sex 'M' or 'F' : ")
        while True:
            try:
                rank = int(input("enter player rank : "))
            except ValueError:
                print("\nPlease enter valid number.")
                input("Press ENTER to continue...")
                continue
            else:
                self.rank = abs(rank)
                break

    def serialized_player(self):
        serialized_player = {
                            'id': self.id,
                            'last_name': self.last_name,
                            'first_name': self.first_name,
                            'date_of_birth': self.date_of_birth,
                            'sex': self.sex,
                            'rank': self.rank,
                            'id_tournament': self.id_tournament
                            }
        return serialized_player
    