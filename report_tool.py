import csv
import argparse
from tabulate import tabulate

# Константы для адаптивности
POSITION_COL = 1
PERFORMANCE_COL = 3


def read_csv_files(file_paths):
    all_data = []
    for file_path in file_paths:
        try:
            with open(file_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # пропускаем заголовок
                all_data.extend(list(reader))
        except FileNotFoundError:
            print(f"Ошибка: файл {file_path} не найден")
            exit(1)
    return all_data


def calculate_position_stats(
    data, position_col=POSITION_COL, performance_col=PERFORMANCE_COL
):
    position_stats = {}
    for row in data:
        if not row:
            continue
        try:
            position = row[position_col]
            performance = float(row[performance_col])

            if position not in position_stats:
                position_stats[position] = {"total": 0, "count": 0}

            position_stats[position]["total"] += performance
            position_stats[position]["count"] += 1
        except (IndexError, ValueError) as e:
            print(f"Пропускаем некорректную строку: {row}")
            continue
    return position_stats


def sort_stats_by_performance(position_stats):
    if not position_stats:
        return []
    return sorted(
        position_stats.items(),
        key=lambda x: x[1]["total"] / x[1]["count"],
        reverse=True,
    )


def prepare_table_data(sorted_stats):
    table_data = []
    for index, (position, stats) in enumerate(sorted_stats, 1):
        avg = stats["total"] / stats["count"]
        table_data.append([index, position, f"{avg:.2f}"])
    return table_data


def print_report(table_data, report_name=None):
    report_table = tabulate(table_data, headers=["#", "position", "performance"])
    print(report_table)

    if report_name:
        filename = f"{report_name}_report.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_table)
        print(f"\nОтчет сохранен в {filename}")
