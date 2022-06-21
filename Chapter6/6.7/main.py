from env import BiasEnv
from q_learning import QLearning
from double_q_learning import DoubleQLearning
from argparse import ArgumentParser
import pickle as pkl

if __name__ == "__main__":
  all_actions = []

  for i in range(10000):
    print(f'Run: {i}')
    env = BiasEnv()
    alg = DoubleQLearning()

    n_episodes = 300
    # num_episodes = 0
    action_taken = []
    for eps in range(n_episodes):
      # print(step)
      end_game = False
      s = env.reset()

      action = alg.action(s)
      if s == 0:
        action_taken.append(action)
      while not end_game:
        s_new, reward, end_game, _ = env.step(action)

        action_new = alg.action(s_new)
        if s_new == 0:
          action_taken.append(action_new)

        alg.update(s, action, reward, s_new)
        action = action_new
        s = s_new
        # grid.render()

      # print('-'*50)

    all_actions.append(action_taken)
    # num_actions_left.append(action_taken)

    # print(eps_vs_steps)
  pkl.dump(all_actions, open(f'res/all_actions_dq_learning.pkl', 'wb'))
  # pkl.dump(num_actions_left, open(f'res/num_actions_left.pkl', 'wb'))
