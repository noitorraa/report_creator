import csv
import argparse
from tabulate import tabulate


def parse_arguments():
    parser = argparse.ArgumentParser(description="Утилита для создания отчетов")
    parser.add_argument(
        "--name",
        dest="csv_files",
        nargs="+",
        required=True,
        help="Аргумент, принимающий пути к csv файлам",
    )
    parser.add_argument(
        "--report",
        dest="report_name",
        nargs=1,
        required=True,
        help="Аргумент, принимающий название для итогового отчета",
    )
    return parser.parse_args()


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


def calculate_position_stats(data, position_col=1, performance_col=3):
    position_stats = {}
    for row in data:
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


def main():
    args = parse_arguments()
    all_data = read_csv_files(args.csv_files)
    position_stats = calculate_position_stats(all_data)
    sorted_stats = sort_stats_by_performance(position_stats)
    table_data = prepare_table_data(sorted_stats)
    report_name = args.report_name[0] if args.report_name else None
    print_report(table_data, report_name)


if __name__ == "__main__":
    main()

