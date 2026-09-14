import typing

import calculations
import models


def get_regions(dataset: models.Dataset) -> typing.List[str]:
    return sorted({row[models.REGION_COLUMN] for row in dataset}, key=str.casefold)


def get_region_data(dataset: models.Dataset, region: str) -> models.Dataset:
    rows = [row for row in dataset if row[models.REGION_COLUMN] == region]

    if not rows:
        raise ValueError("В выбранном регионе нет данных.")

    return sorted(rows, key=lambda row: row[models.YEAR_COLUMN])


def get_numeric_columns(
    dataset: models.Dataset
) -> typing.Dict[int, str]:
    if not dataset:
        raise ValueError("Набор данных пуст.")

    return {
        column_id: name
        for column_id, name in enumerate(dataset[0], start=1)
        if name in models.NUMERIC_COLUMNS
    }


def get_column_values(rows: models.Dataset, column: str) -> typing.List[float]:
    if column not in models.NUMERIC_COLUMNS:
        raise ValueError("Выберите числовую колонку.")

    return [row[column] for row in rows if row[column] is not None]


def analyze_column( rows: models.Dataset, column: str 
                   ) -> typing.Tuple[models.Statistics, models.Percentiles, int]:
    values = get_column_values(rows, column)
    statistics = calculations.calculate_statistics(values)
    percentiles = calculations.calculate_percentiles(values)
    missing_count = len(rows) - len(values)

    return statistics, percentiles, missing_count
