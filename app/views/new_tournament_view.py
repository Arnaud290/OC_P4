"""new tournament module"""
from pandas import DataFrame
from .view import View


class NewTournamentView(View):
    """New tournament class"""

    def __init__(self):
        self.tab = None

    def request(self, question):
        """ask questions method"""
        print()
        print(question)
        print()
        choice = self.get_choice()
        return choice

    def tab_view(self, title, elements_list):
        """table view method"""
        print()
        print(title)
        print('_'*(len(title)))
        print()
        index = []
        for element in elements_list:
            index.append('')
        self.tab = DataFrame(elements_list, index=index, columns=['id', 'first_name', 'last_name', 'sex', 'rank'])
        if elements_list:
            print(self.tab)
        print()
        print()

    def indication(self, indication):
        """display indications method"""
        print()
        print(indication)

    def pause(self):
        """display pause method"""
        input("\nPress enter to continue")
