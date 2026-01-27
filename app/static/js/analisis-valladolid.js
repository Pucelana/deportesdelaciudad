// Primera función para calcular la clasificación y oredenar automáticamente
function calcularEstadisticas() {
    const tablaDatos = document.getElementById('tablaClasifVallad2');
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
});

// Segunda función para calcular el porcentaje al ascenso
/*const filas = document.querySelectorAll("#tablaAscensoVallad tbody tr");
const partidosTotales = 42; // Cambiado a 42 partidos en la temporada
const puntosPorGanar = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija = 63; // Ajusta este valor según tus necesidades
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
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 3, puntosParaAscenso);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -5, puntosParaAscenso);
    equipos.push({
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadDeAscenso:Math.round(proximidadDeAscenso),
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
});
// Ordenar los equipos por proximidad descendente
equipos.sort((a, b) => b.proximidadDeAscenso - a.proximidadDeAscenso);
// Actualizar la tabla con los datos ordenados
const tabla = document.querySelector("#tablaAscensoVallad tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="jugados1 fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="pts-act1 fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="proxi1 fw-bold text-center">${equipoData.proximidadDeAscenso}%</td>
    <td class="pts-mate1 fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="pts-opti1 fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="pts-pesi1 fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});*/

// Tercera función para calcular el porcentaje a los PlayOff
/*const filas1 = document.querySelectorAll("#tablaPlayVallad tbody tr");
const partidosTotales1 = 42; // Cambiado a 42 partidos en la temporada
const puntosPorGanar1 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija1 = 55.5; // Ajusta este valor según tus necesidades
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
    const partidosGanadosPesimistas1 = Math.min(partidosGanadosMatematicos1 -3, puntosParaAscenso1);
    const partidosGanadosOptimistas1 = Math.min(partidosGanadosMatematicos1 -5, puntosParaAscenso1);

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
const tabla1 = document.querySelector("#tablaPlayVallad tbody");
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

// Cuarta función para calcular el descenso en la Liga Hypermotion
/*const filas2 = document.querySelectorAll("#tablaDescVallad tbody tr");
const partidosTotales2 = 42; // Cambiado a 42 partidos en la temporada
const puntosPorGanar2 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFijar2 = 46.5; // Ajusta este valor según tus necesidades
const equipos2 = [];
filas2.forEach((fila, indice) => {
    const equipo2 = fila.querySelector(`.fw-bold`).textContent;
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
    const partidosGanadosPesimistas2 = Math.min(partidosGanadosMatematicos2 -3, puntosPermanencia2);
    const partidosGanadosOptimistas2 = Math.min(partidosGanadosMatematicos2 -5, puntosPermanencia2);

    equipos2.push({
        equipo2,
        partidosJugados2,
        puntosActuales2,
        proxiPermanencia:Math.round(proxiPermanencia),
        partidosGanadosMatematicos2,
        partidosGanadosOptimistas2,
        partidosGanadosPesimistas2
    });
});
// Ordenar los equipos2 por proximidad descendente
equipos2.sort((a, b) => b.proxiPermanencia - a.proxiPermanencia);
// Actualizar la tabla2 con los datos ordenados
const tabla2 = document.querySelector("#tablaDescVallad tbody");
tabla2.innerHTML = ""; // Limpiar la tabla2 antes de actualizar
equipos2.forEach((equipo2Data) => {
    const nuevaFila2 = document.createElement("tr");
    nuevaFila2.innerHTML = `
    <td class="fw-bold text-center">${equipo2Data.equipo2}</td>
    <td class="desc-jug fw-bold text-center">${equipo2Data.partidosJugados2}</td>
    <td class="desc-act fw-bold text-center">${equipo2Data.puntosActuales2}</td>
    <td class="desc-prox fw-bold text-center">${equipo2Data.proxiPermanencia}%</td>
    <td class="desc-mate fw-bold text-center">${equipo2Data.partidosGanadosMatematicos2}</td>
    <td class="desc-opti fw-bold text-center">${equipo2Data.partidosGanadosOptimistas2}</td>
    <td class="desc-pesi fw-bold text-center">${equipo2Data.partidosGanadosPesimistas2}</td>
    `;
    tabla2.appendChild(nuevaFila2);
});*/

