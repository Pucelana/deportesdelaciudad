// Primera función para calcular la clasificación y oredenar automaticamente
/*function calcularEstadisticas() {
    const tablaDatos = document.getElementById('tablaClasificacion');
    const filasDatos = Array.from(tablaDatos.querySelectorAll('tbody tr'));
    filasDatos.forEach(row => {
        const ptosFav = parseInt(row.querySelector('.favor').textContent);
        const ptosCont = parseInt(row.querySelector('.contra').textContent);
        const ganados = parseInt(row.querySelector('.ganados').textContent);
        const perdidos = parseInt(row.querySelector('.perdidos').textContent);
        const partidosJugados = ganados + perdidos;
        row.querySelector('.jugados').textContent = partidosJugados;
        const diferenciaPuntos = ptosFav - ptosCont;
        row.querySelector('.dife').textContent = diferenciaPuntos;
        const puntos = ganados * 2 + perdidos;
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
/*const filas = document.querySelectorAll("#tablaAscensoAliados tbody tr");
const partidosTotales = 34; // Total de partidos en la temporada
const partidosPorGanar = 1; // Cantidad de puntos por partido ganado
const puntosAscenso = 31; // Puntos relativos para quedar primero
const equipos = [];
filas.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.fw-bold`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.jugados1`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.pts-act1`).textContent);

    const puntosParaAscenso = puntosAscenso * partidosPorGanar;
    
    const puntosQueFaltan = Math.max(0, puntosParaAscenso - puntosActuales);
    const proxiDeAscenso = Math.min(((puntosParaAscenso - puntosQueFaltan) / puntosParaAscenso) * 100, 100);

    const partidosRestantesAscenso = puntosAscenso;
    const partidosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesAscenso * partidosPorGanar,puntosParaAscenso);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos -2, puntosParaAscenso);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -3, puntosParaAscenso)

    equipos.push({
        equipo,
        partidosJugados,
        puntosActuales,
        proxiDeAscenso,
        partidosGanadosMatematicos,
        partidosGanadosOptimistas,
        partidosGanadosPesimistas
    });
});
// Ordenar los equipos por proximidad descendente
equipos.sort((a, b) => b.proxiDeAscenso - a.proxiDeAscenso);
// Actualizar la tabla con los datos ordenados
const tabla = document.querySelector("#tablaAscensoAliados tbody");
tabla.innerHTML = ""; // Limpiar la tabla antes de actualizar
equipos.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="jugados1 fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="pts-act1 fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="proxi1 fw-bold text-center">${equipoData.proxiDeAscenso.toFixed(2)}%</td>
    <td class="pts-mate1 fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="pts-opti1 fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="pts-pesi1 fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla.appendChild(nuevaFila);
});*/

// Tercera función playoff y ordenar automaticamente
const filas1 = document.querySelectorAll("#tablaPlayAliados tbody tr");
const partidosTotales1 = 22; // Total de partidos en la temporada
const partidosPorGanar1 = 1; // Cantidad de puntos por partido ganado
const partidosPlayOff = 15; // Número de partidos para llegar a los playoffs
const equiposPlay = [];
let index = 1;
filas1.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.play-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.play-act`).textContent);

    //const partidosRestantes = partidosTotales1 - partidosJugados;
    const puntosParaPlayoffs = partidosPlayOff * partidosPorGanar1;

    const puntosFaltantes = Math.max(0, puntosParaPlayoffs - puntosActuales);
    const proximidadAscenso = Math.min(((puntosParaPlayoffs - puntosFaltantes) / puntosParaPlayoffs) * 100, 100);

    const partidosRestantesParaPlayoffs = partidosPlayOff;
    const puntosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesParaPlayoffs * partidosPorGanar1, puntosParaPlayoffs);
    const puntosGanadosPesimistas = Math.min(puntosGanadosMatematicos - 2, puntosParaPlayoffs);
    const puntosGanadosOptimistas = Math.min(puntosGanadosMatematicos - 3, puntosParaPlayoffs);

    equiposPlay.push({
        index: index,
        equipo,
        partidosJugados,
        puntosActuales,
        proximidadAscenso: Math.round(proximidadAscenso),
        puntosGanadosMatematicos,
        puntosGanadosOptimistas,
        puntosGanadosPesimistas
    });
    index++
});
// Ordenar los equiposPlay por proximidad descendente
equiposPlay.sort((a, b) => b.proximidadAscenso - a.proximidadAscenso);
// Actualizar la tabla con los datos ordenados
const tabla1 = document.querySelector("#tablaPlayAliados tbody");
tabla1.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposPlay.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor = '';
    if (equipoData.index <= 4) {
        claseColor = 'pos-ascen';
    } else if (equipoData.index <=12) {
        claseColor = 'pos-nada';
    }
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center ${claseColor}">${equipoData.index}</td>
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="play-jug fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="play-act fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="play-prox fw-bold text-center">${equipoData.proximidadAscenso}%</td>
    <td class="play-mate fw-bold text-center">${equipoData.puntosGanadosMatematicos}</td>
    <td class="play-opti fw-bold text-center">${equipoData.puntosGanadosOptimistas}</td>
    <td class="play-pesi fw-bold text-center">${equipoData.puntosGanadosPesimistas}</td>
    `;
    tabla1.appendChild(nuevaFila);
});

