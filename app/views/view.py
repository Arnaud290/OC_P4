"""base view module"""
import os


class View:
    """General view class"""
    def __init__(self):
        self.choice = ''

    def get_choice(self):
        """user get choice method"""
        self.choice = input(">> ")
        return self.choice

    @staticmethod
    def clear():
        """clear screen method"""
        os.system('cls' if os.name == 'nt' else 'clear')
