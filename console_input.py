import pathlib
import typing


def read_choice(prompt: str, choices: typing.Iterable[int]) -> int:
    try:
        choice = int(input(prompt).strip())
    except ValueError as error:
        raise ValueError("Введите целый номер пункта.") from error

    if choice not in choices:
        raise ValueError("Выберите номер из предложенного списка.")

    return choice


def read_file_method() -> int:
    return read_choice("Способ открытия: ", (0, 1, 2))


def read_path() -> str:
    path = input("Путь к CSV-файлу: ").strip()

    if len(path) >= 2 and path[0] == path[-1] and path[0] in "\"'":
        path = path[1:-1].strip()

    if not path or "\0" in path:
        raise ValueError("Укажите путь к CSV-файлу.")

    return path


def choose_file() -> typing.Optional[str]:
    try:
        import tkinter.filedialog
    except ImportError as error:
        raise ValueError("Диалог недоступен. Введите путь вручную.") from error

    try:
        folder = pathlib.Path(__file__).resolve().parent / "files_for_downloading"
        path = tkinter.filedialog.askopenfilename(
            title="Выберите CSV-файл",
            initialdir=str(folder),
            filetypes=[("CSV-файлы", "*.csv")],
        )
        return path or None
    except tkinter.TclError as error:
        raise ValueError("Не удалось открыть диалог. Введите путь вручную.") from error


def read_region(regions: typing.List[str]) -> int:
    return read_choice("Номер региона: ", range(len(regions) + 1))


def read_column(columns: typing.Dict[int, str]) -> int:
    return read_choice("ID колонки: ", [0, *columns])


def read_menu() -> int:
    return read_choice("Ваш выбор: ", (0, 1, 2, 3))
