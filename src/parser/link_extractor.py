"""
Модуль для извлечения вики-ссылок [[Like This]] из Markdown.
"""

import re
from dataclasses import dataclass


@dataclass
class WikiLink:
    """
    Класс для хранения информации о вики-ссылке.
    
    Примеры:
    [[Заметка]] → target="Заметка", alias=None
    [[Заметка|Текст]] → target="Заметка", alias="Текст"
    """
    target: str          # Целевая заметка (без алиаса)
    alias: str | None    # Отображаемый текст (если есть)
    raw: str             # Исходный текст ссылки, например "[[Заметка|Текст]]"


def extract_wikilinks(content: str) -> list[WikiLink]:
    """
    Находит все вики-ссылки вида [[Цель]] или [[Цель|Алиас]] в тексте.
    
    Args:
        content: Текст Markdown-файла
    
    Returns:
        Список объектов WikiLink
    """
    # Регулярное выражение:
    # \[\[       — открывающие [[ (экранируем, т.к. [ — спецсимвол)
    # ([^\]|]+)  — захватываем всё, кроме ] и | (это целевая заметка)
    # (?:\|([^\]]+))? — опционально: | и текст алиаса в незахватывающей группе
    # \]\]       — закрывающие ]]
    pattern = r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]"
    
    links = []
    
    # re.finditer находит ВСЕ совпадения и возвращает итератор
    for match in re.finditer(pattern, content):
        target = match.group(1).strip()  # Целевая заметка, убираем пробелы
        alias = match.group(2).strip() if match.group(2) else None  # Алиас если есть
        raw = match.group(0)  # Весь матч, например "[[Заметка|Текст]]"
        
        links.append(WikiLink(target=target, alias=alias, raw=raw))
    
    return links


def normalize_slug(title: str) -> str:
    """
    Преобразует название заметки или путь в "slug" — безопасный идентификатор для URL.
    
    Примеры:
    "Моя Заметка" → "moia-zametka"
    "Папка/Заметка" → "papka-zametka"
    "  Лишние пробелы  " → "lishnie-probely"
    
    Args:
        title: Заголовок или путь к заметке
    
    Returns:
        Строка slug в нижнем регистре, с дефисами вместо пробелов и слэшей
    """
    # Приводим к нижнему регистру
    slug = title.lower()
    
    # Заменяем слэши, пробелы, подчёркивания на дефисы
    slug = slug.replace("/", "-").replace(" ", "-").replace("_", "-")
    
    # Убираем повторяющиеся дефисы (если было "  " → "--")
    while "--" in slug:
        slug = slug.replace("--", "-")
    
    # Убираем дефисы в начале и конце
    return slug.strip("-")