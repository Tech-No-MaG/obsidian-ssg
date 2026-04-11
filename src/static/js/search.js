// Живой поиск по сайту
 
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('global-search');
    const resultsDropdown = document.getElementById('search-results');
    
    // Если на странице нет поиска или индекса — выходим
    if (!searchInput || typeof SEARCH_INDEX === 'undefined') return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        resultsDropdown.innerHTML = '';
        
        if (query.length < 2) {
            resultsDropdown.style.display = 'none';
            return;
        }

        // Фильтруем индекс
        const matches = SEARCH_INDEX.filter(item =>
            item.title.toLowerCase().includes(query) ||
            item.content.toLowerCase().includes(query) ||
            item.tags.some(tag => tag.toLowerCase().includes(query))
        ).slice(0, 8); // Максимум 8 результатов

        if (matches.length > 0) {
            resultsDropdown.style.display = 'block';
            matches.forEach(item => {
                const div = document.createElement('div');
                div.className = 'search-result-item';
                // Подсвечиваем совпадение в заголовке
                div.innerHTML = `<strong>${highlightMatch(item.title, query)}</strong> <small>#${item.tags.join(', #')}</small>`;
                div.onclick = () => window.location.href = `${item.slug}.html`;
                resultsDropdown.appendChild(div);
            });
        } else {
            resultsDropdown.style.display = 'none';
        }
    });

    // Закрываем дропдаун при клике вне поля
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
            resultsDropdown.style.display = 'none';
        }
    });

    function highlightMatch(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
});