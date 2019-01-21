from leduc.agent import Agent

# In Leduc hold’em, the deck consists of two suits
# with three cards in each suit. There are two rounds. In the
# first round a single private card is dealt to each player. In
# the second round a single board card is revealed. There is
# a two-bet maximum, with raise amounts of 2 and 4 in the
# first and second round, respectively. Both players start the
# first round with 1 already in the pot


ACTIONS=["FOLD", "CALL", "BET", "RAISE"]


class Game:
    def __init__(self, agent, opponent):
        self.agent = agent
        self.opponent = opponent
        self.round = 1
        self.num_bets_this_round = 0
        self.moves_record = list()
        self.current_pot = 0
        self.game_over = False

    def run(self):
        pass

    def get_possible_actions(self):
        if self.game_over:
            return []
        if self.num_bets_this_round == 0:
            return ["CALL", "BET"]
        elif self.num_bets_this_round == 1:
            return ["FOLD", "CALL", "RAISE"]
        elif self.num_bets_this_round == 2:
            return ["FOLD", "CALL"]

    def get_raise_amounts(self):
        if round == 1:
            return 2
        elif round == 2:
            return 4


if __name__ == "__main__":
    player = Agent()
    opponent = Agent()

    game = Game(player, opponent)
    game.run()
