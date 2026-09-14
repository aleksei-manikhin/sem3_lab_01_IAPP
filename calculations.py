import math
from typing import List

from models import Percentiles, Statistics


def _prepare_values(values: List[float]) -> List[float]:
    if not values:
        raise ValueError("Нет значений для расчёта.")

    for value in values:
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("Для расчёта нужны конечные числа.")

    return sorted(values)


def _calculate_mean(values: List[float]) -> float:
    count = len(values)
    return math.fsum(value / count for value in values)


def _calculate_percentile(sorted_values: List[float], percent: int) -> float:
    position = (len(sorted_values) - 1) * percent / 100 #Переводим проценты в индекс по сути
    lower = int(position) #Находим верх и ниж границы индекса
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = position - lower # Насколько близок к верх знач

    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def calculate_statistics(values: List[float]) -> Statistics:
    sorted_values = _prepare_values(values)

    return {
        "min": sorted_values[0],
        "max": sorted_values[-1],
        "median": _calculate_percentile(sorted_values, 50),
        "mean": _calculate_mean(sorted_values),
    }


def calculate_percentiles(values: List[float]) -> Percentiles:
    sorted_values = _prepare_values(values)

    return [
        (percent, _calculate_percentile(sorted_values, percent))
        for percent in range(0, 101, 5)
    ]
