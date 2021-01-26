"""Application controller module"""
from .main_menu_controller import MainMenuController
from ..views.view import View


class ApplicationController:
    """Application controller class"""
    def __init__(self):
        self.controller = MainMenuController()

    def start(self):
        """Method of launching modules"""
        while self.controller:
            self.controller = self.controller()
        View.quit()
