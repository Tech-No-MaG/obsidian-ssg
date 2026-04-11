#!/usr/bin/env python3
"""
Главный файл запуска проекта.
Отвечает за чтение аргументов командной строки, загрузку настроек
и запуск парсинга заметок.
"""

import argparse
import yaml
from pathlib import Path

# Импортируем парсер
from src.parser import parse_vault, Note

# Импортируем граф
from src.graph import build_graph, export_graph

# Сайт генератор
from src.renderer.generator import SiteGenerator

def load_config(config_path: str) -> dict:
    """Загружает YAML-файл и возвращает словарь настроек"""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"❌ Файл конфигурации не найден: {config_path}")
    
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def print_notes_summary(notes: dict[str, Note]):
    """
    Красиво выводит сводку по распарсенным заметкам.
    
    Args:
        notes: Словарь {slug: Note}
    """
    print(f"\n📚 Найдено заметок: {len(notes)}")
    print("=" * 60)
    
    for slug, note in notes.items():
        print(f"\n🔹 {note.title}")
        print(f"   Slug: {slug}")
        print(f"   Теги: {', '.join(note.tags) if note.tags else 'нет'}")
        print(f"   Ссылок: {len(note.links)}")
        
        # Показываем найденные вики-ссылки
        if note.links:
            link_texts = [f"[[{link.target}]]" for link in note.links[:3]]  # Первые 3
            if len(note.links) > 3:
                link_texts.append(f"... и ещё {len(note.links) - 3}")
            print(f"   Ссылки: {'  '.join(link_texts)}")
    
    print("\n" + "=" * 60)


def main():
    # Создаём "парсер" аргументов командной строки
    parser = argparse.ArgumentParser(
        description="🚀 Генератор статического сайта из Obsidian"
    )
    parser.add_argument(
        "--config", 
        default="config.yaml", 
        help="Путь к файлу конфигурации (по умолчанию: config.yaml)"
    )
    
    args = parser.parse_args()
    
    try:
        # 1. Загружаем конфиг
        config = load_config(args.config)
        print("✅ Конфиг загружен успешно!")
        
        # 2. Получаем пути из конфига
        vault_path = config.get("vault_path", "./test-vault")
        exclude = config.get("exclude_folders", [".obsidian", "attachments"])
        
        print(f"📂 Парсим вольт: {vault_path}")
        
        # 3. ЗАПУСКАЕМ ПАРСЕР
        notes = parse_vault(vault_path, exclude_folders=exclude)
        
        # 4. Показываем результат
        print_notes_summary(notes)
        
        # 🕸️ ПОСТРОЕНИЕ ГРАФА 
        print("\n🕸️  Построение графа связей...")
        graph = build_graph(notes)
        
        output_dir = Path(config.get("output_dir", "./dist"))
        export_graph(graph, output_dir)
        
        print("\n🎨 Запуск генератора сайтов...")
        generator = SiteGenerator(notes, config)
        generator.generate_all()        
        
        print("✅ Граф успешно экспортирован!")
        print(f"\n🎯 Этап 2 завершён! Найдено и распарсено {len(notes)} заметок.")
        print(f"📊 Построено связей: {graph.number_of_edges()}")
        print(f"\n🎉 Всё готово! Открой файл dist/index.html в браузере.")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        # Для отладки показываем полный текст ошибки
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()