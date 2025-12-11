from report_tool import (
    read_csv_files,
    calculate_position_stats,
    sort_stats_by_performance,
    prepare_table_data,
    print_report,
)


def test_read_csv_files_valid():
    import csv
    import os

    test_file = "test_employees.csv"
    with open(test_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "position", "location", "performance"])
        writer.writerow(["Alice", "Manager", "NY", "100.0"])
        writer.writerow(["Bob", "Developer", "SF", "150.0"])

    try:
        result = read_csv_files([test_file])
        assert len(result) == 2
        assert result[0] == ["Alice", "Manager", "NY", "100.0"]
        assert result[1] == ["Bob", "Developer", "SF", "150.0"]

    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_read_csv_files_multiple():
    import csv
    import os

    test_file1 = "test_employees1.csv"
    test_file2 = "test_employees2.csv"

    with open(test_file1, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "position", "location", "performance"])
        writer.writerow(["Alice", "Manager", "NY", "100.0"])

    with open(test_file2, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "position", "location", "performance"])
        writer.writerow(["Bob", "Developer", "SF", "150.0"])

    try:
        result = read_csv_files([test_file1, test_file2])
        assert len(result) == 2
        assert result[0] == ["Alice", "Manager", "NY", "100.0"]
        assert result[1] == ["Bob", "Developer", "SF", "150.0"]

    finally:
        for f in [test_file1, test_file2]:
            if os.path.exists(f):
                os.remove(f)


def test_read_csv_files_not_found():
    """Тестируем обработку отсутствующего файла"""
    import sys
    from unittest.mock import patch

    with patch("report_tool.exit") as mock_exit:
        with patch("builtins.print") as mock_print:
            try:
                result = read_csv_files(["nonexistent_file.csv"])
            except SystemExit:
                pass  # Это ожидаемо

            mock_exit.assert_called_with(1)
            mock_print.assert_called()


def test_calculate_position_stats_basic():
    test_data = [
        ["Alice", "Manager", "NY", "100.0"],
        ["Bob", "Developer", "SF", "150.0"],
        ["Charlie", "Manager", "NY", "200.0"],
    ]
    result = calculate_position_stats(test_data)

    assert "Manager" in result
    assert "Developer" in result
    assert result["Manager"]["total"] == 300.0  # 100 + 200
    assert result["Manager"]["count"] == 2
    assert result["Developer"]["total"] == 150.0
    assert result["Developer"]["count"] == 1


def test_calculate_position_stats_empty_rows():
    test_data = [
        ["Alice", "Manager", "NY", "100.0"],
        [],  # Пустая строка
        ["Bob", "Developer", "SF", "150.0"],
        [""],  # Почти пустая строка
    ]

    result = calculate_position_stats(test_data)

    assert len(result) == 2


def test_calculate_position_stats_invalid_data():
    test_data = [
        ["Alice", "Manager", "NY", "100.0"],
        ["Bob", "Developer", "SF", "not_a_number"],  # Не число!
        ["Charlie", "Manager", "NY", "200.0"],
    ]

    result = calculate_position_stats(test_data)

    assert "Manager" in result
    assert result["Manager"]["total"] == 300.0
    assert result["Manager"]["count"] == 2


def test_sort_stats_by_performance():
    stats = {
        "Intern": {"total": 90, "count": 1},  # avg = 90
        "Manager": {"total": 300, "count": 3},  # avg = 100
        "Developer": {"total": 450, "count": 3},  # avg = 150
    }

    result = sort_stats_by_performance(stats)

    assert result[0][0] == "Developer"  # Самый высокий avg
    assert result[1][0] == "Manager"
    assert result[2][0] == "Intern"


def test_sort_stats_empty():
    result = sort_stats_by_performance({})
    assert result == []


def test_prepare_table_data():
    sorted_stats = [
        ("Developer", {"total": 450, "count": 3}),
        ("Manager", {"total": 300, "count": 3}),
    ]

    result = prepare_table_data(sorted_stats)

    assert len(result) == 2

    assert result[0][0] == 1  # Порядковый номер
    assert result[0][1] == "Developer"  # Должность
    assert result[0][2] == "150.00"  # Среднее значение

    assert result[1][0] == 2
    assert result[1][1] == "Manager"
    assert result[1][2] == "100.00"


def test_print_report_without_file():
    table_data = [
        [1, "Developer", "150.00"],
        [2, "Manager", "100.00"],
    ]

    try:
        print_report(table_data, None)
        assert True  # Если не упало - тест пройден
    except Exception as e:
        assert False, f"Функция упала с ошибкой: {e}"


def test_print_report_with_file():
    import os

    table_data = [
        [1, "Developer", "150.00"],
        [2, "Manager", "100.00"],
    ]

    report_name = "test_report"

    try:
        print_report(table_data, report_name)
        expected_filename = f"{report_name}_report.txt"
        assert os.path.exists(expected_filename)
        with open(expected_filename, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Developer" in content
            assert "Manager" in content
            assert "150" in content  # Формат может быть 150 или 150.00
            assert "100" in content  # Формат может быть 100 или 100.00

    finally:
        expected_filename = f"{report_name}_report.txt"
        if os.path.exists(expected_filename):
            os.remove(expected_filename)


if __name__ == "__main__":
    print("Запуск тестов...")

    test_functions = [
        test_read_csv_files_valid,
        test_read_csv_files_multiple,
        test_read_csv_files_not_found,
        test_calculate_position_stats_basic,
        test_calculate_position_stats_empty_rows,
        test_calculate_position_stats_invalid_data,
        test_sort_stats_by_performance,
        test_sort_stats_empty,
        test_prepare_table_data,
        test_print_report_without_file,
        test_print_report_with_file,
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            print(f"{test_func.__name__}: PASSED")
            passed += 1
        except AssertionError as e:
            print(f"{test_func.__name__}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"{test_func.__name__}: ERROR - {e}")
            failed += 1

    print(f"\nИтого: {passed} пройдено, {failed} упало")