// Quinta función para calcular el porcentaje al PlayOff Ascenso
const filas3 = document.querySelectorAll("#tablaChampionsVallad tbody tr");
const partidosTotales3 = 42; // Cambiado a 38 partidos en la temporada
const puntosPorGanar3 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija3 = 57; // Ajusta este valor según tus necesidades
const equipos3 = [];
let index3 = 1;
filas3.forEach((fila) => {
    const equipo3 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados3 = parseInt(fila.querySelector(`.cham-jug`).textContent);
    const puntosActuales3 = parseInt(fila.querySelector(`.cham-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaChampions = Math.round((proximidadFija3 / 100) * partidosTotales3 * puntosPorGanar3);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan3 = Math.max(0, puntosParaChampions - puntosActuales3);
    const proximidadDeChampions = Math.min(((puntosParaChampions - puntosQueFaltan3) / puntosParaChampions) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesChampions = partidosTotales3 - partidosJugados3;
    const partidosGanadosMatematicos3 = Math.min(puntosActuales3 + partidosRestantesChampions * puntosPorGanar3, puntosParaChampions);
    const partidosGanadosPesimistas3 = Math.min(partidosGanadosMatematicos3 - 2, puntosParaChampions);
    const partidosGanadosOptimistas3 = Math.min(partidosGanadosMatematicos3 -3, puntosParaChampions);
    equipos3.push({
        index3: index3,
        equipo3,
        partidosJugados3,
        puntosActuales3,
        proximidadDeChampions:Math.round(proximidadDeChampions),
        partidosGanadosMatematicos3,
        partidosGanadosOptimistas3,
        partidosGanadosPesimistas3
    });
    index3++
});
// Ordenar los equipo3s3 por proximidad descendente
equipos3.sort((a, b) => b.proximidadDeChampions - a.proximidadDeChampions);
// Actualizar la tabla3 con los datos ordenados
const tabla3 = document.querySelector("#tablaChampionsVallad tbody");
tabla3.innerHTML = ""; // Limpiar la tabla3 antes de actualizar
equipos3.forEach((equipo3Data) => {
    const nuevaFila3 = document.createElement("tr");
    let claseColor3 = '';
    if (equipo3Data.index3 <= 2) {
        claseColor3 = 'pos-nada';
    } else if (equipo3Data.index3 <= 6){
        claseColor3 = 'pos-playoff';        
    } else if (equipo3Data.index3 <=22) {
        claseColor3 = 'pos-nada';
    }
    nuevaFila3.innerHTML = `
    <td class="fw-bold text-center ${claseColor3}">${equipo3Data.index3}</td>
    <td class="fw-bold text-center size_equipos2 text-white">${equipo3Data.equipo3}</td>
    <td class="cham-jug fw-bold text-center">${equipo3Data.partidosJugados3}</td>
    <td class="cham-act fw-bold text-center">${equipo3Data.puntosActuales3}</td>
    <td class="cham-proxi fw-bold text-center">${equipo3Data.proximidadDeChampions}%</td>
    <td class="cham-mate fw-bold text-center">${equipo3Data.partidosGanadosMatematicos3}</td>
    <td class="cham-opti fw-bold text-center">${equipo3Data.partidosGanadosOptimistas3}</td>
    <td class="cham-pesi fw-bold text-center">${equipo3Data.partidosGanadosPesimistas3}</td>
    `;
    tabla3.appendChild(nuevaFila3);
});

// Sexta función para calcular el porcentaje a la Europa League
/*const filas4 = document.querySelectorAll("#tablaEuropaVallad tbody tr");
const partidosTotales4 = 38; // Cambiado a 38 partidos en la temporada
const puntosPorGanar4 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija4 = 63; // Ajusta este valor según tus necesidades
const equipos4 = [];
let index4 = 1;
filas4.forEach((fila) => {
    const equipo4 = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados4 = parseInt(fila.querySelector(`.euro-jug`).textContent);
    const puntosActuales4 = parseInt(fila.querySelector(`.euro-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaEuropa = Math.round((proximidadFija4 / 100) * partidosTotales4 * puntosPorGanar4);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan4 = Math.max(0, puntosParaEuropa - puntosActuales4);
    const proximidadDeEuropa = Math.min(((puntosParaEuropa - puntosQueFaltan4) / puntosParaEuropa) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesEuropa = partidosTotales4 - partidosJugados4;
    const partidosGanadosMatematicos4 = Math.min(puntosActuales4 + partidosRestantesEuropa * puntosPorGanar4, puntosParaEuropa);
    const partidosGanadosPesimistas4 = Math.min(partidosGanadosMatematicos4 - 2, puntosParaEuropa);
    const partidosGanadosOptimistas4 = Math.min(partidosGanadosMatematicos4 -4, puntosParaEuropa);
    equipos4.push({
        index4: index4,
        equipo4,
        partidosJugados4,
        puntosActuales4,
        proximidadDeEuropa:Math.round(proximidadDeEuropa),
        partidosGanadosMatematicos4,
        partidosGanadosOptimistas4,
        partidosGanadosPesimistas4
    });
    index4++
});
// Ordenar los equipo3s3 por proximidad descendente
equipos4.sort((a, b) => b.proximidadDeEuropa - a.proximidadDeEuropa);
// Actualizar la tabla3 con los datos ordenados
const tabla4 = document.querySelector("#tablaEuropaVallad tbody");
tabla4.innerHTML = ""; // Limpiar la tabla3 antes de actualizar
equipos4.forEach((equipo4Data) => {
    const nuevaFila4 = document.createElement("tr");
    let claseColor4 = '';
    if (equipo4Data.index4 <= 4) {
        claseColor4 = 'pos-nada';
    } else if (equipo4Data.index4 <= 5) {
        claseColor4 = 'pos-playoff';
    }else if (equipo4Data.index4 <= 20) {
        claseColor4 = 'pos-nada';
    }
    nuevaFila4.innerHTML = `
    <td class="fw-bold text-center ${claseColor4}">${equipo4Data.index4}</td>
    <td class="fw-bold text-center">${equipo4Data.equipo4}</td>
    <td class="euro-jug fw-bold text-center">${equipo4Data.partidosJugados4}</td>
    <td class="euro-act fw-bold text-center">${equipo4Data.puntosActuales4}</td>
    <td class="euro-proxi fw-bold text-center">${equipo4Data.proximidadDeEuropa}%</td>
    <td class="euro-mate fw-bold text-center">${equipo4Data.partidosGanadosMatematicos4}</td>
    <td class="euro-opti fw-bold text-center">${equipo4Data.partidosGanadosOptimistas4}</td>
    <td class="euro-pesi fw-bold text-center">${equipo4Data.partidosGanadosPesimistas4}</td>
    `;
    tabla4.appendChild(nuevaFila4);
});*/

// Septima función para calcular el porcentaje a la Conference League
/*const filas5 = document.querySelectorAll("#tablaConfeVallad tbody tr");
const partidosTotales5 = 38; // Cambiado a 38 partidos en la temporada
const puntosPorGanar5 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija5 = 60; // Ajusta este valor según tus necesidades
const equipos5 = [];
let index5 = 1;
filas5.forEach((fila) => {
    const equipo5 = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados5 = parseInt(fila.querySelector(`.confe-jug`).textContent);
    const puntosActuales5 = parseInt(fila.querySelector(`.confe-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaConfe = Math.round((proximidadFija5 / 100) * partidosTotales5 * puntosPorGanar5);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan5 = Math.max(0, puntosParaConfe - puntosActuales5);
    const proximidadDeConfe = Math.min(((puntosParaConfe - puntosQueFaltan5) / puntosParaConfe) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesConfe = partidosTotales5 - partidosJugados5;
    const partidosGanadosMatematicos5 = Math.min(puntosActuales5 + partidosRestantesConfe * puntosPorGanar5, puntosParaConfe);
    const partidosGanadosPesimistas5 = Math.min(partidosGanadosMatematicos5 - 2, puntosParaConfe);
    const partidosGanadosOptimistas5 = Math.min(partidosGanadosMatematicos5 -4, puntosParaConfe);
    equipos5.push({
        index5: index5,
        equipo5,
        partidosJugados5,
        puntosActuales5,
        proximidadDeConfe:Math.round(proximidadDeConfe),
        partidosGanadosMatematicos5,
        partidosGanadosOptimistas5,
        partidosGanadosPesimistas5
    });
    index5++
});
// Ordenar los equipos3 por proximidad descendente
equipos5.sort((a, b) => b.proximidadDeConfe - a.proximidadDeConfe);
// Actualizar la tabla3 con los datos ordenados
const tabla5 = document.querySelector("#tablaConfeVallad tbody");
tabla5.innerHTML = ""; // Limpiar la tabla5 antes de actualizar
equipos5.forEach((equipo5Data) => {
    const nuevaFila5 = document.createElement("tr");
    let claseColor5 = '';
    if (equipo5Data.index5 <= 5) {
        claseColor5 = 'pos-nada';
    } else if (equipo5Data.index5 <= 6) {
        claseColor5 = 'pos-confe';
    }else if (equipo5Data.index5 <= 20) {
        claseColor5 = 'pos-nada';
    }
    nuevaFila5.innerHTML = `
    <td class="fw-bold text-center ${claseColor5}">${equipo5Data.index5}</td>
    <td class="fw-bold text-center">${equipo5Data.equipo5}</td>
    <td class="confe-jug fw-bold text-center">${equipo5Data.partidosJugados5}</td>
    <td class="confe-act fw-bold text-center">${equipo5Data.puntosActuales5}</td>
    <td class="confe-proxi fw-bold text-center">${equipo5Data.proximidadDeConfe}%</td>
    <td class="confe-mate fw-bold text-center">${equipo5Data.partidosGanadosMatematicos5}</td>
    <td class="confe-opti fw-bold text-center">${equipo5Data.partidosGanadosOptimistas5}</td>
    <td class="confe-pesi fw-bold text-center">${equipo5Data.partidosGanadosPesimistas5}</td>
    `;
    tabla5.appendChild(nuevaFila5);
});*/

// Octava función para calcular el descenso en la Liga BBVA
const filas6 = document.querySelectorAll("#tablaDescVallad2 tbody tr");
const partidosTotales6 = 42; // Cambiado a 42 partidos en la temporada
const puntosPorGanar6 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFijar6 = 40; // Ajusta este valor según tus necesidades
const equipos6 = [];
let index6 = 1;
filas6.forEach((fila) => {
    const equipo6 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados6 = parseInt(fila.querySelector(`.desce-jug`).textContent);
    const puntosActuales6 = parseInt(fila.querySelector(`.desce-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosPermanencia6 = Math.round((proximidadFijar6 / 100) * partidosTotales6 * puntosPorGanar6);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan6 = Math.max(0, puntosPermanencia6 - puntosActuales6);
    const proxiPermanencia6 = Math.min(((puntosPermanencia6 - puntosQueFaltan6) / puntosPermanencia6) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesPermanencia6 = partidosTotales6 - partidosJugados6;
    const partidosGanadosMatematicos6 = Math.min(puntosActuales6 + partidosRestantesPermanencia6 * puntosPorGanar6, puntosPermanencia6);
    const partidosGanadosPesimistas6 = Math.min(partidosGanadosMatematicos6 + 2, puntosPermanencia6);
    const partidosGanadosOptimistas6 = Math.min(partidosGanadosMatematicos6 - 2, puntosPermanencia6);
    equipos6.push({
        index6: index6,
        equipo6,
        partidosJugados6,
        puntosActuales6,
        proxiPermanencia6:Math.round(proxiPermanencia6),
        partidosGanadosMatematicos6,
        partidosGanadosOptimistas6,
        partidosGanadosPesimistas6
    });
    index6++
});
// Ordenar los equipos6 por proximidad desceendente
equipos6.sort((a, b) => b.proxiPermanencia6 - a.proxiPermanencia6);
// Actualizar la tabla6 con los datos ordenados
const tabla6 = document.querySelector("#tablaDescVallad2 tbody");
tabla6.innerHTML = ""; // Limpiar la tabla2 antes de actualizar
equipos6.forEach((equipo6Data) => {
    const nuevaFila6 = document.createElement("tr");
    let claseColor6 = '';
    if (equipo6Data.index6 <= 18) {
        claseColor6 = 'pos-nada';
    } else if (equipo6Data.index6 <= 22) {
        claseColor6 = 'pos-desc';
    }
    nuevaFila6.innerHTML = `
    <td class="fw-bold text-center ${claseColor6}">${equipo6Data.index6}</td>
    <td class="fw-bold text-center size_equipos2 text-white">${equipo6Data.equipo6}</td>
    <td class="desce-jug fw-bold text-center">${equipo6Data.partidosJugados6}</td>
    <td class="desce-act fw-bold text-center">${equipo6Data.puntosActuales6}</td>
    <td class="desce-prox fw-bold text-center">${equipo6Data.proxiPermanencia6}%</td>
    <td class="desce-mate fw-bold text-center">${equipo6Data.partidosGanadosMatematicos6}</td>
    <td class="desce-opti fw-bold text-center">${equipo6Data.partidosGanadosOptimistas6}</td>
    <td class="desce-pesi fw-bold text-center">${equipo6Data.partidosGanadosPesimistas6}</td>
    `;
    tabla6.appendChild(nuevaFila6);
});

// Novena función para calcular el porcentaje al Campeón y Ascenso
const filas7 = document.querySelectorAll("#tablaCampeonVallad tbody tr");
const partidosTotales7 = 42; // Cambiado a 38 partidos en la temporada
const puntosPorGanar7 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija7 = 90; // Ajusta este valor según tus necesidades
const equipos7 = [];
let index7 = 1;
filas7.forEach((fila) => {
    const equipo7 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados7 = parseInt(fila.querySelector(`.camp-jug`).textContent);
    const puntosActuales7 = parseInt(fila.querySelector(`.camp-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaChampions = Math.round((proximidadFija7 / 100) * partidosTotales7 * puntosPorGanar7);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan7 = Math.max(0, puntosParaChampions - puntosActuales7);
    const proximidadDeChampions = Math.min(((puntosParaChampions - puntosQueFaltan7) / puntosParaChampions) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesChampions = partidosTotales7 - partidosJugados7;
    const partidosGanadosMatematicos7 = Math.min(puntosActuales7 + partidosRestantesChampions * puntosPorGanar7, puntosParaChampions);
    const partidosGanadosPesimistas7 = Math.min(partidosGanadosMatematicos7 - 19, puntosParaChampions);
    const partidosGanadosOptimistas7 = Math.min(partidosGanadosMatematicos7 -21, puntosParaChampions);
    equipos7.push({
        index7: index7,
        equipo7,
        partidosJugados7,
        puntosActuales7,
        proximidadDeChampions:Math.round(proximidadDeChampions),
        partidosGanadosMatematicos7,
        partidosGanadosOptimistas7,
        partidosGanadosPesimistas7
    });
    index7++
});
// Ordenar los equipo7s7 por proximidad descendente
equipos7.sort((a, b) => b.proximidadDeChampions - a.proximidadDeChampions);
// Actualizar la tabla7 con los datos ordenados
const tabla7 = document.querySelector("#tablaCampeonVallad tbody");
tabla7.innerHTML = ""; // Limpiar la tabla7 antes de actualizar
equipos7.forEach((equipo7Data) => {
    const nuevaFila7 = document.createElement("tr");
    let claseColor7 = '';
    if (equipo7Data.index7 <= 2) {
        claseColor7 = 'pos-ascen';   
    } else if (equipo7Data.index7 <=22) {
        claseColor7 = 'pos-nada';
    }
    nuevaFila7.innerHTML = `
    <td class="fw-bold text-center ${claseColor7}">${equipo7Data.index7}</td>
    <td class="fw-bold text-center size_equipos2 text-white">${equipo7Data.equipo7}</td>
    <td class="camp-jug fw-bold text-center">${equipo7Data.partidosJugados7}</td>
    <td class="camp-act fw-bold text-center">${equipo7Data.puntosActuales7}</td>
    <td class="camp-proxi fw-bold text-center">${equipo7Data.proximidadDeChampions}%</td>
    <td class="camp-mate fw-bold text-center">${equipo7Data.partidosGanadosMatematicos7}</td>
    <td class="camp-opti fw-bold text-center">${equipo7Data.partidosGanadosOptimistas7}</td>
    <td class="camp-pesi fw-bold text-center">${equipo7Data.partidosGanadosPesimistas7}</td>
    `;
    tabla7.appendChild(nuevaFila7);
});