
function createChartConfig(title, yAxisLabel) {
    return {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: yAxisLabel,
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.3 // Makes the line a bit smoother
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 18
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second',
                        tooltipFormat: 'HH:mm:ss',
                        displayFormats: {
                            second: 'HH:mm:ss'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100, // For utilization percentages
                    title: {
                        display: true,
                        text: yAxisLabel
                    }
                }
            }
        }
    };
}

const cpuCtx = document.getElementById('cpuChart')?.getContext('2d');
const gpuCtx = document.getElementById('gpuChart')?.getContext('2d');
const gpuMemoryCtx = document.getElementById('gpuMemoryChart')?.getContext('2d');
const cpuChartConfig = createChartConfig('CPU Utilization', 'CPU Usage (%)');
const cpuChart = cpuCtx ? new Chart(cpuCtx, cpuChartConfig) : null;
const gpuChartConfig = createChartConfig('GPU Utilization', 'GPU Usage (%)');
const gpuChart = gpuCtx ? new Chart(gpuCtx, gpuChartConfig) : null;
const gpuMemoryChartConfig = createChartConfig('GPU Memory Usage', 'Memory Used (MB)');

if (gpuMemoryChartConfig) {
    delete gpuMemoryChartConfig.options.scales.y.max;
}
const gpuMemoryChart = gpuMemoryCtx ? new Chart(gpuMemoryCtx, gpuMemoryChartConfig) : null;

async function updateCharts() {
    try {
        const response = await fetch('/api/metrics');
        if (!response.ok) {
            console.error("Failed to fetch metrics.");
            return;
        }
        const dataPoints = await response.json();
        const maxDataPoints = 60;
        const labels = dataPoints.map(p => new Date(p.timestamp));
        const cpuData = dataPoints.map(p => p.cpu_utilization);
        const gpuData = dataPoints.map(p => p.gpu_utilization);
        const gpuMemoryData = dataPoints.map(p => p.gpu_memory_used);

        const update = (chart, data) => {
            if (!chart) return;
            chart.data.labels = labels;
            chart.data.datasets[0].data = data;
            chart.update('none'); // stops a full re-render of chart
        };
        update(cpuChart, cpuData);
        update(gpuChart, gpuData);
        update(gpuMemoryChart, gpuMemoryData);
    } catch (error) {
        console.error("Error updating charts:", error);
    }
}

window.addEventListener('load', () => {
    updateCharts();
    setInterval(updateCharts, 1000);
});
