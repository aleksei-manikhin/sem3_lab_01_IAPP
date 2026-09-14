import math
import typing

import models


def _parse_region(value: str) -> str:
    if not value:
        raise ValueError("Название региона не указано.")
    return value


def _parse_year(value: str) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise ValueError("Год должен быть целым числом.") from error


def _parse_number(value: str) -> typing.Optional[float]:
    if not value:
        return None

    try:
        number = float(value)
    except ValueError as error:
        raise ValueError("В числовой колонке указано не число.") from error

    if not math.isfinite(number):
        raise ValueError("Число не должно быть NaN или бесконечностью.")

    return number


def _parse_cell(value: str, column: str) -> models.CellValue:
    value = value.strip()

    if column == models.REGION_COLUMN:
        return _parse_region(value)
    if column == models.YEAR_COLUMN:
        return _parse_year(value)
    return _parse_number(value)


def _parse_header(header: typing.List[str]) -> typing.List[str]:
    columns = [name.strip() for name in header]

    if (
        len(columns) != len(models.COLUMN_NAMES)
        or set(columns) != set(models.COLUMN_NAMES)
    ):
        raise ValueError("Названия или количество колонок не соответствуют формату.")

    return columns


def _parse_row(
    columns: typing.List[str], row: typing.List[str]
) -> models.DataRow:
    if len(row) != len(columns):
        raise ValueError("Количество ячеек в строке не совпадает с заголовком.")

    return {
        column: _parse_cell(value, column)
        for column, value in zip(columns, row)
    }


def parse_csv(
    header: typing.List[str], rows: typing.List[typing.List[str]]
) -> models.Dataset:
    columns = _parse_header(header)
    dataset = [_parse_row(columns, row) for row in rows if row]

    if not dataset:
        raise ValueError("CSV-файл не содержит строк с данными.")

    return dataset
