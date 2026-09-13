import csv


def get_error_message(error: Exception) -> str:
    if isinstance(error, FileNotFoundError):
        return "Файл не найден. Проверьте путь и выберите файл повторно."

    if isinstance(error, IsADirectoryError):
        return "Вместо файла выбрана папка. Укажите CSV-файл."

    if isinstance(error, PermissionError):
        return "Нет доступа к файлу. Проверьте права доступа или выберите другой файл."

    if isinstance(error, UnicodeError):
        return "Не удалось прочитать текст файла. Проверьте его кодировку."

    if isinstance(error, csv.Error):
        return "Некорректный формат CSV. Проверьте разделители, кавычки и строки файла."

    if isinstance(error, ValueError):
        return str(error) or "Введено некорректное значение. Повторите ввод."

    if isinstance(error, OSError):
        return "Не удалось прочитать файл. Проверьте его доступность и повторите выбор."

    return "Произошла непредвиденная ошибка."
