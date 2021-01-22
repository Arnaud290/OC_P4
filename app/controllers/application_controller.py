"""Application controller module"""
from .main_menu_controller import MainMenuController
from ..views.view import View


class ApplicationController:
    """Application controller class"""
    def __init__(self):
        self.controller = MainMenuController()
        self.view = View()

    def start(self):
        while self.controller:
            self.controller = self.controller()
        self.view.quit()
