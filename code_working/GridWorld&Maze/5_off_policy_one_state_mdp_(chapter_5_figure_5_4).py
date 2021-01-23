# -*- coding: utf-8 -*-
"""5_off-policy_one-state_MDP (chapter 5 Figure 5.4).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x-KolCO7GdN84i7T3w5MSErtv_iO9tBN
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ACTION_BACK = 0
ACTION_END = 1

# behavior policy
def behavior_policy():
    return np.random.binomial(1, 0.5)

def play():
    # track the action for importance ratio
    trajectory = []
    while True:
        action = behavior_policy()
        trajectory.append(action)
        if action == ACTION_END:
            return 0, trajectory
        if np.random.binomial(1, 0.9) == 0:
            return 1, trajectory

np.random.binomial(1, 0.5)

if __name__ == '__main__':

    runs = 10
    episodes = 100000
    for run in range(runs):
        rewards = []
        for episode in range(0, episodes):
            reward, trajectory = play()
            if trajectory[-1] == ACTION_END:
                rho = 0
            else:
                rho = 1.0 / pow(0.5, len(trajectory))
            rewards.append(rho * reward)
        rewards = np.add.accumulate(rewards)
        estimations = np.asarray(rewards) / np.arange(1, episodes + 1)
        plt.plot(estimations)
    plt.xlabel('Episodes (log scale)')
    plt.ylabel('Ordinary Importance Sampling')
    plt.xscale('log')
    plt.show()
    #plt.savefig('../images/figure_5_4.png')
    plt.close()