"""View model module"""
from pandas import DataFrame


class View:
    """Class for players and tournaments views"""
    @staticmethod
    def tab_view(elements_list):
        index = []
        for element in elements_list:
            index.append('')
        tab = DataFrame(elements_list, index=index)
        return tab
