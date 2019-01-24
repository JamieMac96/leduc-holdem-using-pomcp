from pycfr.card import Card
from poker.deck import Deck


class LeducDeck(Deck):
    def __init__(self):
        super().__init__()
        self.init_deck()

    def init_deck(self):
        for i in range(2):
            for j in range(3):
                card = Card(j, i)
                self.cards.append(card)

    def get_cards(self):
        return self.cards
