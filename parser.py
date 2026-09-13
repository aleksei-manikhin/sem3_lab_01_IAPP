import math
from typing import List, Optional

from models import (
    COLUMN_NAMES,
    REGION_COLUMN,
    YEAR_COLUMN,
    CellValue,
    DataRow,
    Dataset,
)


def _parse_region(value: str) -> str:
    if not value:
        raise ValueError("Название региона не указано.")
    return value


def _parse_year(value: str) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise ValueError("Год должен быть целым числом.") from error


def _parse_number(value: str) -> Optional[float]:
    if not value:
        return None

    try:
        number = float(value)
    except ValueError as error:
        raise ValueError("В числовой колонке указано не число.") from error

    if not math.isfinite(number):
        raise ValueError("Число не должно быть NaN или бесконечностью.")

    return number


def _parse_cell(value: str, column: str) -> CellValue:
    value = value.strip()

    if column == REGION_COLUMN:
        return _parse_region(value)
    if column == YEAR_COLUMN:
        return _parse_year(value)
    return _parse_number(value)


def _parse_header(header: List[str]) -> List[str]:
    columns = [name.strip() for name in header]

    if len(columns) != len(COLUMN_NAMES) or set(columns) != set(COLUMN_NAMES):
        raise ValueError("Названия или количество колонок не соответствуют формату.")

    return columns


def _parse_row(columns: List[str], row: List[str]) -> DataRow:
    if len(row) != len(columns):
        raise ValueError("Количество ячеек в строке не совпадает с заголовком.")

    return {
        column: _parse_cell(value, column)
        for column, value in zip(columns, row)
    }


def parse_csv(header: List[str], rows: List[List[str]]) -> Dataset:
    columns = _parse_header(header)
    dataset = [_parse_row(columns, row) for row in rows if row]

    if not dataset:
        raise ValueError("CSV-файл не содержит строк с данными.")

    return dataset
