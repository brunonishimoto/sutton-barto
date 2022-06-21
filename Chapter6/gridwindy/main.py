from gridwindy import GridWind4Actions, GridWind8Actions, GridWind9Actions, GridWind8ActionsStochastic
from sarsa import Sarsa
from argparse import ArgumentParser
import pickle as pkl

def create_grid(n_actions, stochastic):
  if n_actions == 4:
    return GridWind4Actions()
  elif n_actions == 8:
    if stochastic:
      return GridWind8ActionsStochastic()
    else:
      return GridWind8Actions()
  elif n_actions == 9:
    return GridWind9Actions()
  raise Exception("Invalid GridWorld")

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--num_actions", type=int, default=4, help="Number of possible actions")
  parser.add_argument("--stochastic", type=int, default=0, help="Wind strength stochastic or not")
  args = parser.parse_args()

  grid = create_grid(int(args.num_actions), int(args.stochastic))
  sarsa = Sarsa(n_actions=int(args.num_actions))

  n_steps = 15000
  num_episodes = 0


  s = (grid.x_pos, grid.y_pos)
  action = sarsa.action(s)

  eps_vs_steps = []

  for step in range(n_steps):
    # print(step)

    s_new, reward, end_game, _ = grid.step(action)
    grid.render()

    if end_game:
      num_episodes += 1
      print('-'*50)
      grid = create_grid(int(args.num_actions), int(args.stochastic))
      s = (grid.x_pos, grid.y_pos)
      action = sarsa.action(s)
      continue

    action_new = sarsa.action(s_new)

    sarsa.update(s, action, reward, s_new, action_new)

    action = action_new
    s = s_new

    eps_vs_steps.append((step, num_episodes))

# print(eps_vs_steps)
pkl.dump(eps_vs_steps, open(f'res_{args.num_actions}_actions_{args.stochastic}.pkl', 'wb'))
