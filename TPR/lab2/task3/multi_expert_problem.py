import numpy as np


def solve(data, to_print=True):
    matrixes = [expert["matrix"] for expert in data]
    w = [expert["w"] for expert in data]

    P = np.minimum.reduce(matrixes)
    Ps = np.maximum(P - P.T, 0)
    Pnd = np.min(1 - Ps.T, axis=1)
    if to_print:
        print(f"1. P = min(R1, R2, ..., Rn):\n{P}")
        print(f"2. Ps = P - P^-1 if P > P^-1 else 0:\n{Ps}")
        print(f"3. Pnd = min(1 - Ps^-1):\n{Pnd}")

    Q = np.sum([w[i] * matrixes[i] for i in range(len(matrixes))], axis=0)
    Qs = np.maximum(Q - Q.T, 0).round(2)
    Qnd = np.min(1 - Qs.T, axis=1)
    if to_print:
        print(f"4. Q = SUM(w[i] * R[i]):\n{Q}")
        print(f"5. Qs = Q - Q^-1 if Q > Q^-1 else 0:\n{Qs}")
        print(f"6. Qnd = min(1 - Qs^-1):\n{Qnd}")

    Und = np.minimum(Pnd, Qnd)
    if to_print:
        print(f"7. Und = min(Pnd, Qnd):\n{Und}")
    best = np.argmax(Und)

    return best

