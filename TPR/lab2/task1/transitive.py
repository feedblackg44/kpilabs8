import numpy as np


def is_transitive(R):
    composition = np.maximum.outer(R, R)
    return np.all(composition <= R)


def check(R):
    if is_transitive(R):
        return "Транзитивне"
    else:
        return "Не транзитивне"
