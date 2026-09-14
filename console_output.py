import typing

import errors
import models

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"


def _style(text: str, *styles: str) -> str:
    return "".join(styles) + text + RESET


def show_file_menu() -> None:
    print("\nКак открыть CSV-файл?")
    print("1. Ввести путь вручную")
    print("2. Выбрать файл через проводник")
    print("0. Завершить программу")


def show_regions(regions: typing.List[str]) -> None:
    print("\nДоступные регионы:")
    for number, region in enumerate(regions, start=1):
        print(str(number) + ". " + region)
    print("0. Вернуться к выбору файла")


def show_columns(columns: typing.Dict[int, str]) -> None:
    print("\nЧисловые колонки:")
    for column_id, name in columns.items():
        print(str(column_id) + ". " + name)
    print("0. Вернуться к выбору региона")


def show_menu() -> None:
    print("\nЧто сделать дальше?")
    print("1. Изменить файл")
    print("2. Изменить регион")
    print("3. Изменить колонку")
    print("0. Завершить программу")


def show_error(error: Exception) -> None:
    message = errors.get_error_message(error)
    border = "!" * (len(message) + 10)
    print("\n" + _style(border, RED, BOLD))
    print(_style("  ОШИБКА: " + message + "  ", RED, BOLD))
    print(_style(border, RED, BOLD))


def _format_value(value: models.CellValue) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return format(value, ".4f")
    return str(value).replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")


def _print_row(cells: typing.List[str], widths: typing.List[int]) -> None:
    cells = [cell.ljust(width) for cell, width in zip(cells, widths)]
    print("| " + " | ".join(cells) + " |")


def _show_table(
    headers: typing.List[str], rows: typing.List[typing.List[str]]
) -> None:
    widths = [
        max(len(row[index]) for row in [headers, *rows])
        for index in range(len(headers))
    ]
    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    print(separator)
    _print_row(headers, widths)
    print(separator)
    for row in rows:
        _print_row(row, widths)
    print(separator)


def show_data(rows: models.Dataset) -> None:
    print("\nДанные выбранного региона:")
    if not rows:
        print("Нет данных для отображения.")
        return

    columns = list(rows[0])
    cells = [[_format_value(row[column]) for column in columns] for row in rows]
    _show_table(columns, cells)


def show_statistics(statistics: models.Statistics) -> None:
    print("\n" + _style("Статистика:", BOLD))
    labels = {
        "max": "Максимум:",
        "min": "Минимум:",
        "median": "Медиана:",
        "mean": "Среднее:",
    }
    for key, label in labels.items():
        value = _format_value(statistics[key])
        print(_style(label.ljust(10) + " " + value, BOLD))


def show_percentiles(percentiles: models.Percentiles) -> None:
    print("\nПерцентили:")
    rows = [[str(percent), _format_value(value)] for percent, value in percentiles]
    _show_table(["Перцентиль, %", "Значение"], rows)


def show_counts(used_count: int, missing_count: int) -> None:
    print("Использовано значений:", used_count)
    print("Пропущено значений:", missing_count)


def show_selection(path: str, region: str, column: str) -> None:
    print("\nФайл:", path)
    print("Регион:", region)
    print("Колонка:", column)
