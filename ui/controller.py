from ui import screen
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow, QApplication)
import sys

from ui.driver import Driver


class Controller(QWidget):
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.driver = Driver()
        self.ui_screen = None
        self.setup_screen()
        self.setup_event_handlers()
        self.update_commands = {
            "p1_card": self.update_player_one_card,
            "p2_card": self.update_player_two_card,
            "textbox": self.update_textbox,
            "pot": self.update_pot,
            "actions": self.update_actions
        }

    def setup_screen(self):
        main_window = QMainWindow()
        self.ui_screen = screen.Ui_MainWindow()
        self.ui_screen.setupUi(main_window)
        main_window.show()
        sys.exit(self.application.exec_())

    def setup_event_handlers(self):
        self.ui_screen.take_action_button.cliked.connect(self.on_click)

    def play(self):
        while True:
            pass

    def update_player_one_card(self, value):
        pass

    def update_player_two_card(self, value):
        pass

    def update_textbox(self, value):
        pass

    def update_pot(self, value):
        pass

    def update_actions(self, actions):
        pass

    def on_click(self):
        print("Button clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Controller(app)
    game.play()
