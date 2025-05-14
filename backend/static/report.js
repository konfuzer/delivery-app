document.addEventListener("DOMContentLoaded", function () {
    const chartCtx = document.getElementById('deliveryChart').getContext('2d');
    let chart = null;
    let currentSort = { key: 'delivery_date', asc: true };
    let lastTableData = [];

    // Loader
    const loader = document.createElement('div');
    loader.className = 'loader';
    loader.innerHTML = '<div class="lds-dual-ring"></div>';
    document.body.appendChild(loader);
    loader.style.display = 'none';

    function showLoader() { loader.style.display = 'flex'; }
    function hideLoader() { loader.style.display = 'none'; }

    // Динамическое заполнение фильтров услуг и грузов
    function loadFilters() {
        fetch('/api/services/')
            .then(res => res.json())
            .then(data => {
                const select = document.getElementById('service-type');
                data.forEach(item => {
                    const opt = document.createElement('option');
                    opt.value = item.id;
                    opt.textContent = item.name;
                    select.appendChild(opt);
                });
            });
        fetch('/api/cargos/')
            .then(res => res.json())
            .then(data => {
                const select = document.getElementById('cargo-type');
                data.forEach(item => {
                    const opt = document.createElement('option');
                    opt.value = item.id;
                    opt.textContent = item.name;
                    select.appendChild(opt);
                });
            });
    }

    function fetchAndRender() {
        showLoader();
        const params = {
            start_date: document.getElementById("start-date").value,
            end_date: document.getElementById("end-date").value,
            service: document.getElementById("service-type").value,
            cargo: document.getElementById("cargo-type").value
        };
        const query = new URLSearchParams(params).toString();
        fetch(`/api/reports/report/?${query}`)
            .then(response => {
                if (!response.ok) throw new Error('Ошибка загрузки данных');
                return response.json();
            })
            .then(data => {
                lastTableData = data.table;
                renderChart(data.chart);
                renderTable(data.table);
                hideLoader();
            })
            .catch(err => {
                hideLoader();
                showError('Ошибка загрузки отчёта. Проверьте соединение или попробуйте позже.');
            });
    }

    function showError(msg) {
        let err = document.getElementById('report-error');
        if (!err) {
            err = document.createElement('div');
            err.id = 'report-error';
            err.className = 'report-error';
            document.querySelector('.container').prepend(err);
        }
        err.textContent = msg;
        err.style.display = 'block';
        setTimeout(() => { err.style.display = 'none'; }, 5000);
    }

    function formatDate(dateStr) {
        // Ожидается yyyy-mm-dd
        if (!dateStr) return '';
        const [y, m, d] = dateStr.split('-');
        return `${d}.${m}.${y}`;
    }

    function renderChart(data) {
        if (chart) chart.destroy();
        chart = new Chart(chartCtx, {
            type: 'line',
            data: {
                labels: data.labels.map(formatDate),
                datasets: [{
                    label: 'Количество доставок',
                    data: data.values,
                    borderColor: '#3EC6FF',
                    backgroundColor: 'rgba(62,198,255,0.10)',
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#3EC6FF',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Количество доставок', color: '#23262F', font: { size: 20, weight: 700 } }
                },
                scales: {
                    x: { ticks: { color: '#6B7280' }, grid: { color: '#E5E7EB' } },
                    y: { ticks: { color: '#6B7280' }, grid: { color: '#E5E7EB' } }
                }
            }
        });
    }

    function sortTableData(data, key, asc) {
        return [...data].sort((a, b) => {
            if (key === 'distance') {
                return asc ? a.distance - b.distance : b.distance - a.distance;
            }
            if (key === 'delivery_date') {
                return asc ? a.delivery_date.localeCompare(b.delivery_date) : b.delivery_date.localeCompare(a.delivery_date);
            }
            return asc ? (a[key] > b[key] ? 1 : -1) : (a[key] < b[key] ? 1 : -1);
        });
    }

    function renderTable(data) {
        const tbody = document.getElementById("delivery-table-body");
        tbody.innerHTML = "";
        const sorted = sortTableData(data, currentSort.key, currentSort.asc);
        sorted.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.total}</td>
                <td>${formatDate(row.delivery_date)}</td>
                <td>${row.transport_model}</td>
                <td>${row.service}</td>
                <td>${row.distance}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Сортировка по клику на заголовок
    document.querySelectorAll('.delivery-table th').forEach((th, idx) => {
        const keys = ['total', 'delivery_date', 'transport_model', 'service', 'distance'];
        if (idx === 0) return; // не сортируем по total
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
            const key = keys[idx];
            if (currentSort.key === key) {
                currentSort.asc = !currentSort.asc;
            } else {
                currentSort.key = key;
                currentSort.asc = true;
            }
            // Сбросить классы
            document.querySelectorAll('.delivery-table th').forEach((h, i) => {
                h.classList.remove('sorted-asc', 'sorted-desc');
                if (i === idx) h.classList.add(currentSort.asc ? 'sorted-asc' : 'sorted-desc');
            });
            renderTable(lastTableData);
        });
    });
    // Установить стрелку по умолчанию на дате
    document.getElementById('th-date').classList.add('sorted-asc');

    document.getElementById("apply-filters").addEventListener("click", fetchAndRender);
    loadFilters();
    fetchAndRender(); // начальная загрузка
});
