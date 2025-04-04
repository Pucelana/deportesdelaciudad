// Primera función para calcular la clasificación y oredenar automáticamente
/*function calcularEstadisticas() {
    const tablaDatos = document.getElementById('tablaClasifValladFs');
    const filasDatos = Array.from(tablaDatos.querySelectorAll('tbody tr'));
    filasDatos.forEach(row => {
        const ptosFav = parseInt(row.querySelector('.favor').textContent);
        const ptosCont = parseInt(row.querySelector('.contra').textContent);
        const ganados = parseInt(row.querySelector('.ganados').textContent);
        const empatados = parseInt(row.querySelector('.empatados').textContent); // Añadido para empates
        const perdidos = parseInt(row.querySelector('.perdidos').textContent);
        const partidosJugados = ganados + empatados + perdidos; // Ajuste para incluir empates
        row.querySelector('.jugados').textContent = partidosJugados;
        const diferenciaPuntos = ptosFav - ptosCont;
        row.querySelector('.dife').textContent = diferenciaPuntos;

        // Ajuste en la fórmula para calcular puntos
        const puntos = ganados * 3 + empatados; // Cambio en la puntuación de victoria y empate
        row.querySelector('.puntos').textContent = puntos;
    });

    // Ordenar filas de datos según los puntos (PTS) de mayor a menor
    filasDatos.sort((a, b) => {
        const puntosA = parseInt(a.querySelector('.puntos').textContent);
        const puntosB = parseInt(b.querySelector('.puntos').textContent);
        const difPuntosA = parseInt(a.querySelector('.dife').textContent);
        const difPuntosB = parseInt(b.querySelector('.dife').textContent);
        if (puntosB !== puntosA) {
            return puntosB - puntosA; // Ordenar por puntos de mayor a menor
        } else {
            return difPuntosB - difPuntosA; // Si los puntos son iguales, ordenar por diferencia de puntos
        }
    });

    // Limpiar y reinsertar las filas ordenadas
    const tbody = tablaDatos.querySelector('tbody');
    tbody.innerHTML = '';
    filasDatos.forEach(fila => {
        tbody.appendChild(fila);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    calcularEstadisticas();
});*/

