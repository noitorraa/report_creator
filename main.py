import argparse
from report_tool import (
    read_csv_files,
    calculate_position_stats,
    sort_stats_by_performance,
    prepare_table_data,
    print_report,
)


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
        type=str,
        required=True,
        help="Аргумент, принимающий название для итогового отчета",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    all_data = read_csv_files(args.csv_files)
    position_stats = calculate_position_stats(all_data)
    sorted_stats = sort_stats_by_performance(position_stats)
    table_data = prepare_table_data(sorted_stats)
    print_report(table_data, args.report_name)


if __name__ == "__main__":
    main()
