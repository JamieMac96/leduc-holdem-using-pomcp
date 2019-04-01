import strategy_evaluator
import persistance

import matplotlib.pyplot as plt
import seaborn as sbn

EXPLOITABILITY_MIN = 10000


# This class is used to calculate, store and display metrics recovered
# during the execution of the MCTS algorithm.
class Metrics:
    def __init__(self, exploitability_interval=1000):
        self.exploitability_interval = exploitability_interval
        self.cumulative_reward = 0.0
        self.rewards = []
        self.repeated_rewards = []
        self.avg_rewards_across_repetitions = []
        self.slope_of_rewards_graph = []
        self.exploitability_values = []
        self.repeated_exploitability_values = []
        self.avg_exploitability_across_repetitions = []
        sbn.set_style("darkgrid")

    def handle_exploitability(self, iteration, tree):
        if iteration >= EXPLOITABILITY_MIN and iteration % self.exploitability_interval == 0:
            print(iteration)
            value = strategy_evaluator.calculate_exploitability(persistance.get_deterministic_strategy(tree))
            self.exploitability_values.append(-value)

    def show_exploitability(self):
        self.calculate_avg_exploitability_across_repetitions()
        x_items = list()

        for i in range(len(self.avg_exploitability_across_repetitions)):
            x_items.append(i + (EXPLOITABILITY_MIN / self.exploitability_interval))
        show_graph("Iterations - Thousands", "Exploitability", self.avg_exploitability_across_repetitions, x_items)

    def show_cumulative_reward(self):
        self.calculate_avg_rewards_across_repetitions()
        show_graph("Iterations", "Cumulative Reward", self.avg_rewards_across_repetitions)

    def show_cumulative_reward_slope(self):
        self.calculate_slope_of_rewards_graph_over_time(1000)
        show_graph("Iterations - Thousands", "Avg. Winnings", self.slope_of_rewards_graph)

    def calculate_slope_of_rewards_graph_over_time(self, interval):
        for i in range(len(self.avg_rewards_across_repetitions)):
            if i % interval == 0 and i != 0:
                slope = (self.avg_rewards_across_repetitions[i] - self.avg_rewards_across_repetitions[i - interval]) / interval
                self.slope_of_rewards_graph.append(slope)

    def calculate_avg_rewards_across_repetitions(self):
        reward_sum = 0
        for i in range(len(self.rewards)):
            for reward in self.repeated_rewards:
                reward_sum += reward[i]
            self.avg_rewards_across_repetitions.append(reward_sum / len(self.repeated_rewards))
            reward_sum = 0

    def calculate_avg_exploitability_across_repetitions(self):
        exploitability_sum = 0
        for i in range(len(self.exploitability_values)):
            for exploitability in self.repeated_exploitability_values:
                exploitability_sum += exploitability[i]
            self.avg_exploitability_across_repetitions.append(exploitability_sum / len(self.repeated_exploitability_values))
            exploitability_sum = 0

    def reset(self):
        self.cumulative_reward = 0.0
        self.rewards = []
        self.slope_of_rewards_graph = []
        self.exploitability_values = []


def show_graph(x_label, y_label, y_items, x_items=None):
    if x_items is None:
        x_items = list(zip(range(len(y_items))))
    plt.plot(x_items, y_items)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
