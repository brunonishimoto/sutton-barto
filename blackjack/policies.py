import numpy as np
import os
import pickle
from consts import ACTIONS

class DealerPolicy:

    def action(self, cards_sum):
        if cards_sum >= 17:
            return ACTIONS['stick']
        return ACTIONS['hit']

class PlayerPolicy1:
    # Sticks if the player's sum is 20 or 21

    def action(self, state):
        if state['player_sum'] >= 20:
            return ACTIONS['stick']
        return ACTIONS['hit']


class PlayerPolicy2:
    def __init__(self):
        # policy indicates the probability to hit (probability to stick = 1 - hit)
        # initial policy: stick when sum is 20 or 21 and hit otherwise
        self.policy_ace = [1 if i < 80 else 0 for i in range(100)]
        self.policy_no_ace = [1 if i < 80 else 0 for i in range(100)]

    def action(self, state):
        # if state['player_sum'] < 12:
        #     return ACTIONS['hit']
        index = 10 * (state['player_sum'] - 12) + (state['dealer_showing_card'] - 1)

        probability = self.policy_ace[index] if state['usable_ace'] else self.policy_no_ace[index]
        return self.sample_action(probability)

    def sample_action(self, probability):
        if np.random.rand() <= probability:
            return ACTIONS['hit']
        return ACTIONS['stick']


    def update_state(self, state, argmax_action, usable_ace):
        if usable_ace:
            self.policy_ace[state] = 1 - argmax_action
        else:
            self.policy_no_ace[state] = 1 - argmax_action

    def save(self, directory, experiment_name):
        with open(os.path.join(directory, experiment_name + '_policy_ace.pkl'), 'wb') as f:
            pickle.dump(self.policy_ace, f)

        with open(os.path.join(directory, experiment_name + '_policy_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.policy_no_ace, f)


class PlayerPolicyWithoutES:
    def __init__(self, epsilon=0.1):
        # policy indicates the probability to hit (probability to stick = 1 - hit)
        # initial policy: random policy
        self.policy_ace = [np.random.rand() for _ in range(100)]
        self.policy_no_ace = [np.random.rand() for _ in range(100)]

        self.epsilon = epsilon

    def action(self, state):
        # if state['player_sum'] < 12:
        #     return ACTIONS['hit']
        index = 10 * (state['player_sum'] - 12) + (state['dealer_showing_card'] - 1)

        probability = self.policy_ace[index] if state['usable_ace'] else self.policy_no_ace[index]
        return self.sample_action(probability)

    def sample_action(self, probability):
        if np.random.rand() <= probability:
            return ACTIONS['hit']
        return ACTIONS['stick']


    def update_state(self, state, argmax_action, usable_ace):
        if usable_ace:
            self.policy_ace[state] = (1 - argmax_action) * (1 - self.epsilon / 2) + (argmax_action) * (self.epsilon / 2)
        else:
            self.policy_no_ace[state] = (1 - argmax_action) * (1 - self.epsilon / 2) + (argmax_action) * (self.epsilon / 2)

    def save(self, directory, experiment_name):
        with open(os.path.join(directory, experiment_name + '_policy_ace.pkl'), 'wb') as f:
            pickle.dump(self.policy_ace, f)

        with open(os.path.join(directory, experiment_name + '_policy_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.policy_no_ace, f)
