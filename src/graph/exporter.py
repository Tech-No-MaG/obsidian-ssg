"""
Модуль для экспорта графа в JSON-формат для фронтенда.
"""

import json
from pathlib import Path
import networkx as nx


def export_graph(G: nx.DiGraph, output_dir: Path):
    """
    Экспортирует граф в файл graph.json.
    
    Формат JSON:
    {
        "nodes": [{"id": "slug", "title": "...", "tags": [...]}],
        "links": [{"source": "slug1", "target": "slug2"}]
    }
    
    Args:
        G: Объект графа networkx
        output_dir: Папка для сохранения (из конфига)
    """
    # Создаём папку, если её нет
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Собираем данные об узлах
    nodes_data = []
    for node, data in G.nodes(data=True):
        nodes_data.append({
            "id": node,
            "title": data.get("title", node),
            "tags": data.get("tags", [])
        })
    
    # 2. Собираем данные о рёбрах
    links_data = []
    for source, target in G.edges():
        links_data.append({
            "source": source,
            "target": target
        })
    
    # 3. Формируем итоговый JSON
    graph_json = {
        "nodes": nodes_data,
        "links": links_data
    }
    
    # 4. Сохраняем в файл
    output_path = output_dir / "graph.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph_json, f, ensure_ascii=False, indent=2)
    
    print(f"🕸️  Граф сохранён в {output_path}")
    print(f"   Узлов: {len(nodes_data)}, Связей: {len(links_data)}")