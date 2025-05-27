import csv
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


def open_csv(address: str):
    with open(address, 'r', encoding="utf-16-le", errors="ignore") as f:
        data = csv.reader(f)
        split_data = []
        for row in data:
            split_data.append(row)

    return split_data[1:]


def gen_progress_graph(data: np.array, exercises: set):
    for exercise in exercises:
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


def plot_results(rel_data_tots: dict, exercise: str, mode: str):
    assert mode in {'avg', 'max', 'total'}

    plottable_data_x = rel_data_tots.keys()
    plottable_data_y = np.array(list(rel_data_tots.values()))

    try:
        weight_tots = plottable_data_y[:, 0]
        rep_tots = plottable_data_y[:, 1]
        weight_maxes = plottable_data_y[:, 2]
    except IndexError:
        print(exercise)
        print(rel_data_tots)
        print(plottable_data_y)
        exit()

    # figure = plt.figure(figsize=(12,8))
    figure, ax = plt.subplots(figsize=(12, 8))

    if mode == 'avg':
        plottable_data_y = weight_tots / rep_tots
        plt.ylabel('Average weight per rep (kg)')
    elif mode == 'total':
        plottable_data_y = weight_tots
        plt.ylabel('Total weight lifted (kg)')
    elif mode == 'max':
        plottable_data_y = weight_maxes
        plt.ylabel('Max weight lifted (kg)')

    ax.plot(plottable_data_x, plottable_data_y, marker='o')
    plt.title(exercise)
    plt.xlabel('Date')
    plt.savefig(exercise + '_' + mode)
    plt.close()


if __name__ == "__main__":
    my_data = open_csv("GymBook-Logs-2025-05-25.csv")

    my_exercises = {'Alternating Dumbbell Curls',
                    'Arnold Presses',
                    'Assisted Chin Dips',
                    'Assisted Pull-Ups',
                    'Dumbbell Bench Presses',
                    'Dumbbell Bulgarian Split Squats',
                    'Seated Leg Curls',
                    'Single-Arm Overhead Triceps Extension',
                    'Wide-Grip Lat Pull-Downs'}

    gen_progress_graph(my_data, my_exercises)
