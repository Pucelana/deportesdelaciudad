// Primera función para calcular la clasificación y oredenar automáticamente
/*function calcularEstadisticas() {
    const tablaDatos = document.getElementById('tablaClasifVcv');
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
const filas = document.querySelectorAll("#tablaAscensoVcv tbody tr");
const partidosTotales = 22; // Cambiado a 42 partidos en la temporada
const puntosPorGanar = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija =60; // Ajusta este valor según tus necesidades
const equipos = [];
let index = 1;
filas.forEach((fila) => {
    const equipo = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.jugados1`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.pts-act1`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso = proximidadFija;
    // Calcular la proximidad de ascenso
    const puntosQueFaltan = Math.max(0, puntosParaAscenso - puntosActuales);
    const proximidadDeAscenso = Math.min(((puntosParaAscenso - puntosQueFaltan) / puntosParaAscenso) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso = partidosTotales - partidosJugados;
    const partidosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesAscenso * puntosPorGanar, puntosParaAscenso);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos - 1, puntosParaAscenso);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -2, puntosParaAscenso);
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
const tabla = document.querySelector("#tablaAscensoVcv tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor = '';
    if (equipoData.index <= 2) {
        claseColor = 'pos-ascen';
    } else if (equipoData.index <=12) {
        claseColor = 'pos-nada';
    }
    nuevaFila.innerHTML = `
    <td class="equipo-mobile text-center ${claseColor}">${equipoData.index}</td>
    <td class="equipo-mobile text-start size_equipos2 ${
    equipoData.equipo.includes("Universidad VCV") ? "equipo-pucela" : ""}">${equipoData.equipo}</td>
    <td class="jugados1 equipo-mobile text-center">${equipoData.partidosJugados}</td>
    <td class="pts-act1 equipo-mobile text-center">${equipoData.puntosActuales}</td>
    <td class="proxi1 equipo-mobile text-center">${equipoData.proximidadDeAscenso}%</td>
    <td class="pts-mate1 equipo-mobile text-center d-none d-md-table-cell">${equipoData.partidosGanadosMatematicos}</td>
    <td class="pts-opti1 equipo-mobile text-center d-none d-md-table-cell">${equipoData.partidosGanadosOptimistas}</td>
    <td class="pts-pesi1 equipo-mobile text-center d-none d-md-table-cell">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});

// Tercera función para calcular el porcentaje a los PlayOff
const filas1 = document.querySelectorAll("#tablaPlayVcv tbody tr");
const partidosTotales1 = 22; // Cambiado a 42 partidos en la temporada
const puntosPorGanar1 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFija1 = 55; // Ajusta este valor según tus necesidades
const equipos1 = [];
let index1 = 1;
filas1.forEach((fila) => {
    const equipo1 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados1 = parseInt(fila.querySelector(`.play-jug`).textContent);
    const puntosActuales1 = parseInt(fila.querySelector(`.play-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosParaAscenso1 = proximidadFija1;
    // Calcular la proximidad de ascenso
    const puntosQueFaltan1 = Math.max(0, puntosParaAscenso1 - puntosActuales1);
    const proximidadDePlayOff = Math.min(((puntosParaAscenso1 - puntosQueFaltan1) / puntosParaAscenso1) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesAscenso1 = partidosTotales1 - partidosJugados1;
    const partidosGanadosMatematicos1 = Math.min(puntosActuales1 + partidosRestantesAscenso1 * puntosPorGanar1, puntosParaAscenso1);
    const partidosGanadosPesimistas1 = Math.min(partidosGanadosMatematicos1 -2, puntosParaAscenso1);
    const partidosGanadosOptimistas1 = Math.min(partidosGanadosMatematicos1 -3, puntosParaAscenso1);
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
const tabla1 = document.querySelector("#tablaPlayVcv tbody");
tabla1.innerHTML = ""; // Limpiar la tabla1 antes de actualizar
equipos1.forEach((equipo1Data) => {
    const nuevaFila1 = document.createElement("tr");
    let claseColor1 = '';
    if (equipo1Data.index1 <= 1) {
        claseColor1 = 'pos-ascen';
    } else if (equipo1Data.index1 <=12) {
        claseColor1 = 'pos-nada';
    }
    nuevaFila1.innerHTML = `
    <td class="equipo-mobile text-center ${claseColor1}">${equipo1Data.index1}</td>
    <td class="equipo-mobile text-start size_equipos2 ${
    equipo1Data.equipo1.includes("Universidad VCV") ? "equipo-pucela" : ""}">${equipo1Data.equipo1}</td>
    <td class="play-jug equipo-mobile text-center">${equipo1Data.partidosJugados1}</td>
    <td class="play-act equipo-mobile text-center">${equipo1Data.puntosActuales1}</td>
    <td class="play-prox equipo-mobile text-center">${equipo1Data.proximidadDePlayOff}%</td>
    <td class="play-mate equipo-mobile text-center d-none d-md-table-cell">${equipo1Data.partidosGanadosMatematicos1}</td>
    <td class="play-opti equipo-mobile text-center d-none d-md-table-cell">${equipo1Data.partidosGanadosOptimistas1}</td>
    <td class="play-pesi equipo-mobile text-center d-none d-md-table-cell">${equipo1Data.partidosGanadosPesimistas1}</td>
    `;
    tabla1.appendChild(nuevaFila1);
});

// Cuarta función para calcular la permanencia
const filas2 = document.querySelectorAll("#tablaDescVcv tbody tr");
const partidosTotales2 = 22; // Cambiado a 42 partidos en la temporada
const puntosPorGanar2 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFijar2 = 20; // Ajusta este valor según tus necesidades
const equipos2 = [];
let index2 = 1;
filas2.forEach((fila) => {
    const equipo2 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados2 = parseInt(fila.querySelector(`.desc-jug`).textContent);
    const puntosActuales2 = parseInt(fila.querySelector(`.desc-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosPermanencia2 = proximidadFijar2;
    // Calcular la proximidad de ascenso
    const puntosQueFaltan2 = Math.max(0, puntosPermanencia2 - puntosActuales2);
    const proxiPermanencia = Math.min(((puntosPermanencia2 - puntosQueFaltan2) / puntosPermanencia2) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesPermanencia = partidosTotales2 - partidosJugados2;
    const partidosGanadosMatematicos2 = Math.min(puntosActuales2 + partidosRestantesPermanencia * puntosPorGanar2, puntosPermanencia2);
    const partidosGanadosPesimistas2 = Math.min(partidosGanadosMatematicos2 -1, puntosPermanencia2);
    const partidosGanadosOptimistas2 = Math.min(partidosGanadosMatematicos2 -2, puntosPermanencia2);
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
const tabla2 = document.querySelector("#tablaDescVcv tbody");
tabla2.innerHTML = ""; // Limpiar la tabla2 antes de actualizar
equipos2.forEach((equipo2Data) => {
    const nuevaFila2 = document.createElement("tr");
    let claseColor2 = '';
    if (equipo2Data.index2 <= 10) {
        claseColor2 = 'pos-nada';
    } else if (equipo2Data.index2 <=12) {
        claseColor2 = 'pos-desc';
    }
    nuevaFila2.innerHTML = `
    <td class="equipo-mobile text-center ${claseColor2}">${equipo2Data.index2}</td>
    <td class="equipo-mobile text-start size_equipos2 ${
    equipo2Data.equipo2.includes("Universidad VCV") ? "equipo-pucela" : ""}">${equipo2Data.equipo2}</td>
    <td class="desc-jug equipo-mobile text-center">${equipo2Data.partidosJugados2}</td>
    <td class="desc-act equipo-mobile text-center">${equipo2Data.puntosActuales2}</td>
    <td class="desc-prox equipo-mobile text-center">${equipo2Data.proxiPermanencia}%</td>
    <td class="desc-mate equipo-mobile text-center d-none d-md-table-cell">${equipo2Data.partidosGanadosMatematicos2}</td>
    <td class="desc-opti equipo-mobile text-center d-none d-md-table-cell">${equipo2Data.partidosGanadosOptimistas2}</td>
    <td class="desc-pesi equipo-mobile text-center d-none d-md-table-cell">${equipo2Data.partidosGanadosPesimistas2}</td>
    `;
    tabla2.appendChild(nuevaFila2);
});
// Quinta función para calcular la promoción descenso
const filas5 = document.querySelectorAll("#tablaPromoVcv tbody tr");
const partidosTotales5 = 22; // Cambiado a 42 partidos en la temporada
const puntosPorGanar5 = 3; // Cambiado a 3 puntos por partido ganado
const proximidadFijar5 = 22; // Ajusta este valor según tus necesidades
const equipos5 = [];
let index5 = 1;
filas5.forEach((fila) => {
    const equipo5 = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados5 = parseInt(fila.querySelector(`.desc-jug`).textContent);
    const puntosActuales5 = parseInt(fila.querySelector(`.desc-act`).textContent);
    // Calcular puntos necesarios para alcanzar la proximidad fija
    const puntosPermanencia5 = Math.round((proximidadFijar5 / 100) * partidosTotales5 * puntosPorGanar5);
    // Calcular la proximidad de ascenso
    const puntosQueFaltan5 = Math.max(0, puntosPermanencia5 - puntosActuales5);
    const proxiPermanencia5 = Math.min(((puntosPermanencia5 - puntosQueFaltan5) / puntosPermanencia5) * 100, 100);
    // Calcular los partidos ganados matemáticos, optimistas y pesimistas
    const partidosRestantesPermanencia5 = partidosTotales5 - partidosJugados5;
    const partidosGanadosMatematicos5 = Math.min(puntosActuales5 + partidosRestantesPermanencia5 * puntosPorGanar5, puntosPermanencia5);
    const partidosGanadosPesimistas5 = Math.min(partidosGanadosMatematicos5 -1, puntosPermanencia5);
    const partidosGanadosOptimistas5 = Math.min(partidosGanadosMatematicos5 -2, puntosPermanencia5);
    equipos5.push({
        index5: index5,
        equipo5,
        partidosJugados5,
        puntosActuales5,
        proxiPermanencia5:Math.round(proxiPermanencia5),
        partidosGanadosMatematicos5,
        partidosGanadosOptimistas5,
        partidosGanadosPesimistas5
    });
    index5++
});
// Ordenar los equipos2 por proximidad descendente
equipos5.sort((a, b) => b.proxiPermanencia - a.proxiPermanencia);
// Actualizar la tabla2 con los datos ordenados
const tabla5 = document.querySelector("#tablaPromoVcv tbody");
tabla5.innerHTML = ""; // Limpiar la tabla5 antes de actualizar
equipos5.forEach((equipo5Data) => {
    const nuevaFila5 = document.createElement("tr");
    let claseColor5 = '';
    if (equipo5Data.index5 <= 9) {
        claseColor5 = 'pos-nada';
    } else if (equipo5Data.index5 <=10) {
        claseColor5 = 'pos-promo';
    } else if (equipo5Data.index5 <=12) {
        claseColor5 = 'pos-nada';
    }
    nuevaFila5.innerHTML = `
    <td class="equipo-mobile text-center ${claseColor5}">${equipo5Data.index5}</td>
    <td class="equipo-mobile text-start size_equipos2 ${
    equipo5Data.equipo5.includes("Universidad VCV") ? "equipo-pucela" : ""}">${equipo5Data.equipo5}</td>
    <td class="desc-jug equipo-mobile text-center">${equipo5Data.partidosJugados5}</td>
    <td class="desc-act equipo-mobile text-center">${equipo5Data.puntosActuales5}</td>
    <td class="desc-prox equipo-mobile text-center">${equipo5Data.proxiPermanencia5}%</td>
    <td class="desc-mate equipo-mobile text-center d-none d-md-table-cell">${equipo5Data.partidosGanadosMatematicos5}</td>
    <td class="desc-opti equipo-mobile text-center d-none d-md-table-cell">${equipo5Data.partidosGanadosOptimistas5}</td>
    <td class="desc-pesi equipo-mobile text-center d-none d-md-table-cell">${equipo5Data.partidosGanadosPesimistas5}</td>
    `;
    tabla5.appendChild(nuevaFila5);
});