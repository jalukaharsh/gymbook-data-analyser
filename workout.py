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

        plot_results(rel_data_tots, exercise)


def plot_results(rel_data_tots: dict, exercise: str):
    plottable_data_x = rel_data_tots.keys()
    plottable_data_y = np.array(list(rel_data_tots.values()))

    weight_tots = plottable_data_y[:, 0]
    rep_tots = plottable_data_y[:, 1]
    weight_maxes = plottable_data_y[:, 2]

    figure, axs = plt.subplots(2, figsize=(12, 8))
    figure.suptitle(exercise)

    plottable_data_y_avg = weight_tots / rep_tots
    plottable_data_y_total = weight_tots
    plottable_data_y_max = weight_maxes

    axs[0].plot(plottable_data_x, plottable_data_y_max, marker='o', label='Max Weight Per Rep')
    axs[0].plot(plottable_data_x, plottable_data_y_avg, marker='o', label='Average Weight Per Rep')
    axs[0].set(ylabel='Weight (kg)')
    axs[0].legend(loc='upper left')

    axs[1].plot(plottable_data_x, plottable_data_y_total, marker='o', label='Total Weight')
    axs[1].set(xlabel='Date', ylabel='Weight (kg)')
    axs[1].legend(loc='upper left')

    plt.savefig(exercise)
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
