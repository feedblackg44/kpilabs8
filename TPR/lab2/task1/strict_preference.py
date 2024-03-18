import numpy as np


def get_strict_preference(R):
    return np.maximum(R - R.T, 0)
