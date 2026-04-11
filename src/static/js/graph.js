
//Интерактивная визуализация графа на D3.js


// Ждём загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    initGraph(graphData);
});

function initGraph(data) {
    // Размеры контейнера
    const container = document.getElementById('graph-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Создаём SVG
    const svg = d3.select('#graph-container')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('preserveAspectRatio', 'xMidYMid meet');

    // Добавляем группу для зума
    const g = svg.append('g');

    // Настройка зума
    const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on('zoom', (event) => {
            g.attr('transform', event.transform);
        });

    svg.call(zoom);

    // Создаём стрелки для связей (маркеры)
    svg.append('defs').selectAll('marker')
        .data(['end'])
        .enter().append('marker')
        .attr('id', 'arrow')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 25)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', '#3e3e42');

    // Создаём связи (линии)
    const link = g.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(data.links)
        .enter().append('line')
        .attr('class', 'graph-link');

    // Создаём узлы (круги + текст)
    const node = g.append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(data.nodes)
        .enter().append('g')
        .attr('class', 'graph-node')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    // Добавляем круги узлам
    node.append('circle')
        .attr('r', 8)
        .attr('fill', function(d) {
            // Цвет по тегам (если есть теги)
            if (d.tags && d.tags.length > 0) {
                return getNodeColor(d.tags[0]);
            }
            return '#7c3aed'; // Фиолетовый по умолчанию
        });

    // Добавляем подписи к узлам
    node.append('text')
        .attr('dx', 12)
        .attr('dy', 4)
        .text(function(d) {
            // Обрезаем длинные заголовки
            return d.title.length > 20 ? d.title.substring(0, 20) + '...' : d.title;
        });

    // Добавляем клик по узлу — переход к заметке
    node.on('click', function(event, d) {
        window.location.href = `${d.id}.html`;
    });

    // Подсветка при наведении
    node.on('mouseover', function(event, d) {
        // Подсвечиваем узел
        d3.select(this).classed('highlighted', true);
        
        // Подсвечиваем связанные узлы и связи
        const connectedLinks = data.links.filter(l => 
            l.source === d.id || l.target === d.id
        );
        
        connectedLinks.forEach(l => {
            d3.selectAll('.graph-link')
                .filter((_, i) => 
                    (data.links[i].source === l.source && data.links[i].target === l.target)
                )
                .classed('highlighted', true);
        });

        // Подсвечиваем связанные узлы
        const connectedNodes = new Set();
        connectedLinks.forEach(l => {
            connectedNodes.add(l.source);
            connectedNodes.add(l.target);
        });
        
        node.filter(n => connectedNodes.has(n.id))
            .classed('highlighted', true);
    });

    node.on('mouseout', function() {
        d3.select(this).classed('highlighted', false);
        d3.selectAll('.graph-link').classed('highlighted', false);
        node.classed('highlighted', false);
    });

    // Физическая симуляция
    const simulation = d3.forceSimulation(data.nodes)
        .force('link', d3.forceLink(data.links)
            .id(d => d.id)
            .distance(150))
        .force('charge', d3.forceManyBody().strength(-400))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(40));

    // Обновление позиций на каждом шаге симуляции
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('transform', d => `translate(${d.x},${d.y})`);
    });

    // Функции для drag-and-drop
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    // Функция для цвета узла по тегу
    function getNodeColor(tag) {
        const colors = {
            'локация': '#0ea5e9',
            'персонаж': '#f59e0b',
            'магия': '#8b5cf6',
            'сюжет': '#ef4444',
            'введение': '#10b981'
        };
        return colors[tag] || '#7c3aed';
    }
}