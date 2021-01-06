"""match model module"""

class Match:
    """Class for matchs"""
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.end = False

    def end_match(self, result):
        if result == '1':
            self.player1.weight += 10
        if result == '2':
            self.player2.weight += 10
        if result == '0':
            self.player1.weight += 5
            self.player1.weight += 5
        self.end = True



