"""new tournament module"""
from . import view


class NewTournamentView(view.View):
    """New tournament class"""
    def request(self, question):
        """ask questions"""
        print()
        print(question)
        print()
        choice = self.get_choice()
        return choice