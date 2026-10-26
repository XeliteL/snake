"""Чтение и сохранение рекорда в файл."""

from settings import RECORD_FILE


def load_record():
    """Возвращает рекорд из файла или 0, если файла нет или он испорчен."""
    try:
        with open(RECORD_FILE, encoding='utf-8') as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0


def save_record(value):
    """Записывает рекорд в файл, перезаписывая старый."""
    with open(RECORD_FILE, 'w', encoding='utf-8') as file:
        file.write(str(value))
