const canvas_jornadas = document.getElementById("graficoJornadas");
if (canvas_jornadas) {
    const labels_jornadas = JSON.parse(canvas_jornadas.dataset.labels);
    const puntos_jornadas = JSON.parse(canvas_jornadas.dataset.puntos);
    new Chart(canvas_jornadas, {
    type: "line",

    data: {
        labels: labels_jornadas,
        datasets: [{
            label: "Puntos",
            data: puntos_jornadas,

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
                        size: 13
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
                
                suggestedMax: Math.max(...puntos_jornadas) + 5

            }

        }

    }

});
}