// Primera función para calcular la clasificación y oredenar automaticamente
/*function calcularEstadisticas2() {
    const tablaDatos = document.getElementById('tablaClasificacion2');
    const filasDatos = Array.from(tablaDatos.querySelectorAll('tbody tr'));
    filasDatos.forEach(row => {
        const ptosFav = parseInt(row.querySelector('.favor2').textContent);
        const ptosCont = parseInt(row.querySelector('.contra2').textContent);
        const ganados = parseInt(row.querySelector('.ganados2').textContent);
        const perdidos = parseInt(row.querySelector('.perdidos2').textContent);
        const partidosJugados = ganados + perdidos;
        row.querySelector('.jugados2').textContent = partidosJugados;
        const diferenciaPuntos = ptosFav - ptosCont;
        row.querySelector('.dife2').textContent = diferenciaPuntos;
        const puntos = ganados * 2 + perdidos;
        row.querySelector('.puntos2').textContent = puntos;
    });
    // Ordenar filas de datos según los puntos (PTS) de mayor a menor
    filasDatos.sort((a, b) => {
        const puntosA = parseInt(a.querySelector('.puntos2').textContent);
        const puntosB = parseInt(b.querySelector('.puntos2').textContent);
        const difPuntosA = parseInt(a.querySelector('.dife2').textContent);
        const difPuntosB = parseInt(b.querySelector('.dife2').textContent);
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
    calcularEstadisticas2();
  });*/

// Segunda función playoff y ordenar automaticamente
const filas1 = document.querySelectorAll("#tablaPlayPonce tbody tr");
const partidosTotales1 = 26; // Total de partidos en la temporada
const partidosPorGanar1 = 1; // Cantidad de puntos por partido ganado
const partidosPlayOff = 25; // Número de partidos para llegar a los playoffs
const equiposPlay = [];
let index1 = 1;
filas1.forEach((fila) => {
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
const tabla1 = document.querySelector("#tablaPlayPonce tbody");
tabla1.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposPlay.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor1 = '';
    if (equipoData.index1 <= 4) {
        claseColor1 = 'pos-ascen';
    } else if (equipoData.index1 <=14) {
        claseColor1 = 'pos-nada';
    }
    nuevaFila.innerHTML = `
    <td class="fw-bold text-center ${claseColor1}">${equipoData.index1}</td>
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

// Tercera función descenso y ordenar automaticamente
const filas2 = document.querySelectorAll("#tablaDescPonce tbody tr");
const partidosTotales2 = 26; // Total de partidos en la temporada
const partidosPorGanar2 = 1; // Cantidad de puntos por partido ganado
const partidosDescenso = 11;
const equiposDesc = [];
let index2 = 1;
filas2.forEach((fila) => {
    const equipo = fila.querySelector(`.size_equipos`).textContent;
    const partidosJugados = parseInt(fila.querySelector(`.desc-jug`).textContent);
    const puntosActuales = parseInt(fila.querySelector(`.desc-act`).textContent);
    const puntosParaSalvar = partidosDescenso * partidosPorGanar2;
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
const tabla2 = document.querySelector("#tablaDescPonce tbody");
tabla2.innerHTML = ""; // Limpiar la tabla antes de actualizar
equiposDesc.forEach((equipoData) => {
    const nuevaFila = document.createElement("tr");
    let claseColor2 = '';
    if (equipoData.index2 <= 11) {
        claseColor2 = 'pos-nada';
    } else if (equipoData.index2 <=14) {
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
