import csv
import re
from datetime import datetime
from pathlib import Path


def find_latest_csv() -> str:
    data_dir = Path("data")
    csv_files = list(data_dir.glob("GymBook-Logs-*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found in data directory")

    latest_file = max(
        csv_files,
        key=lambda f: datetime.strptime(f.stem.replace("GymBook-Logs-", ""), "%Y-%m-%d")
    )
    return str(latest_file)


def open_csv(address: str) -> list:
    with open(address, 'r', encoding="utf-16-le", errors="ignore") as f:
        data = list(csv.reader(f))
    return data[1:]  # skip header


def extract_exercises(data: list) -> set:
    return {log[3] for log in data}


def parse_weight(log: list) -> tuple[float, int] | None:
    """
    Returns (weight_kg, reps) from a log row, or None if the row should be skipped.
    """
    weight_parts = re.split(r'[\xa0\u202f]', log[-3])
    reps = int(log[-4].split('\xa0')[0])

    if len(weight_parts) == 2:
        weight = float(weight_parts[0])
        if weight_parts[1] == 'lb':
            weight *= 0.4536
    else:
        print(f"Unexpected weight format in log: {log}")
        weight = reps
        reps = 1

    return weight, reps


def build_exercise_data(data: list) -> dict[str, dict[datetime, list]]:
    """
    Returns a nested dict: { exercise_name: { date: [total_volume, total_reps, max_weight] } }
    Skips warmup sets (log[-1] == "Yes").
    """
    exercise_data: dict[str, dict[datetime, list]] = {}

    for log in data:
        if log[-1] == "Yes":  # skip warmup sets
            continue

        exercise_name = log[3]
        date_parts = str(log[0]).split('-')
        date = datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))

        weight, reps = parse_weight(log)

        day = exercise_data.setdefault(exercise_name, {})
        if date in day:
            day[date][0] += weight * reps
            day[date][1] += reps
            if weight > day[date][2]:
                day[date][2] = weight
        else:
            day[date] = [weight * reps, reps, weight]

    return exercise_data


def load() -> tuple[dict[str, dict[datetime, list]], set[str]]:
    """
    Main entry point. Returns (exercise_data, exercises).
    exercise_data: { exercise_name: { date: [total_volume, total_reps, max_weight] } }
    exercises: set of all exercise names
    """
    raw = open_csv(find_latest_csv())
    exercise_data = build_exercise_data(raw)
    exercises = set(exercise_data.keys())
    return exercise_data, exercises
