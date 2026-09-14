import typing


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

CellValue = typing.Union[str, int, float, None]
DataRow = typing.Dict[str, CellValue]
Dataset = typing.List[DataRow]
Statistics = typing.Dict[str, float]
Percentiles = typing.List[typing.Tuple[int, float]]
