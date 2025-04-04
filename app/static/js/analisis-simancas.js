// Primera función para calcular la clasificación y oredenar automáticamente
/*function calcularEstadisticas() {
    const tablaDatos = document.getElementById('tablaClasifSiman');
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
const filas = document.querySelectorAll("#tablaAscensoSimancas tbody tr");
const partidosTotales = 30; // Cambiado a 42 partidos en la temporada
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
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 4, puntosParaAscenso);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -8, puntosParaAscenso);
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
const tabla = document.querySelector("#tablaAscensoSimancas tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor = '';
    if (equipoData.index <= 1) {
        claseColor = 'pos-ascen';
    } else if (equipoData.index <= 16) {
        claseColor = 'pos-nada';
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

/*// Tercera función para calcular el porcentaje a los PlayOff
const filas1 = document.querySelectorAll("#tablaPlaySiman tbody tr");
const partidosTotales1 = 42; // Cambiado a 42 partidos en la temporada
const puntosPorGanar1 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija1 = 70; // Ajusta este valor según tus necesidades
const equipo1s1 = [];
filas1.forEach((fila, indice) => {
    const equipo1 = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados1 = parseInt(fila.querySelector(`.play-jug`).textContent);
    const puntosActuales1 = parseInt(fila.querySelector(`.play-act`).textContent);

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

    equipo1s1.push({
        equipo1,
        partidosJugados1,
        puntosActuales1,
        proximidadDePlayOff:Math.round(proximidadDePlayOff),
        partidosGanadosMatematicos1,
        partidosGanadosOptimistas1,
        partidosGanadosPesimistas1
    });
});
// Ordenar los equipo1s1 por proximidad descendente
equipo1s1.sort((a, b) => b.proximidadDePlayOff - a.proximidadDePlayOff);
// Actualizar la tabla1 con los datos ordenados
const tabla1 = document.querySelector("#tablaPlaySiman tbody");
tabla1.innerHTML = ""; // Limpiar la tabla1 antes de actualizar
equipo1s1.forEach((equipo1Data) => {
    const nuevaFila1 = document.createElement("tr");
    nuevaFila1.innerHTML = `
    <td class="fw-bold text-center">${equipo1Data.equipo1}</td>
    <td class="play-jug fw-bold text-center">${equipo1Data.partidosJugados1}</td>
    <td class="play-act fw-bold text-center">${equipo1Data.puntosActuales1}</td>
    <td class="play-prox fw-bold text-center">${equipo1Data.proximidadDePlayOff}%</td>
    <td class="play-mate fw-bold text-center">${equipo1Data.partidosGanadosMatematicos1}</td>
    <td class="play-opti fw-bold text-center">${equipo1Data.partidosGanadosOptimistas1}</td>
    <td class="play-pesi fw-bold text-center">${equipo1Data.partidosGanadosPesimistas1}</td>
    `;
    tabla1.appendChild(nuevaFila1);
});*/

// Cuarta función para calcular la permanencia
const filas2 = document.querySelectorAll("#tablaDescSimancas tbody tr");
const partidosTotales2 = 42; // Cambiado a 42 partidos en la temporada
const puntosPorGanar2 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFijar2 = 32; // Ajusta este valor según tus necesidades
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
    const partidosGanadosPesimistas2 = Math.min(partidosGanadosMatematicos2 - 13, puntosPermanencia2);
    const partidosGanadosOptimistas2 = Math.min(partidosGanadosMatematicos2 -20, puntosPermanencia2);
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
const tabla2 = document.querySelector("#tablaDescSimancas tbody");
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

