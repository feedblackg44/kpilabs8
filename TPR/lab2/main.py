import numpy as np
import pandas as pd

from task1 import *
from task2 import *
from task3 import *


def read_excel_data(filename, variant):
    df = pd.read_excel(filename, header=None)

    target_row_index = df[df[df.columns[0]].astype(str).str.contains(str(variant))].index.min()

    if target_row_index is pd.NA:
        return "Цифра не найдена."

    start_row = max(0, target_row_index - 1)
    end_row = min(len(df) - 1, target_row_index + 7)

    result_df = df.iloc[start_row:end_row + 1].reset_index()

    experts_data = []

    last_row = result_df.iloc[-1]
    w_indices = last_row[last_row.astype(str).str.contains('w', case=False, na=False)].index

    for w_index in w_indices:
        w = round(float(result_df.iloc[-1, w_index + 2]), 2)
        a_count = result_df[w_index].str.contains('А', na=False).sum()
        first_a_row_index = result_df[result_df[w_index].str.contains('А', na=False)].index[0]
        matrix_df = result_df.iloc[first_a_row_index:first_a_row_index + a_count, w_index + 2:w_index + 2 + a_count]
        matrix_np = matrix_df.to_numpy().astype(float)

        experts_data.append({"w": w, "matrix": matrix_np})

    return experts_data


def check_R(R, name="R1"):
    reflexive_R1 = check_reflexive(R).lower()
    antireflexive_R1 = check_antireflexive(R).lower()
    symmetric_R1 = check_symmetric(R).lower()
    connectivity_R1 = check_connectivity(R).lower()
    transitive_R1 = check_transitive(R).lower()
    print(f"{name}: {reflexive_R1}, {antireflexive_R1}, {symmetric_R1}, {connectivity_R1}, {transitive_R1}")


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    np.set_printoptions(precision=1, floatmode='fixed')

    filename = "./data/Варіанти1-95 Практикум2.xlsx"

    variant = 52

    data = read_excel_data(filename, variant)
    for i, expert in enumerate(data):
        for key, value in expert.items():
            if key == "matrix":
                print(f"Експерт {i + 1} {key}:")
                print(value)
            else:
                print(f"Експерт {i + 1} {key}: {value}")

    print("\n" + "=" * 50 + "\n")
    print("Завдання 1:\n")

    R1 = data[0]["matrix"]
    R2 = data[1]["matrix"]

    check_R(R1)
    check_R(R2, "R2")

    union = np.maximum(R1, R2)
    intersection = np.minimum(R1, R2)
    complement1 = 1 - R1
    complement2 = 1 - R2
    composition = np.zeros_like(R1)
    for i in range(R1.shape[0]):
        for j in range(R1.shape[1]):
            composition[i, j] = max(min(R1[i, k], R2[k, j]) for k in range(R1.shape[1]))
    print(f"Об'єднання:\n{union}")
    print(f"Перетин:\n{intersection}")
    print(f"Доповнення R1:\n{complement1}")
    print(f"Доповнення R2:\n{complement2}")
    print(f"Композиція:\n{composition}")

    alpha_levels_05 = (R1 >= 0.5).astype(int)
    alpha_levels_09 = (R1 >= 0.9).astype(int)
    print(f"Альфа-рівні 0.5:\n{alpha_levels_05}")
    print(f"Альфа-рівні 0.9:\n{alpha_levels_09}")

    strict_preference_R1 = get_strict_preference(R1)
    indefference_R1 = get_indifference(R1)
    quasiequivalence_R1 = get_quasiequivalence(R1)
    print(f"Строга перевага:\n{strict_preference_R1}")
    print(f"Байдужість:\n{indefference_R1}")
    print(f"Квазіеквівалентність:\n{quasiequivalence_R1}")

    print("\n" + "=" * 50 + "\n")
    print("Завдання 2:\n")

    np.set_printoptions(precision=2, floatmode='fixed')

    best_alternative = solve_1expert_problem(R1)
    print(f"Найкраща альтернатива: {best_alternative + 1}")

    print("\n" + "=" * 50 + "\n")
    print("Завдання 3:\n")

    best_alternative = solve_multi_expert_problem(data)
    print(f"Найкраща альтернатива: {best_alternative + 1}")


if __name__ == "__main__":
    main()
