let grafico2 = null;
const canvas_jornadas = document.getElementById("graficoJornadas");

if (canvas_jornadas) {

    const labels = JSON.parse(canvas_jornadas.getAttribute("data-labels"));
    const datasets = JSON.parse(canvas_jornadas.getAttribute("data-datasets"));

    grafico2 =new Chart(canvas_jornadas, {

        type: "line",

        data: {
            labels: labels,
            datasets: datasets
        },

        options: {

            responsive: true,

            plugins: {

                legend: {
                    display: true,
                    labels: {
                        font: {
                            size: 13
                        }
                    }
                },

                tooltip: {
                    mode: "index",
                    intersect: false
                }

            },

            interaction: {
                mode: "index",
                intersect: false
            },

            scales: {

                x: {
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                },

                y: {

                    beginAtZero: true,

                    ticks: {
                        stepSize: 5,
                        font: {
                            size: 15
                        }
                    }

                }

            }

        }

    });
    document.querySelectorAll(".temporada-check").forEach(check => {

    check.addEventListener("change", function(){

        const indice = Number(this.dataset.index);

        grafico2.data.datasets[indice].hidden = !this.checked;

        grafico2.update();

    });

});

}

