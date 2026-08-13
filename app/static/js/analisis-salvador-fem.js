// Segunda función playoff y ordenar automaticamente
const filas1 = document.querySelectorAll("#tablaPlaySalvFem tbody tr");
const partidosTotales1 = 14; // Total de partidos en la temporada
const partidosPorGanar1 = 4; // Cantidad de puntos por partido ganado
const partidosPlayOff = 50; // Número de partidos para llegar a los playoffs
const equiposPlay = [];
let index1 = 1;
filas1.forEach((fila) => {
    const equipo = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.play-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.play-act`).textContent);

    //const partidosRestantes = partidosTotales1 - partidosJugados;
    const puntosParaPlayoffs = partidosPlayOff;

    const puntosFaltantes = Math.max(0, puntosParaPlayoffs - puntosActuales);
    const proximidadAscenso = Math.min(((puntosParaPlayoffs - puntosFaltantes) / puntosParaPlayoffs) * 100, 100);

    const partidosRestantesParaPlayoffs = partidosPlayOff;
    const puntosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesParaPlayoffs * partidosPorGanar1, puntosParaPlayoffs);
    const puntosGanadosPesimistas = Math.min(puntosGanadosMatematicos - 2, puntosParaPlayoffs);
    const puntosGanadosOptimistas = Math.min(puntosGanadosMatematicos - 3, puntosParaPlayoffs);

    equiposPlay.push({
        index1: index1,
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadAscenso:Math.round(proximidadAscenso),
        puntosGanadosMatematicos,
        puntosGanadosOptimistas,
        puntosGanadosPesimistas
    });
    index1++
});
// Ordenar los equiposPlay por proximidad descendente
equiposPlay.sort((a, b) => b.proximidadAscenso - a.proximidadAscenso);
// Actualizar la tabla con los datos ordenados
const tabla1 = document.querySelector("#tablaPlaySalvFem tbody");
tabla1.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposPlay.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor1 = '';
    if (equipoData.index1 <= 4) {
        claseColor1 = 'pos-ascen';
    } else if (equipoData.index1 <=8) {
        claseColor1 = 'pos-nada';
    }
    nuevaFila.innerHTML = `
    <td class="text-center equipo-mobile ${claseColor1}">${equipoData.index1}</td>
    <td class="equipo-mobile text-start size_equipos2 ${
    equipoData.equipo.includes("El Salvador Fem") ? "equipo-pucela" : ""}">${equipoData.equipo}</td>
    <td class="play-jug text-center equipo-mobile">${equipoData.partidosJugados}</td>
    <td class="play-act text-center equipo-mobile">${equipoData.puntosActuales}</td>
    <td class="play-prox text-center equipo-mobile">${equipoData.proximidadAscenso}%</td>
    <td class="play-mate text-center equipo-mobile">${equipoData.puntosGanadosMatematicos}</td>
    <td class="play-opti text-center equipo-mobile d-none d-md-table-cell">${equipoData.puntosGanadosOptimistas}</td>
    <td class="play-pesi text-center equipo-mobile d-none d-md-table-cell">${equipoData.puntosGanadosPesimistas}</td>
    `;
    tabla1.appendChild(nuevaFila);
});

// Tercera función descenso y ordenar automaticamente
const filas2 = document.querySelectorAll("#tablaDescSalvFem tbody tr");
const partidosTotales2 = 14; // Total de partidos en la temporada
const partidosPorGanar2 = 4; // Cantidad de puntos por partido ganado
const partidosDescenso = 22;
const equiposDesc = [];
let index2 = 1;
filas2.forEach((fila) => {
    const equipo = fila.querySelector(`.size_equipos2`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.desc-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.desc-act`).textContent);
    const puntosParaSalvar = partidosDescenso;
    const puntosFaltan = Math.max((0, puntosParaSalvar - puntosActuales));
    const proxiSalvacion = Math.min(((puntosParaSalvar - puntosFaltan) / puntosParaSalvar) * 100, 100);
    const partidosRestantesSalvacion = partidosDescenso;
    const partidosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesSalvacion * partidosPorGanar2,puntosParaSalvar);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos -2, puntosParaSalvar);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -3, puntosParaSalvar);
    equiposDesc.push({
        index2: index2,
        equipo,
        partidosJugados,
        puntosActuales,
        proxiSalvacion:Math.round(proxiSalvacion),
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
    index2++
});
// Ordenar los equiposDesc por proximidad descendente
equiposDesc.sort((a, b) => b.proxiSalvacion - a.proxiSalvacion);
// Actualizar la tabla con los datos ordenados
const tabla2 = document.querySelector("#tablaDescSalvFem tbody");
tabla2.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposDesc.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor2 = '';
    if (equipoData.index2 <= 6) {
        claseColor2 = 'pos-nada';
    }    else if (equipoData.index2 <=7) {
        claseColor2 = 'pos-promo';
    } else if (equipoData.index2 <=8) {
        claseColor2 = 'pos-desc';
    }
    nuevaFila.innerHTML = `
    <td class="text-center equipo-mobile ${claseColor2}">${equipoData.index2}</td>
    <td class="equipo-mobile text-start size_equipos2 ${
    equipoData.equipo.includes("El Salvador Fem.") ? "equipo-pucela" : ""}">${equipoData.equipo}</td>
    <td class="desc-jug text-center equipo-mobile">${equipoData.partidosJugados}</td>
    <td class="desc-act text-center equipo-mobile">${equipoData.puntosActuales}</td>
    <td class="desc-prox text-center equipo-mobile">${equipoData.proxiSalvacion}%</td>
    <td class="desc-mate text-center equipo-mobile">${equipoData.partidosGanadosMatematicos}</td>
    <td class="desc-opti text-center equipo-mobile d-none d-md-table-cell">${equipoData.partidosGanadosOptimistas}</td>
    <td class="desc-pesi text-center equipo-mobile d-none d-md-table-cell">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla2.appendChild(nuevaFila);
});