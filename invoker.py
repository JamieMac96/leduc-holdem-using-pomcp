import mcts
import metrics
import util
import persistance

import time


class Invoker:
    def __init__(self, iterations, repetitions, time_limit=None):
        self.iterations = iterations
        self.repetitions = repetitions
        self.time_limit = time_limit
        self.m_metrics = metrics.Metrics()
        self.mcts_instance = mcts.Mcts(self.m_metrics)

    def invoke(self):
        for i in range(self.repetitions):
            self.m_metrics.reset()
            mcts.player_one_tree = {}
            mcts.player_two_tree = {}
            self.search("", iterations=self.iterations)
            self.m_metrics.repeated_rewards.append(self.m_metrics.rewards)
            self.m_metrics.repeated_exploitability_values.append(self.m_metrics.exploitability_values)

        util.print_tree(mcts.player_one_tree)
        self.m_metrics.show_cumulative_reward()
        self.m_metrics.show_cumulative_reward_slope()
        self.m_metrics.show_exploitability()
        # util.manual_traverse_tree(mcts.player_one_tree)

        # persistance.save_deterministic_strategy(mcts.player_one_tree, "Deterministic_" + str(self.iterations) + "_random.json")
        # persistance.save_stochastic_strategy(mcts.player_one_tree, "Stochastic_" + str(self.iterations) + "_random.json")
        persistance.save_deterministic_strategy(mcts.player_one_tree, "Deterministic_" + str(self.iterations) + "_self-play.json")
        persistance.save_stochastic_strategy(mcts.player_one_tree, "Stochastic_" + str(self.iterations) + "_self-play.json")

    def search(self, history, time_limit=None, iterations=None):
        if self.time_limit is not None:
            self.time_limit = time.time() + time_limit / 1000
            while time.time() < time_limit:
                self.mcts_instance.simulate(history)
        elif iterations is not None:
            for i in range(iterations):
                self.mcts_instance.simulate(history)
                self.m_metrics.handle_exploitability(i, mcts.player_one_tree)
        else:
            raise ValueError("You must specify a time or iterations limit")

if __name__ == "__main__":
    invoker = Invoker(300000, 1)
    invoker.invoke()
