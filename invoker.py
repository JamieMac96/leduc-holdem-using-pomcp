import strategy_evaluator
import mcts
import metrics
import util

import time


class Invoker:
    def __init__(self, iterations, repetitions, time_limit=None):
        self.iterations = iterations
        self.repetitions = repetitions
        self.time_limit = time_limit
        self.m_metrics = metrics.Metrics()

    def invoke(self):
        for i in range(self.repetitions):
            self.m_metrics.reset()
            self.search("", iterations=self.iterations)
            self.m_metrics.repeated_rewards.append(self.m_metrics.rewards)

        util.print_tree(mcts.player_one_tree)

    def search(self, history, time_limit=None, iterations=None):
        if self.time_limit is not None:
            self.time_limit = time.time() + time_limit / 1000
            while time.time() < time_limit:
                mcts.simulate(history)
        elif iterations is not None:
            for i in range(iterations):
                mcts.simulate(history)
                self.m_metrics.handle_exploitability(i, mcts.player_one_tree)
        else:
            raise ValueError("You must specify a time or iterations limit")

if __name__ == "__main__":
    invoker = Invoker(10000, 1)
    invoker.invoke()