// Quinta función para calcular el porcentaje al ascenso
/*const filas3 = document.querySelectorAll("#tablaAsceSimancas tbody tr");
const partidosTotales3 = 30; // Cambiado a 42 partidos en la temporada
const puntosPorGanar3 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija3 = 88; // Ajusta este valor según tus necesidades
const equipos3 = [];
filas3.forEach((fila, indice) => {
    const equipo3 = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados3 = parseInt(fila.querySelector(`.asce-jug`).textContent);
    const puntosActuales3 = parseInt(fila.querySelector(`.asce-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAsce= Math.round((proximidadFija3 / 100) * partidosTotales3 * puntosPorGanar3);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan3 = Math.max(0, puntosParaAsce - puntosActuales3);
    const proximidadDeAsce = Math.min(((puntosParaAsce - puntosQueFaltan3) / puntosParaAsce) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAsce = partidosTotales3 - partidosJugados3;
    const partidosGanadosMatematicos3 = Math.min(puntosActuales3 + partidosRestantesAsce * puntosPorGanar3, puntosParaAsce);
    const partidosGanadosPesimistas3 = Math.min(partidosGanadosMatematicos3 - 4, puntosParaAsce);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos3 -8, puntosParaAsce);
    equipos3.push({
        equipo3,
        partidosJugados3,
        puntosActuales3,
        proximidadDeAsce:Math.round(proximidadDeAsce),
        partidosGanadosMatematicos3,
        partidosGanadosOptimistas3,
        partidosGanadosPesimistas3
    });
});
// Ordenar los equipos por proximidad descendente
equipos3.sort((a, b) => b.proximidadDeAsce - a.proximidadDeAsce);
// Actualizar la tabla con los datos ordenados
const tabla3 = document.querySelector("#tablaAsceSimancas tbody");
tabla3.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos3.forEach((equipo3Data) => {
    const nuevaFila3 = document.createElement("tr");
    nuevaFila3.innerHTML = `
    <td class="fw-bold text-center">${equipo3Data.equipo}</td>
    <td class="asce-jug fw-bold text-center">${equipo3Data.partidosJugados3}</td>
    <td class="asce-act fw-bold text-center">${equipo3Data.puntosActuales3}</td>
    <td class="asce-proxi fw-bold text-center">${equipo3Data.proximidadDeAsce}%</td>
    <td class="asce-mate fw-bold text-center">${equipo3Data.partidosGanadosMatematicos3}</td>
    <td class="asce-opti fw-bold text-center">${equipo3Data.partidosGanadosOptimistas3}</td>
    <td class="asce-pesi fw-bold text-center">${equipo3Data.partidosGanadosPesimistas3}</td>
    `;
    tabla3.appendChild(nuevaFila3);
});*/

// Sexta función para calcular la permanencia
/*const filas4 = document.querySelectorAll("#tablaDesceSimancas tbody tr");
const partidosTotales4 = 42; // Cambiado a 42 partidos en la temporada
const puntosPorGanar4 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFijar4 = 32; // Ajusta este valor según tus necesidades
const equipos4 = [];
filas4.forEach((fila, indice) => {
    const equipo4 = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados4 = parseInt(fila.querySelector(`.desce-jug`).textContent);
    const puntosActuales4 = parseInt(fila.querySelector(`.desce-act`).textContent);

    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosPermanencia4 = Math.round((proximidadFijar4 / 100) * partidosTotales4 * puntosPorGanar4);

    // Calcular la proximidad de ascenso
    const puntosQueFaltan4 = Math.max(0, puntosPermanencia4 - puntosActuales4);
    const proxiPermanencia4 = Math.min(((puntosPermanencia4 - puntosQueFaltan4) / puntosPermanencia4) * 100, 100);

    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesPermanencia4 = partidosTotales4 - partidosJugados4;
    const partidosGanadosMatematicos4 = Math.min(puntosActuales4 + partidosRestantesPermanencia4 * puntosPorGanar4, puntosPermanencia4);
    const partidosGanadosPesimistas4 = Math.min(partidosGanadosMatematicos4 - 13, puntosPermanencia4);
    const partidosGanadosOptimistas4 = Math.min(partidosGanadosMatematicos4 -20, puntosPermanencia4);

    equipos4.push({
        equipo4,
        partidosJugados4,
        puntosActuales4,
        proxiPermanencia4:Math.round(proxiPermanencia4),
        partidosGanadosMatematicos4,
        partidosGanadosOptimistas4,
        partidosGanadosPesimistas4
    });
});
// Ordenar los equipos2 por proximidad desceendente
equipos4.sort((a, b) => b.proxiPermanencia4 - a.proxiPermanencia4);
// Actualizar la tabla2 con los datos ordenados
const tabla4 = document.querySelector("#tablaDesceSimancas tbody");
tabla4.innerHTML = ""; // Limpiar la tabla2 antes de actualizar
equipos4.forEach((equipo4Data) => {
    const nuevaFila4 = document.createElement("tr");
    nuevaFila4.innerHTML = `
    <td class="fw-bold text-center">${equipo4Data.equipo4}</td>
    <td class="desce-jug fw-bold text-center">${equipo4Data.partidosJugados4}</td>
    <td class="desce-act fw-bold text-center">${equipo4Data.puntosActuales4}</td>
    <td class="desce-prox fw-bold text-center">${equipo4Data.proxiPermanencia4}%</td>
    <td class="desce-mate fw-bold text-center">${equipo4Data.partidosGanadosMatematicos4}</td>
    <td class="desce-opti fw-bold text-center">${equipo4Data.partidosGanadosOptimistas4}</td>
    <td class="desce-pesi fw-bold text-center">${equipo4Data.partidosGanadosPesimistas4}</td>
    `;
    tabla4.appendChild(nuevaFila4);
});*/