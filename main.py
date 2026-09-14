import console_input
import console_output
import csv_reader
import data_logic
import parser


def _select_file(state: dict) -> str:
    console_output.show_file_menu()
    method = console_input.read_file_method()
    if method == 0:
        return "exit"

    if method == 1:
        path = console_input.read_path()
    else:
        path = console_input.choose_file()
    if path is None:
        return "file"

    header, rows = csv_reader.read_csv(path)
    dataset = parser.parse_csv(header, rows)
    regions = data_logic.get_regions(dataset)
    columns = data_logic.get_numeric_columns(dataset)
    state.update(
        path=path, dataset=dataset, regions=regions, columns=columns,
        region="", rows=[],
    )
    return "region"


def _select_region(state: dict) -> str:
    console_output.show_regions(state["regions"])
    number = console_input.read_region(state["regions"])
    if number == 0:
        return "file"

    region = state["regions"][number - 1]
    rows = data_logic.get_region_data(state["dataset"], region)
    state.update(region=region, rows=rows)
    return "column"


def _show_report(state: dict, column: str) -> None:
    rows = state["rows"]
    statistics, percentiles, missing = data_logic.analyze_column(rows, column)
    console_output.show_selection(state["path"], state["region"], column)
    console_output.show_data(rows)
    console_output.show_counts(len(rows) - missing, missing)
    console_output.show_statistics(statistics)
    console_output.show_percentiles(percentiles)


def _select_column(state: dict) -> str:
    console_output.show_columns(state["columns"])
    column_id = console_input.read_column(state["columns"])
    if column_id == 0:
        return "region"

    column = state["columns"][column_id]
    _show_report(state, column)
    return "menu"


def _select_action() -> str:
    console_output.show_menu()
    action = console_input.read_menu()
    return ("exit", "file", "region", "column")[action]


def main() -> None:
    state = {}
    step = "file"
    handlers = {
        "file": _select_file,
        "region": _select_region,
        "column": _select_column,
    }

    while step != "exit":
        try:
            if step == "menu":
                step = _select_action()
            else:
                step = handlers[step](state)
        except EOFError:
            console_output.show_error(ValueError("Ввод недоступен. Программа завершена."))
            return
        except KeyboardInterrupt:
            console_output.show_error(ValueError("Ввод отменён. Повторите выбор."))
        except Exception as error:
            console_output.show_error(error)


if __name__ == "__main__":
    main()
