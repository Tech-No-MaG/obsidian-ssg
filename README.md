# 🌐 Obsidian SSG

**Статический генератор сайтов для базы знаний Obsidian**

[![Deploy](https://github.com/Tech-No-Mag/obsidian-ssg/actions/workflows/deploy.yml/badge.svg)](https://github.com/Tech-No-Mag/obsidian-ssg/actions/workflows/deploy.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Описание

Obsidian SSG — это инструмент для автоматической генерации статического веб-сайта из коллекции Markdown-заметок в формате Obsidian. 

Проект преобразует вашу личную базу знаний в красивый, быстрый и удобный сайт с:
- **Интерактивным графом связей** между заметками
- **Живым поиском** по всему контенту
- **Фильтрацией по тегам**
- **Автоматическим деплоем** на GitHub Pages

**Демо:** [https://tech-no-mag.github.io/obsidian-ssg/](https://tech-no-mag.github.io/obsidian-ssg/)

---

## ✨ Возможности

###  Основные функции
- ✅ **Парсинг Markdown** — автоматическое извлечение метаданных (заголовки, теги)
- ✅ **Вики-ссылки** — поддержка `[[ссылок]]` как в Obsidian
- ✅ **Граф знаний** — визуализация связей на D3.js (drag & drop, зум)
- ✅ **Поиск** — мгновенный поиск по заголовкам, тексту и тегам
- ✅ **Теги** — облако тегов и фильтрация заметок
- ✅ **Обратные ссылки** — блок "связанные заметки"
- ✅ **404 страница** — обработка несуществующих страниц
- ✅ **Тёмная тема** — в стиле Obsidian

### 🚀 DevOps
- ✅ **CI/CD** — автоматическая сборка и деплой через GitHub Actions
- ✅ **GitHub Pages** — бесплатный хостинг
- ✅ **Модульная архитектура** — легко расширять

---

## 📦 Установка

### Требования
- Python 3.12+
- Git

### Быстрый старт

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Tech-No-Mag/obsidian-ssg.git
cd obsidian-ssg
```
2. Создайте виртуальное окружение:
```
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Настройте конфиг:
```
# Отредактируйте config.yaml под свои нужды
```
5. Запустите генератор:
```
python -m src.cli --config config.yaml
```
6. Откройте сайт:
   ```
   # Откройте dist/index.html в браузере
   ```

   ### 📁 Структура проекта
```
obsidian-ssg/
├── .github/workflows/      # CI/CD пайплайны
├── src/
│   ├── cli.py              # Точка входа
│   ├── parser/             # Парсинг Markdown
│   ├── graph/              # Построение графа
│   ├── renderer/           # Генерация HTML
│   ├── templates/          # Jinja2 шаблоны
│   └── static/             # CSS и JavaScript
├── test-vault/             # Примеры заметок
├── tests/                  # Unit тесты
├── config.yaml             # Конфигурация
└── requirements.txt        # Зависимости
```
