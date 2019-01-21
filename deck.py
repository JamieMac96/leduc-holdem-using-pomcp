from poker import deck


class LeducCard(deck.Card):

    def __init__(self, rank, suit):
        super().__init__(rank, suit)
        self.suits = self.suits[2:4]
        self.ranks = self.ranks[10:]


class LeducDeck(deck.Deck):
    def __init__(self):
        super().__init__()
        self.init_deck()

    def init_deck(self):
        for i in range(2):
            for j in range(3):
                card = LeducCard(j, i)
                self.cards.append(card)

    def get_cards(self):
        return self.cards
