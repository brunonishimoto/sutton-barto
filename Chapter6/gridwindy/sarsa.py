import numpy as np

class Sarsa:
  def __init__(self, n_rows=7, n_cols=10, n_actions=4, alpha=0.5, epsilon=0.1, gamma=1):
    self.q_values = np.zeros((n_cols, n_rows, n_actions))
    self.alpha = alpha
    self.epsilon = epsilon
    self.gamma = gamma


  def action(self, state):
    if np.random.rand() > self.epsilon:
      idxs = np.argwhere(self.q_values[state[0], state[1], :] == np.amax(self.q_values[state[0], state[1], :])).flatten()
      return np.random.choice(idxs)
    else:
      return np.random.randint(4)

  def update(self, s, a, r, s_new, a_new):
    self.q_values[s[0], s[1], a] = self.q_values[s[0], s[1], a] + \
                                   self.alpha * (r + self.gamma * self.q_values[s_new[0], s_new[1], a_new] - self.q_values[s[0], s[1], a])
