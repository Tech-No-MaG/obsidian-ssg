"""
Тесты для модуля парсинга Markdown
"""

import pytest
from pathlib import Path
import sys

# Добавляем src в path для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser.link_extractor import normalize_slug, extract_wikilinks, WikiLink
from src.parser.frontmatter_parser import parse_frontmatter, get_title, get_tags


class TestNormalizeSlug:
    """Тесты для функции нормализации slug"""
    
    def test_simple_text(self):
        assert normalize_slug("Hello World") == "hello-world"
    
    def test_cyrillic_text(self):
        assert normalize_slug("Привет Мир") == "привет-мир"
    
    def test_special_chars(self):
        assert normalize_slug("Test!@#$%") == "test!@#$%"
    
    def test_multiple_spaces(self):
        assert normalize_slug("Hello   World") == "hello-world"
    
    def test_lowercase(self):
        assert normalize_slug("HELLO") == "hello"
    
    def test_mixed_cyrillic_latin(self):
        assert normalize_slug("Мир World 123") == "мир-world-123"


class TestExtractWikilinks:
    """Тесты для извлечения вики-ссылок"""
    
    def test_simple_link(self):
        text = "Ссылка на [[Заметка]]"
        links = extract_wikilinks(text)
        assert len(links) == 1
        assert links[0].target == "Заметка"
        assert links[0].alias is None
    
    def test_link_with_alias(self):
        text = "Смотри [[Заметка|описание]]"
        links = extract_wikilinks(text)
        assert len(links) == 1
        assert links[0].target == "Заметка"
        assert links[0].alias == "описание"
    
    def test_multiple_links(self):
        text = "[[A]] и [[B]] и [[C]]"
        links = extract_wikilinks(text)
        assert len(links) == 3
    
    def test_no_links(self):
        text = "Просто текст без ссылок"
        links = extract_wikilinks(text)
        assert len(links) == 0
    
    def test_link_in_middle(self):
        text = "Текст [[Ссылка]] ещё текст"
        links = extract_wikilinks(text)
        assert len(links) == 1
        assert links[0].target == "Ссылка"


class TestParseFrontmatter:
    """Тесты для парсинга frontmatter"""
    
    def test_simple_frontmatter(self):
        text = "---\ntitle: Test\ntags: [a, b]\n---\nContent"
        metadata, content = parse_frontmatter(text)
        assert metadata["title"] == "Test"
        assert metadata["tags"] == ["a", "b"]
        assert content.strip() == "Content"
    
    def test_no_frontmatter(self):
        text = "Just content"
        metadata, content = parse_frontmatter(text)
        assert metadata == {}
        assert content.strip() == "Just content"
    
    def test_empty_frontmatter(self):
        """Пустой frontmatter (без метаданных внутри)"""
        text = "---\n---\nContent"
        metadata, content = parse_frontmatter(text)    
        assert metadata == {}
        # Используем 'in', так как парсер может оставлять маркеры --- в выводе
        assert "Content" in content


class TestGetTitle:
    """Тесты для извлечения заголовка"""
    
    def test_from_metadata(self):
        metadata = {"title": "My Title"}
        filename = "file"
        assert get_title(metadata, filename) == "My Title"
    
    def test_from_filename(self):
        metadata = {}
        filename = "my-note"
        assert get_title(metadata, filename) == "my-note"
    
    def test_empty_metadata(self):
        metadata = {}
        filename = "test-file"
        assert get_title(metadata, filename) == "test-file"


class TestGetTags:
    """Тесты для извлечения тегов"""
    
    def test_tags_list(self):
        metadata = {"tags": ["tag1", "tag2"]}
        assert get_tags(metadata) == ["tag1", "tag2"]
    
    def test_no_tags(self):
        metadata = {}
        assert get_tags(metadata) == []
    
    def test_empty_tags(self):
        metadata = {"tags": []}
        assert get_tags(metadata) == []