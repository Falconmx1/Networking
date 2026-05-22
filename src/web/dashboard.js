const socket = io();

let trafficChart = null;

socket.on('connect', () => {
    document.getElementById('connection-status').innerHTML = '✅ Conectado';
    document.getElementById('connection-status').style.color = '#00b894';
});

socket.on('disconnect', () => {
    document.getElementById('connection-status').innerHTML = '❌ Desconectado';
    document.getElementById('connection-status').style.color = '#d63031';
});

socket.on('network_stats', (data) => {
    updateTrafficChart(data);
});

socket.on('system_stats', (data) => {
    document.getElementById('cpu-usage').textContent = data.cpu;
    document.getElementById('cpu-bar').style.width = data.cpu + '%';
    document.getElementById('ram-usage').textContent = data.ram;
    document.getElementById('ram-bar').style.width = data.ram + '%';
});

socket.on('connections', (connections) => {
    const tbody = document.querySelector('#connections-table tbody');
    tbody.innerHTML = '';
    
    connections.forEach(conn => {
        const row = tbody.insertRow();
        row.insertCell(0).textContent = conn.local_ip || 'N/A';
        row.insertCell(1).textContent = conn.remote_ip || 'N/A';
        row.insertCell(2).textContent = conn.status || 'UNKNOWN';
        row.insertCell(3).textContent = conn.pid || '-';
    });
});

function updateTrafficChart(data) {
    if (!trafficChart) {
        const ctx = document.getElementById('traffic-chart').getContext('2d');
        trafficChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    { label: 'Bytes enviados (MB)', data: [], borderColor: '#00b894', fill: false },
                    { label: 'Bytes recibidos (MB)', data: [], borderColor: '#e17055', fill: false }
                ]
            },
            options: {
                responsive: true,
                animation: false,
                scales: { y: { beginAtZero: true } }
            }
        });
    }
    
    const time = new Date().toLocaleTimeString();
    const sentMB = (data.bytes_sent / 1024 / 1024).toFixed(2);
    const recvMB = (data.bytes_recv / 1024 / 1024).toFixed(2);
    
    if (trafficChart.data.labels.length > 20) {
        trafficChart.data.labels.shift();
        trafficChart.data.datasets[0].data.shift();
        trafficChart.data.datasets[1].data.shift();
    }
    
    trafficChart.data.labels.push(time);
    trafficChart.data.datasets[0].data.push(sentMB);
    trafficChart.data.datasets[1].data.push(recvMB);
    trafficChart.update();
}

// Actualizar estadísticas cada 5 segundos vía API también
setInterval(() => {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            // Backup data via REST API
        });
}, 5000);
