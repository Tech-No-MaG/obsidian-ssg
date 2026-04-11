"""
Модуль для поиска и чтения Markdown-файлов.
"""

from pathlib import Path


def find_markdown_files(root_path: str, exclude_folders: list[str] = None) -> list[Path]:
    """
    Рекурсивно находит все .md файлы в папке.
    
    Args:
        root_path: Путь к корневой папке (например, "./test-vault")
        exclude_folders: Список папок для исключения (например, [".obsidian"])
    
    Returns:
        Список путей к .md файлам
    """
    # Если не передали список исключений — создаём пустой
    exclude = exclude_folders or []
    
    # Преобразуем строку пути в объект Path
    root = Path(root_path)
    
    # rglob ищет рекурсивно (во всех подпапках) файлы с расширением .md
    all_files = root.rglob("*.md")
    
    # Фильтруем: убираем файлы из исключённых папок
    result = []
    for file_path in all_files:
        # Проверяем, нет ли имени исключаемой папки в пути к файлу
        if not any(exc in file_path.parts for exc in exclude):
            result.append(file_path)
    
    return result


def read_file_content(file_path: Path) -> str:
    """
    Читает содержимое файла в кодировке UTF-8.
    
    Args:
        file_path: Путь к файлу
    
    Returns:
        Текст файла как строка
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()