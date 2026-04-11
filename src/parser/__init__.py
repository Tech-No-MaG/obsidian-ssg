"""
Главный модуль парсера.
Импортирует и объединяет функции из подмодулей.
"""

from .file_loader import find_markdown_files, read_file_content
from .frontmatter_parser import parse_frontmatter, get_title, get_tags
from .link_extractor import extract_wikilinks, normalize_slug, WikiLink

# Импортируем dataclasses для создания класса заметки
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Note:
    """
    Класс, представляющий одну заметку из Obsidian.
    """
    slug: str                    # Уникальный ID для URL (например, "papka-zametka")
    title: str                   # Заголовок заметки
    content: str                 # Текст заметки (без frontmatter)
    links: list[WikiLink]        # Список вики-ссылок внутри заметки
    tags: list[str] = field(default_factory=list)  # Список тегов
    file_path: Path | None = None  # Путь к файлу на диске (опционально)
    meta: dict = field(default_factory=dict)  # Все остальные метаданные из frontmatter


def parse_note(file_path: Path) -> Note:
    """
    Парсит один .md файл и возвращает объект Note.
    
    Args:
        file_path: Путь к файлу
    
    Returns:
        Объект Note с распарсенными данными
    """
    # 1. Читаем сырой контент
    raw_content = read_file_content(file_path)
    
    # 2. Парсим frontmatter → получаем метаданные и контент без YAML
    metadata, content = parse_frontmatter(raw_content)
    
    # 3. Извлекаем заголовок (из metadata или из имени файла)
    filename = file_path.stem  # Имя файла без расширения
    title = get_title(metadata, filename)
    
    # 4. Извлекаем теги
    tags = get_tags(metadata)
    
    # 5. Находим все вики-ссылки в контенте
    links = extract_wikilinks(content)
    
    # 6. Создаём slug из заголовка
    slug = normalize_slug(title)
    
    # 7. Возвращаем собранный объект
    return Note(
        slug=slug,
        title=title,
        content=content,
        links=links,
        tags=tags,
        file_path=file_path,
        meta=metadata
    )


def parse_vault(vault_path: str, exclude_folders: list[str] = None) -> dict[str, Note]:
    """
    Парсит ВСЮ папку с заметками (vault).
    
    Args:
        vault_path: Путь к корневой папке с .md файлами
        exclude_folders: Папки для исключения (например, [".obsidian"])
    
    Returns:
        Словарь {slug: Note} со всеми распарсенными заметками
    """
    # 1. Находим все .md файлы
    md_files = find_markdown_files(vault_path, exclude_folders)
    
    # 2. Парсим каждый файл
    notes = {}
    for file_path in md_files:
        note = parse_note(file_path)
        notes[note.slug] = note  # Используем slug как ключ
    
    return notes