// Cuarta función descenso y ordenar automaticamente
const filas2 = document.querySelectorAll("#tablaDescAliados tbody tr");
const partidosTotales2 = 22; // Total de partidos en la temporada
const partidosPorGanar2 = 1; // Cantidad de puntos por partido ganado
const partidosDescenso = 5;
const equiposDesc = [];
let index2 = 1;
filas2.forEach((fila, indice) => {
    const equipo = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.desc-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.desc-act`).textContent);

    const puntosParaSalvar = partidosDescenso * partidosPorGanar2;

    const puntosFaltan = Math.max((0, puntosParaSalvar - puntosActuales));
    const proxiSalvacion = Math.min(((puntosParaSalvar - puntosFaltan) / puntosParaSalvar) * 100, 100);

    const partidosRestantesSalvacion = partidosDescenso;
    const partidosGanadosMatematicos = Math.min(puntosActuales + partidosRestantesSalvacion * partidosPorGanar2,puntosParaSalvar);
    const partidosGanadosPesimistas = Math.min(partidosGanadosMatematicos -1, puntosParaSalvar);
    const partidosGanadosOptimistas = Math.min(partidosGanadosMatematicos -2, puntosParaSalvar);

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
const tabla2 = document.querySelector("#tablaDescAliados tbody");
tabla2.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposDesc.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor2 = '';
    if (equipoData.index2 <= 10) {
        claseColor2 = 'pos-nada';
    } else if (equipoData.index2 <=11) {
        claseColor2 = 'pos-promo';
    }  else if (equipoData.index2 <=12) {
        claseColor2 = 'pos-desc';
    }
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center ${claseColor2}">${equipoData.index2}</td>
    <td class="fw-bold text-center">${equipoData.equipo}</td>
    <td class="desc-jug fw-bold text-center">${equipoData.partidosJugados}</td>
    <td class="desc-act fw-bold text-center">${equipoData.puntosActuales}</td>
    <td class="desc-prox fw-bold text-center">${equipoData.proxiSalvacion}%</td>
    <td class="desc-mate fw-bold text-center">${equipoData.partidosGanadosMatematicos}</td>
    <td class="desc-opti fw-bold text-center">${equipoData.partidosGanadosOptimistas}</td>
    <td class="desc-pesi fw-bold text-center">${equipoData.partidosGanadosPesimistas}</td>
    `;
    tabla2.appendChild(nuevaFila);
});

// Quinta función Euro y ordenar automaticamente
const filas3 = document.querySelectorAll("#tablaEuroAliados tbody tr");
const partidosTotales3 = 22; // Total de partidos en la temporada
const partidosPorGanar3 = 1; // Cantidad de puntos por partido ganado
const partidosEuro = 22;
const equiposEuro = [];
let index3 = 1;
filas3.forEach((fila, indice) => {
    const equipo3 = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados3 = parseInt(fila.querySelector(`.euro-jug`).textContent);
    const puntosActuales3 = parseInt(fila.querySelector(`.euro-act`).textContent);
    const puntosParaEuro = partidosEuro * partidosPorGanar2;
    const puntosFaltan3 = Math.max((0, puntosParaEuro - puntosActuales3));
    const proxiEuro = Math.min(((puntosParaEuro - puntosFaltan3) / puntosParaEuro) * 100, 100);
    const partidosRestantesEuro = partidosEuro;
    const partidosGanadosMatematicos3 = Math.min(puntosActuales3 + partidosRestantesEuro * partidosPorGanar3,puntosParaEuro);
    const partidosGanadosPesimistas3 = Math.min(partidosGanadosMatematicos3 -2, puntosParaEuro);
    const partidosGanadosOptimistas3 = Math.min(partidosGanadosMatematicos3 -3, puntosParaEuro);
    equiposEuro.push({
        index3:index3,
        equipo3,
        partidosJugados3,
        puntosActuales3,
        proxiEuro:Math.round(proxiEuro),
        partidosGanadosMatematicos3,
        partidosGanadosOptimistas3,
        partidosGanadosPesimistas3
    });
    index3++
});
// Ordenar los equiposEuro por proximidad Euroendente
equiposEuro.sort((a, b) => b.proxiEuro - a.proxiEuro);
// Actualizar la tabla con los datos ordenados
const tabla3 = document.querySelector("#tablaEuroAliados tbody");
tabla3.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposEuro.forEach((equipo3Data) => {
    const nuevaFila3 = document.createElement("tr");
    let claseColor3 = '';
    if (equipo3Data.index3 <= 1) {
        claseColor3 = 'pos-ascen';
    } else if (equipo3Data.index3 <=12) {
        claseColor3 = 'pos-nada';
    }
    nuevaFila3.innerHTML = `
    <td class="fw-bold text-center ${claseColor3}">${equipo3Data.index3}</td>
    <td class="fw-bold text-center">${equipo3Data.equipo3}</td>
    <td class="euro-jug fw-bold text-center">${equipo3Data.partidosJugados3}</td>
    <td class="euro-act fw-bold text-center">${equipo3Data.puntosActuales3}</td>
    <td class="euro-prox fw-bold text-center">${equipo3Data.proxiEuro}%</td>
    <td class="euro-mate fw-bold text-center">${equipo3Data.partidosGanadosMatematicos3}</td>
    <td class="euro-opti fw-bold text-center">${equipo3Data.partidosGanadosOptimistas3}</td>
    <td class="euro-pesi fw-bold text-center">${equipo3Data.partidosGanadosPesimistas3}</td>
    `;
    tabla3.appendChild(nuevaFila3);
});
