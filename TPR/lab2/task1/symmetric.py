import numpy as np


def is_symmetric(R):
    return np.array_equal(R, R.T)


def is_antisymmetric(R):
    transposed_R = R.T
    violation_R = (R > 0) & (transposed_R > 0) & (R != transposed_R)
    return not violation_R.any()


def is_asymmetric(R):
    asymmetry_violation = (R * R.T) > 0
    np.fill_diagonal(asymmetry_violation, False)
    return not np.any(asymmetry_violation)


def check(R):
    if is_symmetric(R):
        return "Симетричне"
    elif is_antisymmetric(R):
        return "Антисиметричне"
    elif is_asymmetric(R):
        return "Асиметричне"
    else:
        return "Не симетричне, не антисиметричне, не асиметричне"
