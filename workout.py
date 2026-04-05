import csv
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path
import re

matplotlib.use('TkAgg')


def open_csv(address: str):
    with open(address, 'r', encoding="utf-16-le", errors="ignore") as f:
        data = csv.reader(f)
        split_data = []
        for row in data:
            split_data.append(row)

    return split_data[1:]


def gen_progress_graph(data: np.array, exercises: set):
    exercise_count = {key: 0 for key in exercises}
    for exercise in exercises:
        rel_data_tots = {}

        for log in data:
            if log[-1] == "Yes": 
                continue
            exercise_name = log[3]
            if exercise == exercise_name:
                exercise_count[exercise_name] += 1
                date_lst = str(log[0]).split('-')
                date = datetime(int(date_lst[0]), int(date_lst[1]), int(date_lst[2]))
                weight = re.split(r'[\xa0\u202f]', log[-3])
                reps = int(log[-4].split('\xa0')[0])

                if len(weight) == 2: 
                    if weight[1] == 'lb':
                        weight = float(weight[0]) * 0.4536  # convert to kg
                    else:
                        weight = float(weight[0])
                        # if weight[1] != 'kg': 
                        #     print(weight)
                else: 
                    print(log)
                    print(type(weight)) 
                    print(weight)
                    weight = reps
                    reps = 1

                if date in rel_data_tots:
                    rel_data_tots[date][0] += weight * reps
                    rel_data_tots[date][1] += reps
                    if weight > rel_data_tots[date][2]:
                        rel_data_tots[date][2] = weight
                else:
                    rel_data_tots[date] = [weight * reps, reps, weight]

        str_count = str(exercise_count[exercise]).zfill(3) 
        try: 
            plot_results(rel_data_tots, exercise, str_count)
        except: 
            print(exercise)

def plot_results(rel_data_tots: dict, exercise: str, count: str):
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

    plt.savefig("exercises/" + count + ' ' + exercise)
    plt.close()

def find_latest_csv() -> str:
    data_dir = Path("data")
    csv_files = list(data_dir.glob("GymBook-Logs-*.csv"))
    
    if not csv_files:
        raise FileNotFoundError("No CSV files found in data directory")
    
    latest_file = None
    latest_date = None
    
    for csv_file in csv_files:
        # Extract date from filename: GymBook-Logs-2025-05-25.csv
        date_str = csv_file.stem.replace("GymBook-Logs-", "")
        file_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        if latest_date is None or file_date > latest_date:
            latest_date = file_date
            latest_file = csv_file
    
    return str(latest_file)

def extract_exercises(data: np.array) -> set(): 
    all_exercises = set()
    for log in data:
        all_exercises.add(log[3])

    return all_exercises


if __name__ == "__main__":
    my_data = open_csv(find_latest_csv())

    my_exercises = extract_exercises(my_data)

    gen_progress_graph(my_data, my_exercises)
