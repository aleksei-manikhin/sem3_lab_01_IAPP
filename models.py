from typing import Dict, List, Tuple, Union


YEAR_COLUMN = "year"
REGION_COLUMN = "region"

COLUMN_NAMES = (
    YEAR_COLUMN,
    REGION_COLUMN,
    "npg",
    "birth_rate",
    "death_rate",
    "gdw",
    "urbanization",
)

NUMERIC_COLUMNS = tuple(
    name for name in COLUMN_NAMES if name != REGION_COLUMN
)

CellValue = Union[str, int, float, None]
DataRow = Dict[str, CellValue]
Dataset = List[DataRow]
Statistics = Dict[str, float]
Percentiles = List[Tuple[int, float]]
