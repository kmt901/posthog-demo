document.addEventListener('DOMContentLoaded', function () {
    const weekStats = JSON.parse(document.getElementById('weekStats').textContent);
    const monthStats = JSON.parse(document.getElementById('monthStats').textContent);
    const yearStats = JSON.parse(document.getElementById('yearStats').textContent);

    let currentStats = weekStats;

    function getGenreData(stats, genre) {
        return stats.filter(stat => stat.genre === genre);
    }

    const ctx = document.getElementById('moviesWatchedChart').getContext('2d');
    let moviesWatchedChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: getGenreData(weekStats, 'Action').map(stat => stat.date),
            datasets: [
                {
                    label: 'Action Movies',
                    data: getGenreData(weekStats, 'Action').map(stat => stat.count),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 1
                },
                {
                    label: 'Romantic Comedies',
                    data: getGenreData(weekStats, 'Romantic Comedy').map(stat => stat.count),
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function updateChart(timeFrame) {
        let stats;
        if (timeFrame === 'week') {
            stats = weekStats;
        } else if (timeFrame === 'month') {
            stats = monthStats;
        } else if (timeFrame === 'year') {
            stats = yearStats;
        }
        currentStats = stats;

        const actionData = getGenreData(currentStats, 'Action');
        const romComData = getGenreData(currentStats, 'Romantic Comedy');

        moviesWatchedChart.data.labels = actionData.map(stat => stat.date);
        moviesWatchedChart.data.datasets[0].data = actionData.map(stat => stat.count);
        moviesWatchedChart.data.datasets[1].data = romComData.map(stat => stat.count);
        moviesWatchedChart.update();
    }

    document.getElementById('timeFrameSelect').addEventListener('change', function () {
        let timeFrame = this.value;
        updateChart(timeFrame);
    });

    // Automatically highlight the user's current plan
    const currentPlan = document.getElementById('currentPlan').textContent;
    selectPlan(currentPlan);
});

function selectPlan(plan) {
    document.getElementById('plan_input').value = plan;
    document.querySelectorAll('.plan-card').forEach(card => {
        card.classList.remove('border-danger');
        card.querySelector('.overlay').style.opacity = '0.6';
    });
    const selectedCard = document.getElementById('card_' + plan.toLowerCase().replace('-', '_'));
    selectedCard.classList.add('border-danger');
    selectedCard.querySelector('.overlay').style.opacity = '0';
}
