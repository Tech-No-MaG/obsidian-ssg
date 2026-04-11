"""
Модуль для парсинга YAML frontmatter из Markdown-файлов.
"""

import re
import yaml
from typing import Optional


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Извлекает YAML-метаданные из начала Markdown-файла.
    
    Формат frontmatter:
    ---
    title: Моя заметка
    tags: [тег1, тег2]
    ---
    Остальной контент...
    
    Args:
        content: Полный текст .md файла
    
    Returns:
        Кортеж (словарь метаданных, контент без frontmatter)
    """
    # Регулярное выражение ищет блок между --- и ---
    pattern = r"^---\n(.*?)\n---\n(.*)"
    
    # re.DOTALL позволяет точке . захватывать переносы строк
    match = re.match(pattern, content, re.DOTALL)
    
    # Если frontmatter найден — парсим его
    if match:
        yaml_text = match.group(1)  # Текст между ---
        rest_content = match.group(2)  # Всё после закрывающего ---
        
        # yaml.safe_load превращает YAML-текст в словарь Python
        metadata = yaml.safe_load(yaml_text)
        
        # Если YAML был пустым — вернёт None, заменяем на пустой словарь
        return metadata or {}, rest_content
    
    # Если frontmatter нет — возвращаем пустые метаданные и весь контент
    return {}, content


def get_title(metadata: dict, fallback_filename: str) -> str:
    """
    Получает заголовок заметки: из metadata['title'] или из имени файла.
    
    Args:
        meta Словарь с метаданными из frontmatter
        fallback_filename: Имя файла без расширения (резервный вариант)
    
    Returns:
        Строка-заголовок
    """
    # Если в метаданных есть 'title' — используем его
    if metadata and "title" in metadata:
        return str(metadata["title"])
    
    # Иначе берём имя файла и убираем .md
    return fallback_filename


def get_tags(metadata: dict) -> list[str]:
    """
    Извлекает список тегов из метаданных.
    
    Args:
        meta Словарь с метаданными
    
    Returns:
        Список строк-тегов (или пустой список)
    """
    if not metadata or "tags" not in metadata:
        return []
    
    tags = metadata["tags"]
    
    # Теги могут быть списком или строкой — приводим к списку
    if isinstance(tags, str):
        return [tags]
    elif isinstance(tags, list):
        return [str(t) for t in tags]
    
    return []