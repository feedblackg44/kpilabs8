import re
import numpy as np


def try_parse_float(value):
    try:
        return float(value)
    except ValueError:
        return value


def read_bad_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read()

    data = re.split('_+', data)
    for i in range(len(data)):
        data[i] = re.split(r"МПП.*?\n", data[i])
        data[i] = list(filter(None, data[i]))
        for j in range(len(data[i])):
            data[i][j] = re.split(r'\n', data[i][j])
            data[i][j] = list(filter(None, data[i][j]))
            for k in range(len(data[i][j])):
                data[i][j][k] = re.split(r' ', data[i][j][k])
                data[i][j][k] = np.array([try_parse_float(x) for x in data[i][j][k]
                                          if isinstance(try_parse_float(x), (float, int))])
            data[i][j] = np.array(data[i][j])

    experts, criteria, alterntives = data[0].pop(0)[0]
    mpp_experts = data[0].pop(0)
    data.pop(0)
    experts_criteria = [data[i].pop(0) for i in range(len(data))]
    experts_alternatives = data

    return experts, criteria, alterntives, mpp_experts, experts_criteria, experts_alternatives


def calc_lambda_max(matrix, tol=1e-10, max_iterations=1000, print_iterations=False):
    x = np.ones(matrix.shape[0])

    lambda_max = 0
    for i in range(1, max_iterations + 1):
        x_next = np.dot(matrix, x)
        lambda_max_new = np.max(x_next / x)
        if print_iterations:
            print(f"{i}: x^m = {x}, x^(m+1) = {x_next}, λ_max = {lambda_max_new}")
        if np.abs(lambda_max - lambda_max_new) < tol:
            break
        lambda_max = lambda_max_new
        x = x_next / np.linalg.norm(x_next)

    return lambda_max


def calculate_CI(lambda_max, n):
    return round((lambda_max - n) / (n - 1), 5)


def calculate_CR(CI, n):
    CIS_dict = {
        1: 0.00,
        2: 0.00,
        3: 0.58,
        4: 0.90,
        5: 1.12,
        6: 1.24,
        7: 1.32,
        8: 1.41,
        9: 1.45,
        10: 1.49
    }

    return round(CI / CIS_dict[n], 5)


def calculate_weights(matrix):
    v = np.prod(matrix, axis=1) ** (1 / matrix.shape[0])
    return v / np.sum(v)


def correct_matrix(matrix, tol=1e-10):
    weights = calculate_weights(matrix)
    normalized_weights = weights / np.sum(weights)
    w = np.outer(normalized_weights, normalized_weights)
    matrix_delta = np.abs(matrix - w)
    i, j = np.unravel_index(np.argmax(matrix_delta), matrix_delta.shape)
    if matrix_delta[i, j] < tol:
        return matrix
    else:
        matrix[i, j] = normalized_weights[i] / normalized_weights[j]
        matrix[j, i] = 1 / matrix[i, j]
        return correct_matrix(matrix)


def check_matrix(matrix, print_iterations=False, interval=''):
    t = matrix.shape[0]

    valid_matrix = False
    k_weights = None
    while not valid_matrix:
        valid_matrix = True
        k_lambda_max = calc_lambda_max(matrix, print_iterations=print_iterations)
        if print_iterations:
            print(f"{interval}Критерій: ", k_lambda_max)
        k_weights = calculate_weights(matrix)
        print(f"{interval}Ваги критеріїв w:", k_weights)
        k_CI = calculate_CI(k_lambda_max, t)
        if k_CI > 0.1:
            valid_matrix = False
        k_CR = calculate_CR(k_CI, t)
        if k_CR <= 0.2:
            if t == 3 and k_CI > 0.05:
                valid_matrix = False
            elif t == 4 and k_CI > 0.08:
                valid_matrix = False
        else:
            valid_matrix = False
        print(f"{interval}CI: {k_CI}, CR: {k_CR}")

        if not valid_matrix:
            print(f"{interval}Ступінь неузгодженності: не прийнятний")
            matrix = correct_matrix(matrix)
        else:
            print(f"{interval}Ступінь неузгодженності: прийнятний")

    return matrix, k_weights


def calculate_global_weights(k_weights, omega_weights, p_weights, t, m, n):
    t = int(t)
    m = int(m)
    n = int(n)

    p = []
    for i in range(n):
        p_i = 0
        for k in range(t):
            p_i_j = 0
            for j in range(m):
                p_i_j += omega_weights[k][j] * p_weights[k][j][i]
            p_i += p_i_j * k_weights[k]
        p.append(round(p_i, 5))

    return p


def main():
    np.set_printoptions(threshold=99999,
                        linewidth=200,
                        precision=5)

    data = read_bad_data('data/Варіант №52 умова.txt')
    t, m, n, k, omega, weights_p = data

    print("Кількість експертів: ", t)
    print("Кількість критеріїв: ", m)
    print("Кількість альтернатив: ", n)
    print("МПП експертів:", k, sep='\n')

    print("Локальні пріоритети МПП експертів:")
    _, k_weights = check_matrix(k, print_iterations=True)

    print('-' * 50)

    omega_weights = []
    for i in range(len(omega)):
        print(f"Експерт {i + 1}:")
        _, w = check_matrix(omega[i], interval='\t')
        omega_weights.append(w)

    print('-' * 50)

    p_weights = []
    for i in range(len(weights_p)):
        print(f"Експерт {i + 1}:")
        p_weights.append([])
        for j in range(len(weights_p[i])):
            print(f"\tКритерій {j + 1}:")
            _, w = check_matrix(weights_p[i][j], interval='\t\t')
            p_weights[-1].append(w)

    global_weights = calculate_global_weights(k_weights, omega_weights, p_weights, t, m, n)
    print("Глобальні ваги: ", global_weights)
    print("Ранжування:", np.argsort(global_weights)[::-1] + 1)


if __name__ == "__main__":
    main()
