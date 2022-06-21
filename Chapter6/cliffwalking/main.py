from cliffwalking import CliffWalking4Actions
from sarsa import Sarsa
from q_learning import QLearning
from argparse import ArgumentParser
import pickle as pkl

def create_grid(n_actions):
  if n_actions == 4:
    return CliffWalking4Actions()
  raise Exception("Invalid GridWorld")

def create_alg(alg, n_actions):
  if alg == 'sarsa':
    return Sarsa(n_actions, epsilon=0)
  elif alg == 'q_learning':
    return QLearning(n_actions, epsilon=0)
  raise Exception("Invalid Algorithm")

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--num_actions", type=int, default=4, help="Number of possible actions")
  parser.add_argument("--alg", type=str, default='sarsa', help="Algorithm to use")
  args = parser.parse_args()


  for i in range(100):
    grid = create_grid(int(args.num_actions))
    alg = create_alg(args.alg, int(args.num_actions))

    n_episodes = 500
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
    pkl.dump(total_rewards, open(f'res/res_{args.num_actions}_actions_{args.alg}_{i}_greedy.pkl', 'wb'))
    pkl.dump(alg.q_values, open(f'res/q_values_{args.num_actions}_actions_{args.alg}_{i}_greedy.pkl', 'wb'))
