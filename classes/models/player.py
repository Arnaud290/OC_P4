"""Player model module"""


class Player:
    """Class for players"""

    def __init__(self):
        self.last_name = ""
        self.first_name = ""
        self.date_of_birth = ""
        self.sex = ""
        self.rank = 0
        Player.player_info()

    def player_info(self):
        """player information instance method"""
        self.last_name = input("Enter player last name : ")
        self.first_name = input("Enter player first name : ")
        self.date_of_birth = input("Enter player birth date (format dd/mm/yyyy) : ")
        self.sex = input("enter player sex 'M' or 'F' : ")
        self.rank = input("enter player rank :")
