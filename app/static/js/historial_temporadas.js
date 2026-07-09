const canvas_temporadas = document.getElementById("graficoTemporadas");
if (canvas_temporadas) {
    const labels_temporadas = JSON.parse(canvas_temporadas.dataset.labels);
    const puntos_temporadas = JSON.parse(canvas_temporadas.dataset.puntos);
    new Chart(canvas_temporadas, {
    type: "line",

    data: {
        labels: labels_temporadas,
        datasets: [{
            label: "Puntos",
            data: puntos_temporadas,
            borderColor: "#672e8d",
            backgroundColor: "rgba(103,46,141,0.10)",
            borderWidth: 3,
            pointRadius: 5,
            pointHoverRadius: 8,
            pointBackgroundColor: "#ffffff",
            pointBorderColor: "#672e8d",
            pointBorderWidth: 3,
            tension: 0.35,
            fill: true
        }]
    },

    options: {

        responsive: true,

        plugins: {

            legend: {
                display: false
            },

            tooltip: {

                displayColors: false,

                callbacks: {

                    title: function(context){
                        return "Temporada " + context[0].label;
                    },

                    label: function(context){
                        return "Puntos: " + context.raw;
                    }

                }

            }

        },

        scales: {

            x: {

                ticks: {
                    font: {
                        size: 15
                    }
                },

                grid: {
                    display: false
                }

            },

            y: {

                beginAtZero: true,
                max:90,

                ticks: {
                    stepSize: 5,
                    font: {
                        size: 15
                    }
                },
                
                suggestedMax: Math.max(...puntos_temporadas) + 5

            }

        }

    }

});
}