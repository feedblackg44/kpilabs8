import numpy as np


def get_quasiequivalence(R):
    return np.minimum(R, R.T)
