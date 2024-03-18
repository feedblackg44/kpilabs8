import numpy as np


def is_antireflexive(R):
    return np.all(np.diag(R) == 0)


def is_strong_antireflexive(R):
    if not is_antireflexive(R):
        return False
    R_copy = R.copy()
    np.fill_diagonal(R_copy, 1)
    return np.all(R_copy > 0)


def is_weak_antireflexive(R):
    diagonal_elements = np.diag(R)
    diagonal_matrix = np.tile(diagonal_elements, (R.shape[0], 1))
    return np.all(R >= diagonal_matrix)


def check(R):
    if is_antireflexive(R):
        return "Антирефлексивне"
    elif is_strong_antireflexive(R):
        return "Сильно антирефлексивне"
    elif is_weak_antireflexive(R):
        return "Слабко антирефлексивне"
    else:
        return "Не антирефлексивне"
