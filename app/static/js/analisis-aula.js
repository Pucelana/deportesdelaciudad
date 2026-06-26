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
/*const filas = document.querySelectorAll("#tablaAscensoAula tbody tr");
const partidosTotales = 22; // Cambiado a 30 partidos en la temporada
const puntosPorGanar = 2; // Cambiado a 3 puntos por partido ganado
const proximidadFija = 44; // Ajusta este valor según tus necesidades
const equipos = [];
filas.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.fw-bold`).textContent;
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
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 7, puntosParaAscenso);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -11, puntosParaAscenso);
    equipos.push({
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadDeAscenso,
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
});
// Ordenar los equipos por proximidad descendente
equipos.sort((a, b) => b.proximidadDeAscenso - a.proximidadDeAscenso);
// Actualizar la tabla con los datos ordenados
const tabla = document.querySelector("#tablaAscensoAula tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="jugados1 fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="pts-act1 fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="proxi1 fw-bold text-center">${equipoData.proximidadDeAscenso.toFixed(2)}%</td>
    <td class="pts-mate1 fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="pts-opti1 fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="pts-pesi1 fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});*/

// Tercera función para calcular el porcentaje al Ascenso
const filas3 = document.querySelectorAll("#tablaAscAula tbody tr");
const partidosTotales3 = 26; // Cambiado a 26 partidos en la temporada
const puntosPorGanar3 = 2; // Cambiado a 2 puntos por partido ganado
const proximidadFija3 = 52; // Ajusta este valor según tus necesidades
const equipos3 = [];
let index3 = 1;
filas3.forEach((fila, indice) => {
    const equipo3 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados3 = parseInt(fila.querySelector(`.play-jug`).textContent);
    const puntosActuales3 = parseInt(fila.querySelector(`.play-act`).textContent);

    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso3 = Math.round((proximidadFija3 / 100) * partidosTotales3 * puntosPorGanar3);

    // Calcular la proximidad de ascenso
    const puntosQueFaltan3 = Math.max(0, puntosParaAscenso3 - puntosActuales3);
    const proximidadDePlayOff = Math.min(((puntosParaAscenso3 - puntosQueFaltan3) / puntosParaAscenso3) * 100, 100);

    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso3 = partidosTotales3 - partidosJugados3;
    const partidosGanadosMatematicos3 = Math.min(puntosActuales3 + partidosRestantesAscenso3 * puntosPorGanar3, puntosParaAscenso3);
    const partidosGanadosPesimistas3 = Math.min(partidosGanadosMatematicos3 - 2, puntosParaAscenso3);
    const partidosGanadosOptimistas3 = Math.min(partidosGanadosMatematicos3 -4, puntosParaAscenso3);

    equipos3.push({
        index3:index3,
        equipo3,
        partidosJugados3,
        puntosActuales3,
        proximidadDePlayOff:Math.round(proximidadDePlayOff),
        partidosGanadosMatematicos3,
        partidosGanadosOptimistas3,
        partidosGanadosPesimistas3
    });
    index3++
});
// Ordenar los equipo1s1 por proximidad descendente
equipos3.sort((a, b) => b.proximidadDePlayOff - a.proximidadDePlayOff);
// Actualizar la tabla1 con los datos ordenados
const tabla3 = document.querySelector("#tablaAscAula tbody");
tabla3.innerHTML = ""; // Limpiar la tabla1 antes de actualizar
equipos3.forEach((equipo3Data) => {
    const nuevaFila3 = document.createElement("tr");
    let claseColor3 = '';
    if (equipo3Data.index3 <= 1) {
        claseColor3 = 'pos-ascen';    
    } else if (equipo3Data.index3 <=14) {
        claseColor3 = 'pos-nada';
    }
    nuevaFila3.innerHTML = `
    <td class="text-center equipo-mobile ${claseColor3}">${equipo3Data.index3}</td>
    <td class="text-start size_equipos2 equipo-mobile">${equipo3Data.equipo3}</td>
    <td class="play-jug text-center equipo-mobile">${equipo3Data.partidosJugados3}</td>
    <td class="play-act text-center equipo-mobile">${equipo3Data.puntosActuales3}</td>
    <td class="play-prox text-center equipo-mobile">${equipo3Data.proximidadDePlayOff}%</td>
    <td class="play-mate text-center equipo-mobile">${equipo3Data.partidosGanadosMatematicos3}</td>
    <td class="play-opti text-center equipo-mobile d-none d-md-table-cell">${equipo3Data.partidosGanadosOptimistas3}</td>
    <td class="play-pesi text-center equipo-mobile d-none d-md-table-cell">${equipo3Data.partidosGanadosPesimistas3}</td>
    `;
    tabla3.appendChild(nuevaFila3);
});

