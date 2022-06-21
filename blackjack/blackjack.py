import numpy as np
from consts import *
from policies import DealerPolicy

class Blackjack:
    def __init__(self):
        self.dealer = []
        self.player = []

        self.cards = range(1, 14)

        self.end_game = None
        self.reward = 0
        self.policy = DealerPolicy()

    def get_end_game(self):
        return self.end_game

    def start_game(self):
        self.player = [min(10, x) for x in np.random.choice(self.cards, size=2, replace=True)]
        self.dealer = [min(10, x) for x in np.random.choice(self.cards, size=2, replace=True)]

        assert self.get_sum(PLAYER['player']) <= 21
        assert self.get_sum(PLAYER['dealer']) <= 21


        self.end_game = False
        self.reward = 0

        # If natural (sum 21 in first hand) the game ends, with a WIN if the dealer does not have a natural,
        # DRAW otherwise

        # if self.get_sum(PLAYER['player']) == 21:
        #     self.end_game = True

        #     if self.get_sum(PLAYER['dealer']) == 21:
        #         self.reward = REWARD['draw']
        #     else:
        #         self.reward = REWARD['win']

        return self.get_state()

    def get_state(self):
        self.state = {'player_sum': self.get_sum(PLAYER['player']),
                        'dealer_showing_card': self.get_dealer_showing_card(),
                        'usable_ace': self.get_usable_ace()}

        return self.state

    def get_sum(self, player):
        if player == PLAYER['dealer']:
            return self.get_hand_sum(self.dealer)
        elif player == PLAYER['player']:
            return self.get_hand_sum(self.player)
        else:
            ValueError("Undefined player. It must be 'dealer' or 'player'")

    def get_hand_sum(self, hand):
        hand_sum = sum(hand)

        if 1 in hand and hand_sum < 12:
            # If we have usable ace
            return sum(hand) + 10

        return hand_sum

    def get_dealer_showing_card(self):
        return self.dealer[0]

    def get_usable_ace(self):
        hand_sum = sum(self.player)

        if 1 in self.player and hand_sum < 12:
            return True

        return False

    def action(self, action):
        if action == ACTIONS['hit']:
            self.hit_card(PLAYER['player'])

            if self.get_bust(PLAYER['player']):
                self.end_game = True
                self.reward = REWARD['lose']

        elif action == ACTIONS['stick']:
            self.turn = PLAYER['dealer']
            self.dealer_play()

        else:
            ValueError("Invalid action. It must be 'hit' or 'stick'")

        return self.get_state(), self.reward, self.end_game

    def dealer_play(self):
        while not self.end_game:
            action = self.policy.action(self.get_sum(PLAYER['dealer']))

            if action == ACTIONS['hit']:
                self.hit_card(PLAYER['dealer'])

                if self.get_bust(PLAYER['dealer']):
                    self.end_game = True
                    self.reward = REWARD['win']
            elif action == ACTIONS['stick']:
                self.end_game = True
                self.reward = self.get_reward()

    def get_reward(self):
        if self.get_sum(PLAYER['player']) > self.get_sum(PLAYER['dealer']):
            return REWARD['win']
        elif self.get_sum(PLAYER['player']) < self.get_sum(PLAYER['dealer']):
            return REWARD['lose']
        else:
            return REWARD['draw']

    def hit_card(self, player):
        if player == PLAYER['dealer']:
            self.dealer.append(min(10, np.random.choice(self.cards)))
        elif player == PLAYER['player']:
            self.player.append(min(10, np.random.choice(self.cards)))
        else:
            ValueError("Undefined player. It must be 'dealer' or 'player'")

    def get_bust(self, player):
        return self.get_sum(player) > 21
