"""
Тесты для модуля построения графа
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parser import Note
from src.graph.builder import build_graph
from src.parser.link_extractor import WikiLink


class TestBuildGraph:
    """Тесты для построения графа"""
    
    def test_empty_notes(self):
        notes = {}
        graph = build_graph(notes)
        assert graph.number_of_nodes() == 0
        assert graph.number_of_edges() == 0
    
    def test_single_node(self):
        notes = {
            "note1": Note(
                slug="note1",
                title="Note 1",
                content="Content",
                links=[],
                tags=[]
            )
        }
        graph = build_graph(notes)
        assert graph.number_of_nodes() == 1
        assert graph.number_of_edges() == 0
    
    def test_two_nodes_with_link(self):
        notes = {
            "note1": Note(
                slug="note1",
                title="Note 1",
                content="Content",
                links=[WikiLink(raw="[[note2]]", target="note2", alias=None)],
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
        graph = build_graph(notes)
        assert graph.number_of_nodes() == 2
        assert graph.number_of_edges() == 1
        assert graph.has_edge("note1", "note2")
    
    def test_bidirectional_links(self):
        notes = {
            "note1": Note(
                slug="note1",
                title="Note 1",
                content="Content",
                links=[WikiLink(raw="[[note2]]", target="note2", alias=None)],
                tags=[]
            ),
            "note2": Note(
                slug="note2",
                title="Note 2",
                content="Content",
                links=[WikiLink(raw="[[note1]]", target="note1", alias=None)],
                tags=[]
            )
        }
        graph = build_graph(notes)
        assert graph.number_of_nodes() == 2
        assert graph.number_of_edges() == 2
        assert graph.has_edge("note1", "note2")
        assert graph.has_edge("note2", "note1")
    
    def test_broken_link(self):
        notes = {
            "note1": Note(
                slug="note1",
                title="Note 1",
                content="Content",
                links=[WikiLink(raw="[[nonexistent]]", target="nonexistent", alias=None)],
                tags=[]
            )
        }
        graph = build_graph(notes)
        assert graph.number_of_nodes() == 1
        assert graph.number_of_edges() == 0  # Ссылка не создана
    
    def test_node_metadata(self):
        notes = {
            "note1": Note(
                slug="note1",
                title="My Title",
                content="Content",
                links=[],
                tags=["tag1", "tag2"]
            )
        }
        graph = build_graph(notes)
        node_data = graph.nodes["note1"]
        assert node_data["title"] == "My Title"
        assert node_data["tags"] == ["tag1", "tag2"]