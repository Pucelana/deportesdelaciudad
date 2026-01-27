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

// Segunda función para calcular el porcentaje a la Champion y Campeón
const filas = document.querySelectorAll("#tablaChampionRecoletas tbody tr");
const partidosTotales = 30; // Cambiado a 30 partidos en la temporada
const puntosPorGanar = 2; // Cambiado a 3 puntos por partido ganado
const proximidadFija = 99; // Ajusta este valor según tus necesidades
const equipos = [];
let index = 1;
filas.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.champ-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.champ-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso = Math.round((proximidadFija / 100) * partidosTotales * puntosPorGanar);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan = Math.max(0, puntosParaAscenso - puntosActuales);
    const proximidadDeAscenso = Math.min(((puntosParaAscenso - puntosQueFaltan) / puntosParaAscenso) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso = partidosTotales - partidosJugados;
    const partidosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesAscenso * puntosPorGanar, puntosParaAscenso);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 4, puntosParaAscenso);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -6, puntosParaAscenso);
    equipos.push({
        index:index,
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
const tabla = document.querySelector("#tablaChampionRecoletas tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor = '';
    if (equipoData.index <= 1) {
        claseColor = 'pos-ascen';
    } else if (equipoData.index <=16) {
        claseColor = 'pos-nada';
    }
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center ${claseColor}">${equipoData.index}</td>
    <td class="fw-bold text-center size_equipos2 text-white">${equipoData.equipo}</td>
    <td class="champ-jug fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="champ-act fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="champ-prox fw-bold text-center">${equipoData.proximidadDeAscenso}%</td>
    <td class="champ-mate fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="champ-opti fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="champ-pesi fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});

// Tercera función para calcular el porcentaje a la Europa League
const filas3 = document.querySelectorAll("#tablaEuropaRecoletas tbody tr");
const partidosTotales3 = 30; // Cambiado a 30 partidos en la temporada
const puntosPorGanar3 = 2; // Cambiado a 3 puntos por partido ganado
const proximidadFija3 = 75; // Ajusta este valor según tus necesidades
const equipos3 = [];
let index3 = 1;
filas3.forEach((fila, indice) => {
    const equipo3 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados3 = parseInt(fila.querySelector(`.euro-jug`).textContent);
    const puntosActuales3 = parseInt(fila.querySelector(`.euro-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso3 = Math.round((proximidadFija3 / 100) * partidosTotales3 * puntosPorGanar3);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan3 = Math.max(0, puntosParaAscenso3 - puntosActuales3);
    const proximidadDeAscenso3 = Math.min(((puntosParaAscenso3 - puntosQueFaltan3) / puntosParaAscenso3) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso3 = partidosTotales3 - partidosJugados3;
    const partidosGanadosMatematicos3 = Math.min(puntosActuales3 + partidosRestantesAscenso3 * puntosPorGanar3, puntosParaAscenso3);
    const partidosGanadosPesimistas3 = Math.min(partidosGanadosMatematicos3 - 3, puntosParaAscenso3);
    const partidosGanadosOptimistas3 = Math.min(partidosGanadosMatematicos3 -5, puntosParaAscenso3);
    equipos3.push({
        index3: index3,
        equipo3,
        partidosJugados3,
        puntosActuales3,
        proximidadDeAscenso3:Math.round(proximidadDeAscenso3),
        partidosGanadosMatematicos3,
        partidosGanadosOptimistas3,
        partidosGanadosPesimistas3
    });
    index3++
});
// Ordenar los equipos3 por proximidad descendente
equipos3.sort((a, b) => b.proximidadDeAscenso3 - a.proximidadDeAscenso3);
// Actualizar la tabla3 con los datos ordenados
const tabla3 = document.querySelector("#tablaEuropaRecoletas tbody");
tabla3.innerHTML = ""; // Limpiar la tabla3 antes de actualizar
equipos3.forEach((equipo3Data) => {
    const nuevaFila3 = document.createElement("tr");
    let claseColor3 = '';
    if (equipo3Data.index3 <= 1) {
        claseColor3 = 'pos-nada';
    }else if (equipo3Data.index3 <= 5) {
        claseColor3 = 'pos-ehfec'
    }else if (equipo3Data.index3 <=16) {
        claseColor3 = 'pos-nada';
    }
    nuevaFila3.innerHTML = `
    <td class="fw-bold text-center ${claseColor3}">${equipo3Data.index3}</td>
    <td class="fw-bold text-center size_equipos2 text-white">${equipo3Data.equipo3}</td>
    <td class="euro-jug fw-bold text-center">${equipo3Data.partidosJugados3}</td>
    <td class="euro-act fw-bold text-center">${equipo3Data.puntosActuales3}</td>
    <td class="euro-prox fw-bold text-center">${equipo3Data.proximidadDeAscenso3}%</td>
    <td class="euro-mate fw-bold text-center">${equipo3Data.partidosGanadosMatematicos3}</td>
    <td class="euro-opti fw-bold text-center">${equipo3Data.partidosGanadosOptimistas3}</td>
    <td class="euro-pesi fw-bold text-center">${equipo3Data.partidosGanadosPesimistas3}</td>
    `;
    tabla3.appendChild(nuevaFila3);
});

// Cuarta función para calcular el porcentaje a la Promoción del descenso
const filas1 = document.querySelectorAll("#tablaPromoRecoletas tbody tr");
const partidosTotales1 = 30; // Cambiado a 42 partidos en la temporada
const puntosPorGanar1 = 2; // Cambiado a 3 puntos por partido ganado
const proximidadFija1 = 56; // Ajusta este valor según tus necesidades
const equipo1s1 = [];
let index1 = 1;
filas1.forEach((fila, indice) => {
    const equipo1 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados1 = parseInt(fila.querySelector(`.promo-jug`).textContent);
    const puntosActuales1 = parseInt(fila.querySelector(`.promo-act`).textContent);

    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso1 = Math.round((proximidadFija1 / 100) * partidosTotales1 * puntosPorGanar1);

    // Calcular la proximidad de ascenso
    const puntosQueFaltan1 = Math.max(0, puntosParaAscenso1 - puntosActuales1);
    const proximidadDePlayOff = Math.min(((puntosParaAscenso1 - puntosQueFaltan1) / puntosParaAscenso1) * 100, 100);

    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso1 = partidosTotales1 - partidosJugados1;
    const partidosGanadosMatematicos1 = Math.min(puntosActuales1 + partidosRestantesAscenso1 * puntosPorGanar1, puntosParaAscenso1);
    const partidosGanadosPesimistas1 = Math.min(partidosGanadosMatematicos1 - 10, puntosParaAscenso1);
    const partidosGanadosOptimistas1 = Math.min(partidosGanadosMatematicos1 -12, puntosParaAscenso1);

    equipo1s1.push({
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
equipo1s1.sort((a, b) => b.proximidadDePlayOff - a.proximidadDePlayOff);
// Actualizar la tabla1 con los datos ordenados
const tabla1 = document.querySelector("#tablaPromoRecoletas tbody");
tabla1.innerHTML = ""; // Limpiar la tabla1 antes de actualizar
equipo1s1.forEach((equipo1Data) => {
    const nuevaFila1 = document.createElement("tr");
    let claseColor1 = '';
    if (equipo1Data.index1 <= 13) {
        claseColor1 = 'pos-nada';
    }else if (equipo1Data.index1 <= 14) {
        claseColor1 = 'pos-promo'
    }else if (equipo1Data.index1 <=16) {
        claseColor1 = 'pos-nada';
    }
    nuevaFila1.innerHTML = `
    <td class="fw-bold text-center ${claseColor1}">${equipo1Data.index1}</td>
    <td class="fw-bold text-center size_equipos2 text-white">${equipo1Data.equipo1}</td>
    <td class="promo-jug fw-bold text-center">${equipo1Data.partidosJugados1}</td>
    <td class="promo-act fw-bold text-center">${equipo1Data.puntosActuales1}</td>
    <td class="promo-prox fw-bold text-center">${equipo1Data.proximidadDePlayOff}%</td>
    <td class="promo-mate fw-bold text-center">${equipo1Data.partidosGanadosMatematicos1}</td>
    <td class="promo-opti fw-bold text-center">${equipo1Data.partidosGanadosOptimistas1}</td>
    <td class="promo-pesi fw-bold text-center">${equipo1Data.partidosGanadosPesimistas1}</td>
    `;
    tabla1.appendChild(nuevaFila1);
});

// Quinta función para calcular la permanencia al descenso
const filas2 = document.querySelectorAll("#tablaDescRecoletas tbody tr");
const partidosTotales2 = 30; // Cambiado a 42 partidos en la temporada
const puntosPorGanar2 = 2; // Cambiado a 3 puntos por partido ganado
const proximidadFijar2 = 55; // Ajusta este valor según tus necesidades
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
    const partidosGanadosPesimistas2 = Math.min(partidosGanadosMatematicos2 - 10, puntosPermanencia2);
    const partidosGanadosOptimistas2 = Math.min(partidosGanadosMatematicos2 -12, puntosPermanencia2);

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
const tabla2 = document.querySelector("#tablaDescRecoletas tbody");
tabla2.innerHTML = ""; // Limpiar la tabla2 antes de actualizar
equipos2.forEach((equipo2Data) => {
    const nuevaFila2 = document.createElement("tr");
    let claseColor2 = '';
    if (equipo2Data.index2 <= 14) {
        claseColor2 = 'pos-nada';
    }else if (equipo2Data.index2 <=16) {
        claseColor2 = 'pos-desc';
    }
    nuevaFila2.innerHTML = `
    <td class="fw-bold text-center ${claseColor2}">${equipo2Data.index2}</td>
    <td class="fw-bold text-center size_equipos2 text-white">${equipo2Data.equipo2}</td>
    <td class="desc-jug fw-bold text-center">${equipo2Data.partidosJugados2}</td>
    <td class="desc-act fw-bold text-center">${equipo2Data.puntosActuales2}</td>
    <td class="desc-prox fw-bold text-center">${equipo2Data.proxiPermanencia}%</td>
    <td class="desc-mate fw-bold text-center">${equipo2Data.partidosGanadosMatematicos2}</td>
    <td class="desc-opti fw-bold text-center">${equipo2Data.partidosGanadosOptimistas2}</td>
    <td class="desc-pesi fw-bold text-center">${equipo2Data.partidosGanadosPesimistas2}</td>
    `;
    tabla2.appendChild(nuevaFila2);
});