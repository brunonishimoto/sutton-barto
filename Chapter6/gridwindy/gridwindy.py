import numpy as np
from gym import spaces, Env

class GridWindBase(Env):
  def __init__(self, n_rows=7, n_cols=10, x_ini=0, y_ini=3, wind_strength=[0, 0, 0, 1, 1, 1, 2, 2, 1, 0], x_goal=7, y_goal=3):
    super(GridWindBase, self).__init__()

    self.action_space = spaces.Discrete(4)

    self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([n_cols - 1, n_rows - 1]), shape=(2,), dtype=np.int)

    assert len(wind_strength) == n_cols, "You need to inform the wind strength for all columns"


    self.n_rows = n_rows
    self.n_cols = n_cols
    self.x_ini = x_ini
    self.y_ini = y_ini
    self.x_pos = self.x_ini
    self.y_pos = self.y_ini
    self.x_goal = x_goal
    self.y_goal = y_goal
    self.wind_strength = wind_strength

  def reset(self):

    self.x_pos = self.x_ini
    self.y_pos = self.y_ini

    return np.array([self.x_pos, self.y_pos])

  def step(self, action):
    pass

  def render(self):
    print(' _' * 10)
    for y in range(self.n_rows):
      for x in range(self.n_cols):
        if x == self.x_pos and y == self.n_rows - self.y_pos - 1:
          print('|X', end='')
        elif x == self.x_goal and y == self.n_rows - self.y_goal - 1:
          print('|G', end='')
        else:
          print('|_', end='')
      print('|')

