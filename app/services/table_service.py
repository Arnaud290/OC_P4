"""service module for the creation of tables"""
from ..views.view import View


class TableService:
    """class for make tables"""

    @classmethod
    def table(cls, title, columns, table, select_sort=None):
        """Method to create an array"""
        if not select_sort:
            select_sort = "Id order"
        if table:
            View.tab_view(title, cls._sort(table, select_sort), columns)

    @classmethod
    def _sort(cls, table, select_sort):
        """Private method for
        sorting lists for arrays"""
        if select_sort == "Number order":
            table = sorted(table, key=lambda x: x['number'], reverse=False)
        if select_sort == "Alphabetical order":
            table = sorted(table, key=lambda item: item.get('last_name'), reverse=False)
        if select_sort == "tournament_points":
            table = sorted(table, key=lambda x: (x['tournament_points'], x['rank']), reverse=True)
        if select_sort == "Rank order":
            table = sorted(table, key=lambda x: x['rank'], reverse=True)
        if select_sort == 'Round_name':
            table = sorted(table, key=lambda item: item.get('name'), reverse=False)
        return table

    @classmethod
    def table_sort_menu(cls, type_table, select_sort):
        """method for sorting
        menu lines of tables"""
        if type_table == 'player_table':
            if select_sort == "Number order":
                View.add_menu_line("Alphabetical order")
                return "Alphabetical order"
            if select_sort == "Alphabetical order":
                View.add_menu_line("rank order")
                return "Rank order"
            if select_sort == "Rank order":
                View.add_menu_line("Number order")
                return "Number order"
        if type_table == 'tournament_player_table':
            if select_sort == "Alphabetical order":
                View.add_menu_line("tournament points order")
            if select_sort == "Tournament points order":
                View.add_menu_line("Rank order")
            if select_sort == "Rank order":
                View.add_menu_line("Alphabetical order")

    @classmethod
    def table_sort_select(cls, type_table, select_sort):
        """Method that returns
        the sort mode for arrays"""
        if type_table == 'player_table':
            if select_sort == "Number order":
                return "Alphabetical order"
            if select_sort == "Alphabetical order":
                return "Rank order"
            if select_sort == "Rank order":
                return "Number order"
        if type_table == 'tournament_player_table':
            if select_sort == "Alphabetical order":
                return "Tournament points order"
            if select_sort == "Tournament points order":
                return "Rank order"
            if select_sort == "Rank order":
                return "Alphabetical order"
