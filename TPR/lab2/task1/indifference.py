import numpy as np


def get_indifference(R):
    return np.maximum(1 - np.maximum(R, R.T), np.minimum(R, R.T))
