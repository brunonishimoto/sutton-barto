# Arquivo para experimento comparando expeted sarsa, sarsa e q-learning

from cliffwalking import CliffWalking4Actions
from sarsa import Sarsa
from q_learning import QLearning
from expected_sarsa import ExpectedSarsa
from argparse import ArgumentParser
import pickle as pkl
import numpy as np

def create_grid(n_actions):
  if n_actions == 4:
    return CliffWalking4Actions()
  raise Exception("Invalid GridWorld")

def create_alg(alg, n_actions, alpha=0.5):
  if alg == 'sarsa':
    return Sarsa(n_actions, epsilon=0.1, alpha=alpha)
  elif alg == 'q_learning':
    return QLearning(n_actions, epsilon=0.1, alpha=alpha)
  elif alg == 'expected_sarsa':
    return ExpectedSarsa(n_actions, epsilon=0.1, alpha=alpha)
  raise Exception("Invalid Algorithm")

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--num_actions", type=int, default=4, help="Number of possible actions")
  parser.add_argument("--alg", type=str, default='sarsa', help="Algorithm to use")
  args = parser.parse_args()


  for alpha in np.linspace(0.1, 1, 10):
    print(alpha)
    for i in range(50000):
      grid = create_grid(int(args.num_actions))
      alg = create_alg(args.alg, int(args.num_actions), alpha)

      n_episodes = 100000
      # num_episodes = 0
      total_rewards = []
      for eps in range(n_episodes):
        # print(step)
        end_game = False
        s = grid.reset()
        eps_reward = []

        action = alg.action(s)
        while not end_game:
          s_new, reward, end_game, _ = grid.step(action)
          eps_reward.append(reward)

          action_new = alg.action(s_new)

          alg.update(s, action, reward, s_new, action_new)
          action = action_new
          s = s_new
          # grid.render()

        total_rewards.append(sum(eps_reward))
        # print('-'*50)

      # print(eps_vs_steps)
      pkl.dump(total_rewards, open(f'res/expected_sarsa/res_{args.num_actions}_actions_{args.alg}_{alpha}_{i}.pkl', 'wb'))
      pkl.dump(alg.q_values, open(f'res/expected_sarsa/q_values_{args.num_actions}_actions_{args.alg}_{alpha}_{i}.pkl', 'wb'))
