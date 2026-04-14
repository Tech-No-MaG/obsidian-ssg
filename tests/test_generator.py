"""
Тесты для модуля генерации HTML
"""

import pytest
from pathlib import Path
import sys
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.renderer.generator import SiteGenerator
from src.parser import Note


class TestSiteGenerator:
    """Тесты для генератора сайта"""
    
    @pytest.fixture
    def temp_dir(self):
        """Создаёт временную директорию"""
        dirpath = tempfile.mkdtemp()
        yield Path(dirpath)
        shutil.rmtree(dirpath)
    
    @pytest.fixture
    def sample_notes(self):
        """Пример заметок для тестов"""
        return {
            "note1": Note(
                slug="note1",
                title="Test Note",
                content="# Hello\nWorld",
                links=[],
                tags=["test"]
            )
        }
    
    @pytest.fixture
    def sample_config(self):
        """Пример конфигурации"""
        return {
            "site_title": "Test Wiki",
            "output_dir": "./dist"
        }
    
    def test_init(self, sample_notes, sample_config):
        """Инициализация генератора"""
        generator = SiteGenerator(sample_notes, sample_config)
        assert generator.notes == sample_notes
        assert generator.config == sample_config
    
    def test_convert_markdown_to_html(self, sample_notes, sample_config):
        """Конвертация Markdown в HTML"""
        generator = SiteGenerator(sample_notes, sample_config)
        html = generator.convert_markdown_to_html("# Hello\n\nWorld")
        assert "<h1>Hello</h1>" in html
        assert "World" in html
    
    def test_convert_markdown_with_link(self, sample_notes, sample_config):
        """Конвертация с вики-ссылкой"""
        notes = {
            "note1": Note(
                slug="note1",
                title="Note 1",
                content="Link to [[note2]]",
                links=[],
                tags=[]
            ),
            "note2": Note(
                slug="note2",
                title="Note 2",
                content="Content",
                links=[],
                tags=[]
            )
        }
        generator = SiteGenerator(notes, sample_config)
        html = generator.convert_markdown_to_html("Link to [[note2]]")
        assert 'href="note2.html"' in html
        assert 'class="wikilink"' in html
    
    def test_generate_search_index(self, sample_notes, sample_config, temp_dir):
        """Генерация поискового индекса"""
        sample_config["output_dir"] = str(temp_dir)
        generator = SiteGenerator(sample_notes, sample_config)
        generator.generate_search_index()
        
        # Проверяем, что файл создан
        search_file = temp_dir / "static" / "js" / "search-data.js"
        assert search_file.exists()
        
        # Проверяем содержимое
        content = search_file.read_text(encoding="utf-8")
        assert "const SEARCH_INDEX" in content
        assert "Test Note" in content