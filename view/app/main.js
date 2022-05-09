const ctx = document.getElementById('barChart')
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: '# of money spent',
            data: [1500, 2541, 398, 1412, 945, 102, 2103],
            backgroundColor: ['#EFA159','#AE6D0C','#EFA159','#AE6D0C','#EFA159','#AE6D0C','#EFA159']
        }]
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                position: 'right'
            },
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
})
