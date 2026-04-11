"""
Модуль для генерации HTML-страниц из данных.
Использует Jinja2 для шаблонов и Markdown для текста.
"""

import markdown
import re
import shutil
import json  # импорт JSON
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Импортируем slug-функцию, чтобы проверять ссылки
from src.parser.link_extractor import normalize_slug


class SiteGenerator:
    """Класс, который генерирует весь сайт"""
    
    def __init__(self, notes, config):
        """
        Инициализация генератора.
        
        Args:
            notes: Словарь {slug: Note} со всеми заметками
            config: Словарь с настройками из config.yaml
        """
        self.notes = notes
        self.config = config
        self.output_dir = Path(config.get("output_dir", "./dist"))
        
        # Настраиваем папку для шаблонов Jinja2
        template_dir = Path("src/templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def convert_markdown_to_html(self, text):
        """Превращает Markdown текст в HTML и обрабатывает [[ссылки]]"""
        
        # 1. Сначала заменяем [[вики-ссылки]] на <a> теги
        def replace_wikilink(match):
            target = match.group(1).strip()
            alias = match.group(2).strip() if match.group(2) else target
            slug = normalize_slug(target)
            
            # Проверяем, есть ли такая заметка у нас
            if slug in self.notes:
                return f'<a href="{slug}.html" class="wikilink">{alias}</a>'
            else:
                return f'<a href="#" class="wikilink unresolved" title="Заметка не найдена: {target}">{alias}</a>'

        # Регулярка для [[Ссылка]] или [[Ссылка|Текст]]
        text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', replace_wikilink, text)
        
        # 2. Теперь конвертируем остаток Markdown в HTML
        md = markdown.Markdown(extensions=['extra', 'fenced_code'])
        return md.convert(text)

    def generate_all(self):
        """Главный метод — генерирует ВСЕ страницы сайта"""
        
        print(f"\n🎨 Начинаю генерацию HTML в папку {self.output_dir}...")
        
        # Создаем папку вывода, если нет
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Копируем CSS и JS в папку вывода
        static_src = Path("src/static")
        static_dst = self.output_dir / "static"
        if static_src.exists():
            shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
            print("   📂 Скопированы статические файлы (CSS, JS)")

        # ==========================================
        # 1. ГЕНЕРИРУЕМ СТРАНИЦЫ ЗАМЕТОК
        # ==========================================
        template_note = self.env.get_template("note.html")
        
        for slug, note in self.notes.items():
            # Подготовка данных
            note.html_content = self.convert_markdown_to_html(note.content)
            
            # Находим обратные ссылки (кто ссылается на эту заметку)
            backlinks = {}
            for other_slug, other_note in self.notes.items():
                if other_slug == slug: 
                    continue
                # Проверяем, есть ли ссылка на текущую заметку
                for link in other_note.links:
                    if normalize_slug(link.target) == slug:
                        backlinks[other_slug] = other_note
                        break
            
            # Рендерим HTML
            html = template_note.render(
                note=note,
                backlinks=backlinks,
                site_title=self.config.get("site_title", "My Wiki")
            )
            
            # Сохраняем файл
            output_file = self.output_dir / f"{slug}.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
        
        print(f"   📄 Сгенерировано {len(self.notes)} страниц заметок.")

        # ==========================================
        # 2. ГЕНЕРИРУЕМ ГЛАВНУЮ СТРАНИЦУ
        # ==========================================
        template_index = self.env.get_template("index.html")
        html_index = template_index.render(
            notes=self.notes,
            site_title=self.config.get("site_title", "My Wiki")
        )
        
        with open(self.output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_index)
        
        print("   🏠 Сгенерирована главная страница (index.html).")

        # ==========================================
        # 3. ГЕНЕРИРУЕМ СТРАНИЦУ ГРАФА
        # ==========================================
        # Загружаем graph.json (который создал Этап 2)
        graph_json_path = self.output_dir / "graph.json"
        if graph_json_path.exists():
            with open(graph_json_path, "r", encoding="utf-8") as f:
                graph_data = json.load(f)
            
            # Генерируем graph.html
            self._generate_graph_page(graph_data)
        else:
            print("   ⚠️  graph.json не найден, пропускаем генерацию графа.")
        
        # ==========================================
        # 4. ГЕНЕРАЦИЯ ПОИСКОВОГО ИНДЕКСА
        # ==========================================
        self.generate_search_index()
        
        # ==========================================
        # 5. ГЕНЕРИРУЕМ СТРАНИЦУ 404
        # ==========================================
        try:
            template_404 = self.env.get_template("404.html")
            html_404 = template_404.render(
                site_title=self.config.get("site_title", "My Wiki")
            )
            with open(self.output_dir / "404.html", "w", encoding="utf-8") as f:
                f.write(html_404)
            print("   📄 Сгенерирована страница 404.")
        except Exception as e:
            # Если шаблона нет — не страшно
            pass

        print("✅ Генерация завершена!")

    def _generate_graph_page(self, graph_data):
        """
        Генерирует страницу с интерактивным графом.
        
        Args:
            graph_data: Словарь с nodes и links из graph.json
        """
        # Загружаем шаблон graph.html
        template = self.env.get_template("graph.html")
        
        # Рендерим HTML, передавая данные графа
        html = template.render(
            nodes=graph_data["nodes"],
            links=graph_data["links"],
            site_title=self.config.get("site_title", "My Wiki")
        )
        
        # Сохраняем файл
        with open(self.output_dir / "graph.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"   🕸️  Сгенерирована страница графа (graph.html).")

    def generate_search_index(self):
        """Создаёт JS-файл с поисковым индексом"""
        search_items = []
        for slug, note in self.notes.items():
            search_items.append({
                "slug": slug,
                "title": note.title,
                "content": note.content,
                "tags": note.tags
            })
        
        # Формируем JS-константу
        js_content = f"const SEARCH_INDEX = {json.dumps(search_items, ensure_ascii=False, indent=2)};"
        
        # Сохраняем в папку статики
        output_path = self.output_dir / "static/js/search-data.js"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(js_content)
            
        print(f"   🔍 Создан поисковый индекс ({len(search_items)} заметок).")