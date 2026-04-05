import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from data_loader import load

matplotlib.use('TkAgg')


def gen_progress_graph(exercise_data: dict, exercises: set):
    exercise_count = {key: len(dates) for key, dates in exercise_data.items()}

    for exercise in exercises:
        rel_data_tots = exercise_data.get(exercise, {})
        str_count = str(exercise_count.get(exercise, 0)).zfill(3)
        try:
            plot_results(rel_data_tots, exercise, str_count)
        except Exception:
            print(exercise)


def plot_results(rel_data_tots: dict, exercise: str, count: str):
    plottable_data_x = rel_data_tots.keys()
    plottable_data_y = np.array(list(rel_data_tots.values()))

    weight_tots = plottable_data_y[:, 0]
    rep_tots = plottable_data_y[:, 1]
    weight_maxes = plottable_data_y[:, 2]

    figure, axs = plt.subplots(2, figsize=(12, 8))
    figure.suptitle(exercise)

    axs[0].plot(plottable_data_x, weight_maxes, marker='o', label='Max Weight Per Rep')
    axs[0].plot(plottable_data_x, weight_tots / rep_tots, marker='o', label='Average Weight Per Rep')
    axs[0].set(ylabel='Weight (kg)')
    axs[0].legend(loc='upper left')

    axs[1].plot(plottable_data_x, weight_tots, marker='o', label='Total Weight')
    axs[1].set(xlabel='Date', ylabel='Weight (kg)')
    axs[1].legend(loc='upper left')

    plt.savefig("exercises/" + count + ' ' + exercise)
    plt.close()


if __name__ == "__main__":
    exercise_data, exercises = load()
    gen_progress_graph(exercise_data, exercises)
