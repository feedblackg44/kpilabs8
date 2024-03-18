import numpy as np


def is_reflexive(R):
    return np.all(np.diag(R) == 1)


def is_strongly_reflexive(R):
    if not is_reflexive(R):
        return False
    R_copy = R.copy()
    np.fill_diagonal(R_copy, 0)
    return np.all(R_copy < 1)


def is_weakly_reflexive(R):
    diagonal_elements = np.diag(R)
    diagonal_matrix = np.tile(diagonal_elements, (R.shape[0], 1))
    return np.all(R <= diagonal_matrix)


def check(R):
    if is_reflexive(R):
        return "Рефлексивне"
    elif is_strongly_reflexive(R):
        return "Сильно рефлексивне"
    elif is_weakly_reflexive(R):
        return "Слабко рефлексивне"
    else:
        return "Не рефлексивне"
