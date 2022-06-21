import numpy as np
from gym import spaces, Env

class BiasEnv(Env):
  def __init__(self):
    super(BiasEnv, self).__init__()

    # 0 -> state A
    # 1 -> state B
    self.state = 0
  def reset(self):

    self.state = 0
    return self.state

  def step(self, action):
    # 0 -> right
    # 1 -> left
    if action == 0 and self.state == 0:
      self.state = -1
      return self.state, 0, 1, {}
    elif action == 1 and self.state == 0:
      self.state = 1
      return self.state, 0, 0, {}
    elif self.state == 1:
      self.state = -1
      reward = np.random.normal(-0.1, 1)
      return self.state, reward, 1, {}
    else:
      raise Exception(f"Invalid action {action}")