// Segunda función para calcular el porcentaje al ascenso
const filas = document.querySelectorAll("#tablaAscensoValladFs tbody tr");
const partidosTotales = 30; // Cambiado a 30 partidos en la temporada
const puntosPorGanar = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija = 88; // Ajusta este valor según tus necesidades
const equipos = [];
let index = 1;
filas.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.jugados1`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.pts-act1`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso = Math.round((proximidadFija / 100) * partidosTotales * puntosPorGanar);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan = Math.max(0, puntosParaAscenso - puntosActuales);
    const proximidadDeAscenso = Math.min(((puntosParaAscenso - puntosQueFaltan) / puntosParaAscenso) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso = partidosTotales - partidosJugados;
    const partidosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesAscenso * puntosPorGanar, puntosParaAscenso);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 5, puntosParaAscenso);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos - 9, puntosParaAscenso);
    equipos.push({
        index: index,
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadDeAscenso:Math.round(proximidadDeAscenso),
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
    index++
});
// Ordenar los equipos por proximidad descendente
equipos.sort((a, b) => b.proximidadDeAscenso - a.proximidadDeAscenso);
// Actualizar la tabla con los datos ordenados
const tabla = document.querySelector("#tablaAscensoValladFs tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor = '';
    if (equipoData.index <= 1) {
        claseColor = 'pos-ascen';
    } else if (equipoData.index <=16) {
        claseColor = 'pos-nada' 
    }
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center ${claseColor}">${equipoData.index}</td>
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="jugados1 fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="pts-act1 fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="proxi1 fw-bold text-center">${equipoData.proximidadDeAscenso}%</td>
    <td class="pts-mate1 fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="pts-opti1 fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="pts-pesi1 fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});

// Tercera función para calcular el porcentaje a la Copa
const filas1 = document.querySelectorAll("#tablaCopaValladFs tbody tr");
const partidosTotales1 = 30; // Cambiado a 42 partidos en la temporada
const puntosPorGanar1 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija1 = 70; // Ajusta este valor según tus necesidades
const equipos1 = [];
let index1 = 1;
filas1.forEach((fila, indice) => {
    const equipo1 = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados1 = parseInt(fila.querySelector(`.copa-jug`).textContent);
    const puntosActuales1 = parseInt(fila.querySelector(`.copa-act`).textContent);

    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso1 = Math.round((proximidadFija1 / 100) * partidosTotales1 * puntosPorGanar1);

    // Calcular la proximidad de ascenso
    const puntosQueFaltan1 = Math.max(0, puntosParaAscenso1 - puntosActuales1);
    const proximidadDePlayOff = Math.min(((puntosParaAscenso1 - puntosQueFaltan1) / puntosParaAscenso1) * 100, 100);

    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso1 = partidosTotales1 - partidosJugados1;
    const partidosGanadosMatematicos1 = Math.min(puntosActuales1 + partidosRestantesAscenso1 * puntosPorGanar1, puntosParaAscenso1);
    const partidosGanadosPesimistas1 = Math.min(partidosGanadosMatematicos1 - 21, puntosParaAscenso1);
    const partidosGanadosOptimistas1 = Math.min(partidosGanadosMatematicos1 -24, puntosParaAscenso1);

    equipos1.push({
        index1: index1,
        equipo1,
        partidosJugados1,
        puntosActuales1,
        proximidadDePlayOff:Math.round(proximidadDePlayOff),
        partidosGanadosMatematicos1,
        partidosGanadosOptimistas1,
        partidosGanadosPesimistas1
    });
    index1++
});
// Ordenar los equipo1s1 por proximidad descendente
equipos1.sort((a, b) => b.proximidadDePlayOff - a.proximidadDePlayOff);
// Actualizar la tabla1 con los datos ordenados
const tabla1 = document.querySelector("#tablaCopaValladFs tbody");
tabla1.innerHTML = ""; // Limpiar la tabla1 antes de actualizar
equipos1.forEach((equipo1Data) => {
    const nuevaFila1 = document.createElement("tr");
    let claseColor1 = '';
    if (equipo1Data.index1 <= 1) {
        claseColor1 = 'pos-nada';
    } else if (equipo1Data.index1 <= 2) {
        claseColor1 = 'pos-copa';
    } else if (equipo1Data.index1 <=16) {
        claseColor1 = 'pos-nada'
    }
    nuevaFila1.innerHTML = `
    <td class="fw-bold text-center ${claseColor1}">${equipo1Data.index1}</td>
    <td class="fw-bold text-center">${equipo1Data.equipo1}</td>
    <td class="copa-jug fw-bold text-center">${equipo1Data.partidosJugados1}</td>
    <td class="copa-act fw-bold text-center">${equipo1Data.puntosActuales1}</td>
    <td class="copa-prox fw-bold text-center">${equipo1Data.proximidadDePlayOff}%</td>
    <td class="copa-mate fw-bold text-center">${equipo1Data.partidosGanadosMatematicos1}</td>
    <td class="copa-opti fw-bold text-center">${equipo1Data.partidosGanadosOptimistas1}</td>
    <td class="copa-pesi fw-bold text-center">${equipo1Data.partidosGanadosPesimistas1}</td>
    `;
    tabla1.appendChild(nuevaFila1);
});

// Cuarta función para calcular la permanencia
const filas2 = document.querySelectorAll("#tablaDescValladFs tbody tr");
const partidosTotales2 = 30; // Cambiado a 42 partidos en la temporada
const puntosPorGanar2 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFijar2 = 60; // Ajusta este valor según tus necesidades
const equipos2 = [];
let index2 = 1;
filas2.forEach((fila, indice) => {
    const equipo2 = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados2 = parseInt(fila.querySelector(`.desc-jug`).textContent);
    const puntosActuales2 = parseInt(fila.querySelector(`.desc-act`).textContent);

    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosPermanencia2 = Math.round((proximidadFijar2 / 100) * partidosTotales2 * puntosPorGanar2);

    // Calcular la proximidad de ascenso
    const puntosQueFaltan2 = Math.max(0, puntosPermanencia2 - puntosActuales2);
    const proxiPermanencia = Math.min(((puntosPermanencia2 - puntosQueFaltan2) / puntosPermanencia2) * 100, 100);

    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesPermanencia = partidosTotales2 - partidosJugados2;
    const partidosGanadosMatematicos2 = Math.min(puntosActuales2 + partidosRestantesPermanencia * puntosPorGanar2, puntosPermanencia2);
    const partidosGanadosPesimistas2 = Math.min(partidosGanadosMatematicos2 - 1, puntosPermanencia2);
    const partidosGanadosOptimistas2 = Math.min(partidosGanadosMatematicos2 - 3, puntosPermanencia2);

    equipos2.push({
        index2: index2,
        equipo2,
        partidosJugados2,
        puntosActuales2,
        proxiPermanencia:Math.round(proxiPermanencia),
        partidosGanadosMatematicos2,
        partidosGanadosOptimistas2,
        partidosGanadosPesimistas2
    });
    index2++
});
// Ordenar los equipos2 por proximidad descendente
equipos2.sort((a, b) => b.proxiPermanencia - a.proxiPermanencia);
// Actualizar la tabla2 con los datos ordenados
const tabla2 = document.querySelector("#tablaDescValladFs tbody");
tabla2.innerHTML = ""; // Limpiar la tabla2 antes de actualizar
equipos2.forEach((equipo2Data) => {
    const nuevaFila2 = document.createElement("tr");
    let claseColor2 = '';
    if (equipo2Data.index2 <= 13) {
        claseColor2 = 'pos-nada';
    } else if (equipo2Data.index2 <= 16) {
        claseColor2 = 'pos-desc';
    }
    nuevaFila2.innerHTML = `
    <td class="fw-bold text-center ${claseColor2}">${equipo2Data.index2}</td>
    <td class="fw-bold text-center">${equipo2Data.equipo2}</td>
    <td class="desc-jug fw-bold text-center">${equipo2Data.partidosJugados2}</td>
    <td class="desc-act fw-bold text-center">${equipo2Data.puntosActuales2}</td>
    <td class="desc-prox fw-bold text-center">${equipo2Data.proxiPermanencia}%</td>
    <td class="desc-mate fw-bold text-center">${equipo2Data.partidosGanadosMatematicos2}</td>
    <td class="desc-opti fw-bold text-center">${equipo2Data.partidosGanadosOptimistas2}</td>
    <td class="desc-pesi fw-bold text-center">${equipo2Data.partidosGanadosPesimistas2}</td>
    `;
    tabla2.appendChild(nuevaFila2);
});