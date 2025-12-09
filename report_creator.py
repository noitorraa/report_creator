import csv
import argparse
from tabulate import tabulate

parser = argparse.ArgumentParser(description="Утилита для создания отчетов")
parser.add_argument(
    "--name",
    dest="csvFile",
    nargs="+",
    required=True,
    help="Аргумент, принимающий пути к csv файлам",
)
parser.add_argument(
    "--report",
    dest="reportName",
    nargs=1,
    required=True,
    help="Аргумент, принимающий название для итогового отчета",
)

args = parser.parse_args()
print(args.csvFile, args.reportName)

allData = []
for file_path in args.csvFile:
    with open(file_path) as f:
        reader = csv.reader(f)
        next(reader)
        allData.extend(list(reader))
positionStats = {}
for row in allData:
    position = row[1]
    performance = float(row[3])
    if position not in positionStats:
        positionStats[position] = {"total": 0, "count": 0}
    positionStats[position]["total"] += performance
    positionStats[position]["count"] += 1

sorted_stats = sorted(
    positionStats.items(), key=lambda x: x[1]["total"] / x[1]["count"], reverse=True
)

table_data = []
for index, (position, stats) in enumerate(sorted_stats, 1):
    avg = stats["total"] / stats["count"]
    table_data.append([index, position, f"{avg:.2f}"])

print(tabulate(table_data, headers=["#", "position", "performance"]))


# Нужно разбить код по функциям, передавать в функции index столбца, по которому ведутся расчеты, чтобы дркгой разработчик легко мог изменить эту часть, также нужно обернуть код тестами, еще добавить обработку ошибок, изменить имена переменных, еще не использую название для отчета, но в тех задании об этом речи не было...
