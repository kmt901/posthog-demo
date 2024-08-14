function selectPlan(plan) {
    document.querySelectorAll('.plan-card').forEach(card => {
        card.classList.remove('border-danger');
        card.querySelector('.overlay').style.opacity = '0.6';
    });
    const selectedCard = document.querySelector(`.plan-card[data-plan="${plan}"]`);
    if (selectedCard) {
        selectedCard.classList.add('border-danger');
        selectedCard.querySelector('.overlay').style.opacity = '0';
    }

    console.log("Plan selected: " + plan);

    showConfirmationModal(plan);
}

function showConfirmationModal(plan) {
    const modal = $('#confirmationModal');
    const modalBody = $('#modalBody');
    modalBody.text(`Are you sure you want to change your plan to ${plan}?`);
    
    $('#confirmButton').off('click').on('click', function() {
        updatePlan(plan);
        modal.modal('hide');
    });
    
    modal.modal('show');
}

function updatePlan(plan) {
    const formData = new FormData();
    formData.append('plan', plan);
    formData.append('csrf_token', csrfToken); 

    fetch('/profile', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken  
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessModal(plan);
            document.getElementById('currentPlan').textContent = plan;
        } else {
            showErrorModal();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorModal();
    });
}

function showSuccessModal(plan) {
    const modal = $('#confirmationModal');
    const modalBody = $('#modalBody');
    modalBody.text(`Your plan has been successfully updated to ${plan}!`);
    $('#confirmButton').hide();
    modal.modal('show');
}

function showErrorModal() {
    const modal = $('#confirmationModal');
    const modalBody = $('#modalBody');
    modalBody.text('Failed to update plan. Please try again.');
    $('#confirmButton').hide();
    modal.modal('show');
}

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

    const currentPlan = document.getElementById('currentPlan').textContent.trim();
    if (currentPlan) {
        const currentPlanCard = document.querySelector(`.plan-card[data-plan="${currentPlan}"]`);
        if (currentPlanCard) {
            currentPlanCard.classList.add('border-danger');
            currentPlanCard.querySelector('.overlay').style.opacity = '0';
        }
    }
});