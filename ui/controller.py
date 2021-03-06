from ui import screen
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication)
import sys

from ui.game_model import Model

BUTTON_ACTIONS_BY_INDEX = {
    0: "f",
    1: "c",
    2: "b",
    3: "r"
}


# This class uses the game model in order to retrieve the
# relevant game information and update the UI screen
class Controller(QWidget):
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.model = Model()
        self.main_window = QMainWindow()
        self.ui_screen = None
        self.setup_screen()
        self.setup_event_handlers()
        self.radio_buttons = self.get_radio_buttons()
        self.update_commands = {
            "p1_card": self.update_player_one_card,
            "p2_card": self.update_player_two_card,
            "textbox": self.update_textbox,
            "public": self.show_public_card,
            "pot": self.update_pot,
            "actions": self.update_actions,
            "winnings": self.update_total_winnings
        }
        self.update_ui()
        self.show_screen()

    def setup_screen(self):
        self.ui_screen = screen.Ui_MainWindow()
        self.ui_screen.setupUi(self.main_window)

    def show_screen(self):
        self.main_window.show()
        sys.exit(self.application.exec_())

    def setup_event_handlers(self):
        self.ui_screen.take_action_button.clicked.connect(self.take_action)
        self.ui_screen.new_game_button.clicked.connect(self.new_game)

    def get_radio_buttons(self):
        return [self.ui_screen.fold_radio, self.ui_screen.call_radio,
                self.ui_screen.bet_radio, self.ui_screen.raise_radio]

    def update_ui(self):
        for key, value in self.model.get_game_state().items():
            self.update_commands[key](value)

    def update_player_one_card(self, value):
        update_card(self.ui_screen.player_card, value)

    def update_player_two_card(self, value):
        update_card(self.ui_screen.opponent_card, value)

    def show_public_card(self, value):
        update_card(self.ui_screen.public_card, value)

    def update_textbox(self, value):
        self.ui_screen.textbox.setText(value)

    def update_pot(self, value):
        self.ui_screen.pot.setText(str(value))

    def update_total_winnings(self, value):
        self.ui_screen.total_winnings.setText("Total Winnings: " + str(value))

    def update_actions(self, actions):
        for i in range(len(self.radio_buttons)):
            if BUTTON_ACTIONS_BY_INDEX[i] in actions:
                self.radio_buttons[i].show()
            else:
                self.radio_buttons[i].hide()

    def take_action(self):
        for i in range(len(self.radio_buttons)):
            if self.radio_buttons[i].isChecked():
                self.model.update_game_state(BUTTON_ACTIONS_BY_INDEX[i], -1)

        self.update_ui()

    def new_game(self):
        self.model.reset()
        self.update_ui()


def update_card(card, value):
    if value == "":
        card.setText("")
        return

    start = "<html><head/><body><p><img src=\""
    source = ":/my_cards/" + value
    end = "\"/></p></body></html>"
    card.setText(start + source + end)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Controller(app)

