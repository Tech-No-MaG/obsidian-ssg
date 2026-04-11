"""
Модуль для построения графа связей между заметками.
Использует библиотеку networkx.
"""

import networkx as nx
from src.parser import Note, normalize_slug


def build_graph(notes: dict[str, Note]) -> nx.DiGraph:
    """
    Строит направленный граф на основе распарсенных заметок.
    
    Args:
        notes: Словарь {slug: Note} с распарсенными заметками
    
    Returns:
        Объект networkx.DiGraph с узлами и рёбрами
    """
    # Создаём направленный граф (Directed Graph)
    G = nx.DiGraph()
    
    # 1. Добавляем все заметки как узлы
    for slug, note in notes.items():
        G.add_node(
            slug,
            title=note.title,
            tags=note.tags
        )
    
    # 2. Добавляем рёбра (ссылки между заметками)
    for slug, note in notes.items():
        for link in note.links:
            # Нормализуем целевую ссылку в slug
            target_slug = normalize_slug(link.target)
            
            # Добавляем ребро только если целевая заметка существует
            if target_slug in notes:
                G.add_edge(slug, target_slug)
    
    return G