import numpy as np
import pickle
import os
from numpy.core.fromnumeric import mean
from consts import *

class MonteCarloPrediction:
    def __init__(self, policy, gamma = 1.):
        self.policy = policy
        self.gamma = gamma
        self.states_no_ace = np.random.rand(100)
        self.states_ace = np.random.rand(100)
        # self.returns_no_ace = [[] for _ in range(100)]
        # self.returns_ace = [[] for _ in range(100)]
        self.count_no_ace = [0] * 100
        self.count_ace = [0] * 100


    def start_episode(self):
        self.episode = []
        self.last_state_action = None
        self.G = 0

    def step(self, state, reward, end_game):
        if self.last_state_action is not None:
            self.episode.append((*(self.last_state_action), reward))

        if not end_game:
            action = self.policy.action(state)
            self.last_state_action = (state, action)

            return action

    def update_states(self):

        for episode_num, episode_step in enumerate(self.episode[::-1]):
            self.G = self.gamma * self.G + episode_step[STEP['reward']]

            # Check if state not appeard on previous steps, since we are using first-visit
            state = episode_step[STEP['state']]
            all_states = [s[STEP['state']] for s in self.episode]

            #if state not in all_states[:-episode_num - 1] and state['player_sum'] >= 12:
            if state['player_sum'] >= 12:
                player_sum = state['player_sum'] - 12
                dealer_card = state['dealer_showing_card'] - 1

                index = 10 * player_sum + dealer_card

                if state['usable_ace']:
                    # self.returns_ace[index].append(self.G)
                    # self.states_ace[index] = mean(self.returns_ace[index])
                    self.count_ace[index] += 1
                    self.states_ace[index] = (self.states_ace[index] * (self.count_ace[index] - 1) + self.G) / self.count_ace[index]
                else:
                    # self.returns_no_ace[index].append(self.G)
                    # self.states_no_ace[index] = mean(self.returns_no_ace[index])
                    self.count_no_ace[index] += 1
                    self.states_no_ace[index] = (self.states_no_ace[index] * (self.count_no_ace[index] - 1) + self.G) / self.count_no_ace[index]

    def save(self, directory, experiment_name):
        with open(os.path.join(directory, experiment_name + '_states_ace.pkl'), 'wb') as f:
            pickle.dump(self.states_ace, f)

        with open(os.path.join(directory, experiment_name + '_states_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.states_no_ace, f)

        with open(os.path.join(directory, experiment_name + '_counts_ace.pkl'), 'wb') as f:
            pickle.dump(self.count_ace, f)

        with open(os.path.join(directory, experiment_name + '_counts_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.count_no_ace, f)

class MonteCarloES:
    def __init__(self, policy, gamma = 1.):
        self.policy = policy
        self.gamma = gamma
        self.q_no_ace = [0] * 100 * 2
        self.q_ace = [0] *100 * 2
        # self.returns_no_ace = [[] for _ in range(100)]
        # self.returns_ace = [[] for _ in range(100)]
        self.count_no_ace = [0] * 100 * 2
        self.count_ace = [0] * 100 * 2


    def start_episode(self):
        self.episode = []
        self.last_state_action = None
        self.G = 0

    def step(self, state, reward, end_game):
        # if it's not the first episode, append the step in memory
        if self.last_state_action is not None:
            self.episode.append((*(self.last_state_action), reward))

        if not end_game:
            # Alwayss hit when sum is less than 12
            if state['player_sum'] < 12:
                return ACTIONS['hit']

            if self.last_state_action is not None:
                action = self.policy.action(state)

            else:
                # if firts step select a random action for Exploring Start
                action = np.random.randint(2)

            self.last_state_action = (state, action)

            return action

        # self.update_states()

    def update_states(self):

        for episode_num, episode_step in enumerate(self.episode[::-1]):
            self.G = self.gamma * self.G + episode_step[STEP['reward']]

            # Check if state not appeard on previous steps, since we are using first-visit
            state_action = (episode_step[STEP['state']], episode_step[STEP['action']])
            all_states_action = [(s_a[STEP['state']], s_a[STEP['action']]) for s_a in self.episode]

            if state_action not in all_states_action[:-episode_num - 1] and state_action[0]['player_sum'] >= 12:
            # if state['player_sum'] >= 12:
                player_sum = state_action[0]['player_sum'] - 12
                dealer_card = state_action[0]['dealer_showing_card'] - 1

                index = 100 * state_action[1] + 10 * player_sum + dealer_card

                hit_index = 100 * 0 + 10 * player_sum + dealer_card
                stick_index = 100 * 1 + 10 * player_sum + dealer_card
                policy_index = 10 * player_sum + dealer_card

                if state_action[0]['usable_ace']:
                    # self.returns_ace[index].append(self.G)
                    # self.states_ace[index] = mean(self.returns_ace[index])
                    self.count_ace[index] += 1
                    # update of q value: q_new = (q_old * (n-1) + G) / n
                    self.q_ace[index] = (self.q_ace[index] * (self.count_ace[index] - 1) + self.G) / self.count_ace[index]

                    argmax_action = np.argmax([self.q_ace[hit_index], self.q_ace[stick_index]])
                    self.policy.update_state(policy_index, argmax_action, True)
                else:
                    # self.returns_no_ace[index].append(self.G)
                    # self.states_no_ace[index] = mean(self.returns_no_ace[index])
                    self.count_no_ace[index] += 1
                    self.q_no_ace[index] = (self.q_no_ace[index] * (self.count_no_ace[index] - 1) + self.G) / self.count_no_ace[index]

                    argmax_action = np.argmax([self.q_no_ace[hit_index], self.q_no_ace[stick_index]])
                    self.policy.update_state(policy_index, argmax_action, False)



    def save(self, directory, experiment_name):
        with open(os.path.join(directory, experiment_name + '_q_ace.pkl'), 'wb') as f:
            pickle.dump(self.q_ace, f)

        with open(os.path.join(directory, experiment_name + '_q_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.q_no_ace, f)


        with open(os.path.join(directory, experiment_name + '_counts_ace.pkl'), 'wb') as f:
            pickle.dump(self.count_ace, f)

        with open(os.path.join(directory, experiment_name + '_counts_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.count_no_ace, f)

        self.policy.save(directory, experiment_name)

class MonteCarloWithoutES:
    def __init__(self, policy, gamma = 1.):
        self.policy = policy
        self.gamma = gamma
        self.q_no_ace = [0] * 100 * 2
        self.q_ace = [0] *100 * 2
        # self.returns_no_ace = [[] for _ in range(100)]
        # self.returns_ace = [[] for _ in range(100)]
        self.count_no_ace = [0] * 100 * 2
        self.count_ace = [0] * 100 * 2


    def start_episode(self):
        self.episode = []
        self.last_state_action = None
        self.G = 0

    def step(self, state, reward, end_game):
        # if it's not the first episode, append the step in memory
        if self.last_state_action is not None:
            self.episode.append((*(self.last_state_action), reward))

        if not end_game:
            # Alwayss hit when sum is less than 12
            if state['player_sum'] < 12:
                return ACTIONS['hit']

            action = self.policy.action(state)

            self.last_state_action = (state, action)

            return action

        # self.update_states()

    def update_states(self):

        for episode_num, episode_step in enumerate(self.episode[::-1]):
            self.G = self.gamma * self.G + episode_step[STEP['reward']]

            # Check if state not appeard on previous steps, since we are using first-visit
            state_action = (episode_step[STEP['state']], episode_step[STEP['action']])
            all_states_action = [(s_a[STEP['state']], s_a[STEP['action']]) for s_a in self.episode]

            if state_action not in all_states_action[:-episode_num - 1] and state_action[0]['player_sum'] >= 12:
            # if state['player_sum'] >= 12:
                player_sum = state_action[0]['player_sum'] - 12
                dealer_card = state_action[0]['dealer_showing_card'] - 1

                index = 100 * state_action[1] + 10 * player_sum + dealer_card

                hit_index = 100 * 0 + 10 * player_sum + dealer_card
                stick_index = 100 * 1 + 10 * player_sum + dealer_card
                policy_index = 10 * player_sum + dealer_card

                if state_action[0]['usable_ace']:
                    # self.returns_ace[index].append(self.G)
                    # self.states_ace[index] = mean(self.returns_ace[index])
                    self.count_ace[index] += 1
                    # update of q value: q_new = (q_old * (n-1) + G) / n
                    self.q_ace[index] = (self.q_ace[index] * (self.count_ace[index] - 1) + self.G) / self.count_ace[index]

                    argmax_action = np.argmax([self.q_ace[hit_index], self.q_ace[stick_index]])
                    self.policy.update_state(policy_index, argmax_action, True)
                else:
                    # self.returns_no_ace[index].append(self.G)
                    # self.states_no_ace[index] = mean(self.returns_no_ace[index])
                    self.count_no_ace[index] += 1
                    self.q_no_ace[index] = (self.q_no_ace[index] * (self.count_no_ace[index] - 1) + self.G) / self.count_no_ace[index]

                    argmax_action = np.argmax([self.q_no_ace[hit_index], self.q_no_ace[stick_index]])
                    self.policy.update_state(policy_index, argmax_action, False)



    def save(self, directory, experiment_name):
        with open(os.path.join(directory, experiment_name + '_q_ace.pkl'), 'wb') as f:
            pickle.dump(self.q_ace, f)

        with open(os.path.join(directory, experiment_name + '_q_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.q_no_ace, f)


        with open(os.path.join(directory, experiment_name + '_counts_ace.pkl'), 'wb') as f:
            pickle.dump(self.count_ace, f)

        with open(os.path.join(directory, experiment_name + '_counts_no_ace.pkl'), 'wb') as f:
            pickle.dump(self.count_no_ace, f)

        self.policy.save(directory, experiment_name)
