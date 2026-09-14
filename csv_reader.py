import csv
import pathlib
import stat
import typing


def _validate_path(path: typing.Union[str, pathlib.Path]) -> pathlib.Path:
    if isinstance(path, str) and not path.strip():
        raise ValueError("Путь к файлу не указан. Выберите CSV-файл.")

    file_path = pathlib.Path(path)
    file_mode = file_path.stat().st_mode

    if stat.S_ISDIR(file_mode):
        raise IsADirectoryError(f"Вместо файла выбрана папка: {file_path}")

    if not stat.S_ISREG(file_mode):
        raise ValueError("Указанный путь не ведёт к обычному файлу.")

    if file_path.suffix.lower() != ".csv":
        raise ValueError("Выберите файл с расширением .csv.")

    return file_path


def read_csv(
    path: typing.Union[str, pathlib.Path]
) -> typing.Tuple[typing.List[str], typing.List[typing.List[str]]]:
    file_path = _validate_path(path)

    with file_path.open() as file:
        reader = csv.reader(file, delimiter=",", strict=True)
        header = next(reader, None)

        if header is None:
            raise ValueError("CSV-файл пуст. Выберите файл с данными.")

        rows = list(reader)

    return header, rows
