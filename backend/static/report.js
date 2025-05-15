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

    function fetchAndRender() {
        showLoader();
        const params = {
            start_date: document.getElementById("start-date").value,
            end_date: document.getElementById("end-date").value,
            service: document.getElementById("service-type").value,
            cargo: document.getElementById("cargo-type").value
        };

        const query = new URLSearchParams(params).toString();

        fetch(`/api/reports/data/?${query}`)
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
                showError('Ошибка загрузки отчёта. Попробуйте позже.');
            });
    }

    function showError(msg) {
        let errBox = document.getElementById('report-error');
        if (!errBox) {
            errBox = document.createElement('div');
            errBox.id = 'report-error';
            errBox.className = 'report-error';
            document.querySelector('.container').prepend(errBox);
        }
        errBox.textContent = msg;
        errBox.style.display = 'block';
        setTimeout(() => { errBox.style.display = 'none'; }, 5000);
    }

    function formatDate(dateStr) {
        if (!dateStr) return '';
        const [y, m, d] = dateStr.split('-');
        return `${d.padStart(2, '0')}.${m.padStart(2, '0')}.${y}`;
    }

    function sortTableData(data, key, asc) {
        return [...data].sort((a, b) => {
            const valA = a[key];
            const valB = b[key];

            if (key === 'total' || key === 'distance_km') {
                return asc ? valA - valB : valB - valA;
            }

            if (key === 'delivery_date') {
                return asc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }

            return asc ? valA.localeCompare(valB) : valB.localeCompare(valA);
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
                <td>${row.packaging}</td>
                <td>${row.service}</td>
                <td>${row.status}</td>
                <td>${row.cargo_type}</td>
                <td>${parseFloat(row.distance_km).toFixed(2)}</td>
                <td>${row.created_by}</td>
            `;
            tbody.appendChild(tr);
        });

        addSortingArrows(); // обновляем стрелочки
    }

    function addSortingArrows() {
        const keys = ['total', 'delivery_date', 'transport_model', 'packaging', 'service', 'status', 'cargo_type', 'distance_km', 'created_by'];

        document.querySelectorAll('.delivery-table th').forEach((th, idx) => {
            th.classList.remove('sorted-asc', 'sorted-desc');

            if (idx < keys.length) {
                const key = keys[idx];
                if (key === currentSort.key) {
                    th.classList.add(currentSort.asc ? 'sorted-asc' : 'sorted-desc');
                }
                th.style.cursor = 'pointer';
            } else {
                th.style.cursor = 'default';
            }
        });
    }

    function setupHeaderClickHandlers() {
        const keys = ['total', 'delivery_date', 'transport_model', 'packaging', 'service', 'status', 'cargo_type', 'distance_km', 'created_by'];

        document.querySelectorAll('.delivery-table th').forEach((th, idx) => {
            if (idx >= keys.length) return;

            const key = keys[idx];
            th.style.cursor = 'pointer';
            th.addEventListener('click', () => {
                if (currentSort.key === key) {
                    currentSort.asc = !currentSort.asc;
                } else {
                    currentSort.key = key;
                    currentSort.asc = true;
                }

                renderTable(lastTableData);
            });
        });
    }

    function renderChart(data) {
        if (chart) chart.destroy();

        // Установка размеров canvas
        const chartContainer = document.querySelector('.chart-container');
        const width = chartContainer.offsetWidth; // Ширина контейнера
        const height = Math.min(width * 0.6, 400); // Высота — 60% ширины или максимум 400px

        chartCtx.canvas.width = width;
        chartCtx.canvas.height = height;

        chart = new Chart(chartCtx, {
            type: 'line',
            data: {
                labels: data.labels.map(formatDate),
                datasets: [{
                    label: 'Количество доставок',
                    data: data.total_count,
                    borderColor: '#3EC6FF',
                    backgroundColor: 'rgba(62,198,255,0.1)',
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#3EC6FF',
                    pointRadius: 5,
                    tension: 0.3,
                    fill: true
                }, {
                    label: 'Среднее расстояние',
                    data: data.avg_distance,
                    borderColor: '#FFCA28',
                    backgroundColor: 'rgba(255,202,40,0.1)',
                    pointRadius: 5,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Чтобы график масштабировался
                plugins: {
                    legend: { display: true },
                    title: { display: true, text: 'Количество и среднее расстояние' }
                },
                scales: {
                    x: {
                        ticks: { color: '#6B7280' },
                        grid: { color: '#E5E7EB' }
                    },
                    y: {
                        ticks: { color: '#6B7280' },
                        grid: { color: '#E5E7EB' }
                    }
                }
            }
        });
    }

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

    loadFilters();
    fetchAndRender();
    setupHeaderClickHandlers();
});