import numpy as np


def solve(R, to_print=True):
    Rs = np.maximum(R - R.T, 0)
    if to_print:
        print(f"1. Rs = R - R^-1 if R > R^-1 else 0:\n{Rs}")
    Rnd = np.min(1 - Rs.T, axis=1)
    if to_print:
        print(f"2. Rnd = min(1 - Rs^-1):\n{Rnd}")
    best = np.argmax(Rnd)
    return best