class GridWind4Actions(GridWindBase):
  def __init__(self, n_rows=7, n_cols=10, x_ini=0, y_ini=3, wind_strength=[0, 0, 0, 1, 1, 1, 2, 2, 1, 0], x_goal=7, y_goal=3):
    super(GridWind4Actions, self).__init__(n_rows, n_cols, x_ini, y_ini, wind_strength, x_goal, y_goal)

  def step(self, action):
    info = {}

    if action == 0: # right
      self.y_pos = min(self.y_pos + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 1: # up
      self.y_pos = min(self.y_pos + 1 + self.wind_strength[self.x_pos], self.n_rows - 1)
    elif action == 2: # left
      self.y_pos = min(self.y_pos + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 3: # down
      self.y_pos = max(min(self.y_pos -1 + self.wind_strength[self.x_pos], self.n_rows - 1), 0)
    else:
      raise Exception("Unrecognized error")

    if self.x_pos == self.x_goal and self.y_pos == self.y_goal:
      reward = 0
      done = True
    else:
      reward = -1
      done = False

    return np.array([self.x_pos, self.y_pos]), reward, done, info


class GridWind8Actions(GridWindBase):
  def __init__(self, n_rows=7, n_cols=10, x_ini=0, y_ini=3, wind_strength=[0, 0, 0, 1, 1, 1, 2, 2, 1, 0], x_goal=7, y_goal=3):
    super(GridWind8Actions, self).__init__(n_rows, n_cols, x_ini, y_ini, wind_strength, x_goal, y_goal)

  def step(self, action):
    info = {}

    if action == 0: # left
      self.y_pos = min(self.y_pos + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 1: # up
      self.y_pos = min(self.y_pos + 1 + self.wind_strength[self.x_pos], self.n_rows - 1)
    elif action == 2: # right
      self.y_pos = min(self.y_pos + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 3: # down
      self.y_pos = max(min(self.y_pos -1 + self.wind_strength[self.x_pos], self.n_rows - 1), 0)
    elif action == 4: # down-left
      self.y_pos = max(min(self.y_pos -1 + self.wind_strength[self.x_pos], self.n_rows - 1), 0)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 5: # left-up
      self.y_pos = min(self.y_pos + 1 + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 6: # up-right
      self.y_pos = min(self.y_pos + 1 + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 7: # right-down
      self.y_pos = max(min(self.y_pos -1 + self.wind_strength[self.x_pos], self.n_rows - 1), 0)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    else:
      raise Exception("Unrecognized error")

    if self.x_pos == self.x_goal and self.y_pos == self.y_goal:
      reward = 0
      end_episode = True
    else:
      reward = -1
      end_episode = False

    return (self.x_pos, self.y_pos), reward, end_episode, info



class GridWind9Actions(GridWindBase):
  def __init__(self, n_rows=7, n_cols=10, x_ini=0, y_ini=3, wind_strength=[0, 0, 0, 1, 1, 1, 2, 2, 1, 0], x_goal=7, y_goal=3):
    super(GridWind9Actions, self).__init__(n_rows, n_cols, x_ini, y_ini, wind_strength, x_goal, y_goal)

  def step(self, action):
    info = {}

    if action == 0: # left
      self.y_pos = min(self.y_pos + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 1: # up
      self.y_pos = min(self.y_pos + 1 + self.wind_strength[self.x_pos], self.n_rows - 1)
    elif action == 2: # right
      self.y_pos = min(self.y_pos + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 3: # down
      self.y_pos = max(min(self.y_pos -1 + self.wind_strength[self.x_pos], self.n_rows - 1), 0)
    elif action == 4: # down-left
      self.y_pos = max(min(self.y_pos -1 + self.wind_strength[self.x_pos], self.n_rows - 1), 0)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 5: # left-up
      self.y_pos = min(self.y_pos + 1 + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 6: # up-right
      self.y_pos = min(self.y_pos + 1 + self.wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 7: # right-down
      self.y_pos = max(min(self.y_pos -1 + self.wind_strength[self.x_pos], self.n_rows - 1), 0)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 8: # stay:
      self.y_pos = min(self.y_pos + self.wind_strength[self.x_pos], self.n_rows - 1)
    else:
      raise Exception("Unrecognized error")

    if self.x_pos == self.x_goal and self.y_pos == self.y_goal:
      reward = 0
      end_episode = True
    else:
      reward = -1
      end_episode = False

    return (self.x_pos, self.y_pos), reward, end_episode, info

class GridWind8ActionsStochastic(GridWindBase):
  def __init__(self, n_rows=7, n_cols=10, x_ini=0, y_ini=3, wind_strength=[0, 0, 0, 1, 1, 1, 2, 2, 1, 0], x_goal=7, y_goal=3):
    super(GridWind8ActionsStochastic, self).__init__(n_rows, n_cols, x_ini, y_ini, wind_strength, x_goal, y_goal)

  def step(self, action):
    stochastic = np.random.choice([-1, 0, 1])

    wind_strength = np.array(self.wind_strength) + stochastic

    info = {}

    if action == 0: # left
      self.y_pos = min(self.y_pos + wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 1: # up
      self.y_pos = min(self.y_pos + 1 + wind_strength[self.x_pos], self.n_rows - 1)
    elif action == 2: # right
      self.y_pos = min(self.y_pos + wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 3: # down
      self.y_pos = max(min(self.y_pos -1 + wind_strength[self.x_pos], self.n_rows - 1), 0)
    elif action == 4: # down-left
      self.y_pos = max(min(self.y_pos -1 + wind_strength[self.x_pos], self.n_rows - 1), 0)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 5: # left-up
      self.y_pos = min(self.y_pos + 1 + wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = max(self.x_pos - 1, 0)
    elif action == 6: # up-right
      self.y_pos = min(self.y_pos + 1 + wind_strength[self.x_pos], self.n_rows - 1)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    elif action == 7: # right-down
      self.y_pos = max(min(self.y_pos -1 + wind_strength[self.x_pos], self.n_rows - 1), 0)
      self.x_pos = min(self.x_pos + 1, self.n_cols - 1)
    else:
      raise Exception("Unrecognized error")

    if self.x_pos == self.x_goal and self.y_pos == self.y_goal:
      reward = 0
      end_episode = True
    else:
      reward = -1
      end_episode = False

    return (self.x_pos, self.y_pos), reward, end_episode, info
