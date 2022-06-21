import numpy as np

class DoubleQLearning:
  def __init__(self, alpha=0.1, epsilon=0.1, gamma=1):
    self.q1_values_a = np.zeros(2)
    self.q1_values_b = np.zeros(100)

    self.q2_values_a = np.zeros(2)
    self.q2_values_b = np.zeros(100)

    self.alpha = alpha
    self.epsilon = epsilon
    self.gamma = gamma


  def action(self, state):
    if np.random.rand() > self.epsilon:
      if state == 0:
        q_values_a = self.q1_values_a + self.q2_values_a
        idxs = np.argwhere(q_values_a == np.amax(q_values_a)).flatten()
        return np.random.choice(idxs)
      if state == 1:
        q_values_b = self.q1_values_b + self.q2_values_b
        idxs = np.argwhere(q_values_b == np.amax(q_values_b)).flatten()
        return np.random.choice(idxs)
    else:
      if state == 0:
        return np.random.randint(2)
      elif state == 1:
        return np.random.randint(100)

  def update(self, s, a, r, s_new):
    if np.random.rand() > 0.5:
      if s_new == 0:
        q_max = np.amax(self.q1_values_a)
      else:
        q_max = np.amax(self.q1_values_b)

      if s == 0:
        self.q1_values_a[a] = self.q1_values_a[a] + \
                            self.alpha * (r + self.gamma * q_max - self.q1_values_a[a])
      else:
        self.q1_values_b[a] = self.q1_values_b[a] + \
                            self.alpha * (r + self.gamma * q_max - self.q1_values_b[a])
    else:
      if s_new == 0:
        q_max = np.amax(self.q2_values_a)
      else:
        q_max = np.amax(self.q2_values_b)

      if s == 0:
        self.q2_values_a[a] = self.q2_values_a[a] + \
                            self.alpha * (r + self.gamma * q_max - self.q2_values_a[a])
      else:
        self.q2_values_b[a] = self.q2_values_b[a] + \
                            self.alpha * (r + self.gamma * q_max - self.q2_values_b[a])
