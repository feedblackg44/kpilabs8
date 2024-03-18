import numpy as np


def is_strongly_connected(R):
    R_inv = np.transpose(R)
    return np.all(np.maximum(R, R_inv) == 1)


def is_weakly_connected(R):
    R_inv = np.transpose(R)
    return np.all(np.maximum(R, R_inv) > 0)


def check(R):
    if is_strongly_connected(R):
        return "Сильно зв'язнe"
    elif is_weakly_connected(R):
        return "Слабко зв'язне"
    else:
        return "Не зв'язне"
