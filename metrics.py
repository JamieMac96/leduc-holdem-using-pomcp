import strategy_evaluator

import matplotlib.pyplot as plt
import seaborn as sbn


class Metrics:
    def __init__(self, exploitability_interval=1000):
        self.exploitability_interval = exploitability_interval
        self.cumulative_reward = 0.0
        self.repeated_rewards = [[]]
        self.rewards = []
        self.avg_winnings = []
        self.exploitability_values = []
        sbn.set_style("darkgrid")

    def handle_exploitability(self, iteration, tree):
        if iteration % self.exploitability_interval == 0:
            value = strategy_evaluator.calculate_exploitability(tree)
            self.exploitability_values.append(-value)

    def calculate_avg_winnings_over_time(self, interval):
        for i in range(len(self.rewards)):
            if i % 1000 == 0 and i != 0:
                slope = (self.rewards[i] - self.rewards[i - interval]) / interval
                self.avg_winnings.append(slope)

    def show_exploitability(self):
        show_graph("Iterations", "Exploitability", self.exploitability_values)

    def show_cumulative_reward(self):
        show_graph("Iterations", "Cumulative Reward", self.rewards)

    def show_cumulative_reward_slope(self):
        self.calculate_avg_winnings_over_time(1000)
        show_graph("Iterations", "Avg. Winnings", self.avg_winnings)

    def reset(self):
        self.cumulative_reward = 0.0
        self.rewards = []
        self.avg_winnings = []


def show_graph(x_label, y_label, y_items, x_items=None):
    if x_items is None:
        x_items = list(zip(range(len(y_items))))
    plt.plot(x_items, y_items)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
