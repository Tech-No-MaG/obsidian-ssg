//Фильтрация заметок по тегам на главной странице
document.addEventListener('DOMContentLoaded', () => {
    const tagCloud = document.getElementById('tag-cloud');
    if (!tagCloud) return;

    // Собираем все уникальные теги
    const allTags = new Set();
    document.querySelectorAll('.filter-tag').forEach(el => allTags.add(el.dataset.tag));

    // облако тегов
    Array.from(allTags).sort().forEach(tag => {
        const span = document.createElement('span');
        span.className = 'tag cloud-tag';
        span.textContent = `#${tag}`;
        span.onclick = (e) => filterByTag(tag, e.target);
        tagCloud.appendChild(span);
    });

    // Функция фильтрации (глобальная, чтобы вызывалась из HTML)
    window.filterByTag = (tag, clickedElement) => {
        const items = document.querySelectorAll('.note-item');
        const isActive = clickedElement.classList.contains('active');

        // Сбрасываем активные теги
        document.querySelectorAll('.cloud-tag').forEach(t => t.classList.remove('active'));
        
        if (isActive) {
            // Если кликнули на уже активный — показываем всё
            items.forEach(item => item.style.display = 'flex');
        } else {
            // Иначе фильтруем
            clickedElement.classList.add('active');
            items.forEach(item => {
                const itemTags = item.dataset.tags.split(' ');
                item.style.display = itemTags.includes(tag) ? 'flex' : 'none';
            });
        }
    };
});