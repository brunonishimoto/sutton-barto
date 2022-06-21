import numpy as np
import pickle as pkl


if __name__ == "__main__":
    state_values_ace = pkl.load(open('./saves/states_ace.pkl', 'rb'))
    state_values_no_ace = pkl.load(open('./saves/states_no_ace.pkl', 'rb'))

    X, Y = np.meshgrid(range(10), range(10))
