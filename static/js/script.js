document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".alert").forEach(function (alert) {
        window.setTimeout(function () {
            if (window.bootstrap) {
                bootstrap.Alert.getOrCreateInstance(alert).close();
            }
        }, 5000);
    });

    const chartCanvas = document.getElementById("trafficChart");
    if (chartCanvas && window.Chart) {
        new Chart(chartCanvas, {
            type: "doughnut",
            data: {
                labels: ["Low", "Moderate", "Heavy"],
                datasets: [{
                    data: [
                        Number(chartCanvas.dataset.low),
                        Number(chartCanvas.dataset.moderate),
                        Number(chartCanvas.dataset.heavy),
                    ],
                    backgroundColor: ["#198754", "#ffc107", "#dc3545"],
                    borderWidth: 0,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                    },
                },
            },
        });
    }
});
