import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import csv
from datetime import datetime


def open_csv(address: str):
    with open(address, 'r', encoding="utf-16-le", errors="ignore") as f:
        data = csv.reader(f)
        split_data = []
        for row in data:
            split_data.append(row)

    return split_data[1:]


def gen_progress_graph(data: np.array, exercise: str):
    rel_data_tots = {}

    for log in data:
        exercise_name = log[3]
        if exercise == exercise_name:

            date_lst = str(log[0]).split('/')
            date = datetime(int(date_lst[2]), int(date_lst[1]), int(date_lst[0]))
            weight = log[-3].split('\u202f')
            reps = int(log[-4].split('\xa0')[0])

            if weight[1] == 'lb':
                weight = float(weight[0]) * 0.4536  # convert to kg
            else:
                weight = float(weight[0])

            if date in rel_data_tots:
                rel_data_tots[date][0] += weight * reps
                rel_data_tots[date][1] += reps
                if weight > rel_data_tots[date][2]:
                    rel_data_tots[date][2] = weight
            else:
                rel_data_tots[date] = [weight * reps, reps, weight]

    for mode in {'avg', 'max', 'total'}:
        plot_results(rel_data_tots, exercise, mode)


def plot_results(rel_data_tots, exercise: str, mode: str):
    assert mode in {'avg', 'max', 'total'}

    plottable_data_x = rel_data_tots.keys()
    plottable_data_y = np.array(list(rel_data_tots.values()))

    weight_tots = plottable_data_y[:, 0]
    rep_tots = plottable_data_y[:, 1]
    weight_maxes = plottable_data_y[:, 2]

    if mode == 'avg':
        plottable_data_y = weight_tots / rep_tots
        plt.ylabel('Average weight per rep (kg)')
    elif mode == 'total':
        plottable_data_y = weight_tots
        plt.ylabel('Total weight lifted (kg)')
    elif mode == 'max':
        plottable_data_y = weight_maxes
        plt.ylabel('Max weight lifted (kg)')

    plt.plot(plottable_data_x, plottable_data_y, marker='o')
    plt.title(exercise)
    plt.xlabel('Date')
    plt.savefig(exercise + '_' + mode)


if __name__ == "__main__":
    my_data = open_csv("GymBook-Logs-2025-03-12.csv")

    gen_progress_graph(my_data, 'Dumbbell Bulgarian Split Squats')
