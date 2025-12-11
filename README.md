# report_creator

Утилита командной строки на Python для анализа CSV-файлов. Группирует данные по должностям, вычисляет среднюю производительность и формирует читаемый отчет.

## Начало работы

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/noitorraa/report_creator.git
    cd report_creator
    ```
2.  **Установите зависимости:**
    ```bash
    pip install -e .
    ```

## Использование

```bash
python main.py --name <путь/к/файлу1.csv> --report <имя_отчета>
```
**Пример:**
```bash
python main.py --name data/sales.csv data/hr.csv --report summary
```
Результат сохранится в `summary_report.txt`.

## Запуск тестов

Проект покрыт тестами (~80%). Для запуска:
```bash
# Установите dev-зависимости
pip install -e ".[dev]"
# Запустите тесты
pytest tests/ -v
```