// Tercera función para calcular el porcentaje a los PlayOff
const filas1 = document.querySelectorAll("#tablaPlayAula tbody tr");
const partidosTotales1 = 26; // Cambiado a 26 partidos en la temporada
const puntosPorGanar1 = 2; // Cambiado a 2 puntos por partido ganado
const proximidadFija1 = 52; // Ajusta este valor según tus necesidades
const equipos1 = [];
let index1 = 1;
filas1.forEach((fila, indice) => {
    const equipo1 = fila.querySelector(`.size_equipos2`).textContent;
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
    const partidosGanadosPesimistas1 = Math.min(partidosGanadosMatematicos1 - 2, puntosParaAscenso1);
    const partidosGanadosOptimistas1 = Math.min(partidosGanadosMatematicos1 -4, puntosParaAscenso1);

    equipos1.push({
        index1:index1,
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
const tabla1 = document.querySelector("#tablaPlayAula tbody");
tabla1.innerHTML = ""; // Limpiar la tabla1 antes de actualizar
equipos1.forEach((equipo1Data) => {
    const nuevaFila1 = document.createElement("tr");
    let claseColor1 = '';
    if (equipo1Data.index1 <= 1) {
        claseColor1 = 'pos-nada';
    } else if (equipo1Data.index1 <= 4){
        claseColor1 = 'pos-playoff';    
    } else if (equipo1Data.index1 <=14) {
        claseColor1 = 'pos-nada';
    }
    nuevaFila1.innerHTML = `
    <td class="text-center equipo-mobile ${claseColor1}">${equipo1Data.index1}</td>
    <td class="text-start size_equipos2 equipo-mobile">${equipo1Data.equipo1}</td>
    <td class="play-jug text-center equipo-mobile">${equipo1Data.partidosJugados1}</td>
    <td class="play-act text-center equipo-mobile">${equipo1Data.puntosActuales1}</td>
    <td class="play-prox text-center equipo-mobile">${equipo1Data.proximidadDePlayOff}%</td>
    <td class="play-mate text-center equipo-mobile">${equipo1Data.partidosGanadosMatematicos1}</td>
    <td class="play-opti text-center equipo-mobile d-none d-md-table-cell">${equipo1Data.partidosGanadosOptimistas1}</td>
    <td class="play-pesi text-center equipo-mobile d-none d-md-table-cell">${equipo1Data.partidosGanadosPesimistas1}</td>
    `;
    tabla1.appendChild(nuevaFila1);
});

// Cuarta función para calcular la permanencia
const filas2 = document.querySelectorAll("#tablaDescAula tbody tr");
const partidosTotales2 = 26; // Cambiado a 42 partidos en la temporada
const puntosPorGanar2 = 2; // Cambiado a 3 puntos por partido ganado
const proximidadFijar2 = 48; // Ajusta este valor según tus necesidades
const equipos2 = [];
let index2 = 1;
filas2.forEach((fila, indice) => {
    const equipo2 = fila.querySelector(`.size_equipos2`).textContent;
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
    const partidosGanadosPesimistas2 = Math.min(partidosGanadosMatematicos2 - 2, puntosPermanencia2);
    const partidosGanadosOptimistas2 = Math.min(partidosGanadosMatematicos2 -4, puntosPermanencia2);

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
const tabla2 = document.querySelector("#tablaDescAula tbody");
tabla2.innerHTML = ""; // Limpiar la tabla2 antes de actualizar
equipos2.forEach((equipo2Data) => {
    const nuevaFila2 = document.createElement("tr");
    let claseColor2 = '';
    if (equipo2Data.index2 <= 12) {
        claseColor2 = 'pos-nada';    
    } else if (equipo2Data.index2 <= 14) {
        claseColor2 = 'pos-desc';
    }
    nuevaFila2.innerHTML = `
    <td class="equipo-mobile text-center ${claseColor2}">${equipo2Data.index2}</td>
    <td class="text-start size_equipos2 equipo-mobile">${equipo2Data.equipo2}</td>
    <td class="desc-jug text-center equipo-mobile">${equipo2Data.partidosJugados2}</td>
    <td class="desc-act text-center equipo-mobile">${equipo2Data.puntosActuales2}</td>
    <td class="desc-prox text-center equipo-mobile">${equipo2Data.proxiPermanencia}%</td>
    <td class="desc-mate text-center equipo-mobile">${equipo2Data.partidosGanadosMatematicos2}</td>
    <td class="desc-opti text-center d-none d-md-table-cell">${equipo2Data.partidosGanadosOptimistas2}</td>
    <td class="desc-pesi text-center d-none d-md-table-cell">${equipo2Data.partidosGanadosPesimistas2}</td>
    `;
    tabla2.appendChild(nuevaFila2);
});