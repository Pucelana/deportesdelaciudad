document.addEventListener("DOMContentLoaded", () => {

  const filas = document.querySelectorAll(".tabla_aula tbody tr");

  if (!filas.length) return;

  filas.forEach(fila => {
     // Obtener el nombre del equipo de la fila actual
          var equipo = fila.querySelector("th").textContent.trim();
          console.log(equipo);
          // Obtener la jornada y determinar si el Promesas juega en casa o como visitante
          var jornadaElement = fila.querySelector(".jorn_ida");
          var esLocal = false; // Por defecto, asumimos que el Promesas juega como visitante
          if (jornadaElement) {
            var jornada = jornadaElement.textContent.trim();
            if (jornada.includes("C")) {
              esLocal = true;
            }
          }
          // Obtener los valores de los resultados de la fila
          var resultadoA = parseInt(
            fila.querySelector(".resultadoA").textContent
          );
          console.log(resultadoA);
          var resultadoB = parseInt(
            fila.querySelector(".resultadoB").textContent
          );
          console.log(resultadoB);
          var resultadoAA = parseInt(
            fila.querySelector(".resultadoAA").textContent
          );
          console.log(resultadoAA);
          var resultadoBB = parseInt(
            fila.querySelector(".resultadoBB").textContent
          );
          console.log(resultadoBB);
          // Comparar los resultados y actualizar el estilo de las celdas correspondientes
          var part1 = fila.querySelector(".part1");
          var average = fila.querySelector(".average");
          if (esLocal) {
            if (resultadoA > resultadoB) {
              part1.textContent = "2";
              part1.style.color = "blue";
            } else if (resultadoA === resultadoB) {
              part1.textContent = "1";
              part1.style.color = "blue";
            } else if (resultadoA < resultadoB) {
              part1.textContent = "0";
              part1.style.color = "blue";
            } else if (resultadoAA > resultadoBB) {
              part1.textContent = "2";
              part1.style.color = "blue";
            } else if (resultadoAA === resultadoBB) {
              part1.textContent = "1";
              part1.style.color = "blue";
            } else if (resultadoAA < resultadoBB) {
              part1.textContent = "0";
              part1.style.color = "blue";
            }
          } else {
            if (resultadoB > resultadoA) {
              part1.textContent = "2";
              part1.style.color = "blue";
            } else if (resultadoB === resultadoA) {
              part1.textContent = "1";
              part1.style.color = "blue";
            } else if (resultadoB < resultadoA) {
              part1.textContent = "0";
              part1.style.color = "blue";
            } else if (resultadoBB > resultadoAA) {
              part1.textContent = "2";
              part1.style.color = "blue";
            } else if (resultadoBB === resultadoAA) {
              part1.textContent = "1";
              part1.style.color = "blue";
            } else if (resultadoBB < resultadoAA) {
              part1.textContent = "0";
              part1.style.color = "blue";
            }
          }
          // Verificar si se tienen los resultados del segundo enfrentamiento
          if (!isNaN(resultadoAA) && !isNaN(resultadoBB)) {
            // Calcular el puntaje del segundo enfrentamiento
            var puntajeSegundoEnfrentamiento = 0;
            // Determinar si el equipo juega como local o visitante en el segundo enfrentamiento
            if (resultadoAA > resultadoBB) {
              // "AA" gana como local
              if (!esLocal) {
                puntajeSegundoEnfrentamiento = 2;
              }
            } else if (resultadoAA < resultadoBB) {
              // "AA" gana como visitante
              if (esLocal) {
                puntajeSegundoEnfrentamiento = 2;
              }
            } else {
              // Empate en el segundo enfrentamiento
              puntajeSegundoEnfrentamiento = 1;
            }
            // Actualizar el puntaje total sumando el del segundo enfrentamiento
            if (part1.textContent === "-") {
              part1.textContent = puntajeSegundoEnfrentamiento.toString();
            } else {
              part1.textContent = (
                parseInt(part1.textContent) + puntajeSegundoEnfrentamiento
              ).toString();
            }
          }
        });
        // Iterar sobre cada fila
        filas.forEach(function (fila) {
          // Obtener los valores de resultadoA y resultadoB de la fila actual
          var resultadoA = parseInt(
            fila.querySelector(".resultadoA").textContent
          );
          var resultadoB = parseInt(
            fila.querySelector(".resultadoB").textContent
          );
          // Obtener los valores de resultadoAA y resultadoBB de la fila actual para la jornada de vuelta
          var resultadoAA = parseInt(
            fila.querySelector(".resultadoAA").textContent
          );
          var resultadoBB = parseInt(
            fila.querySelector(".resultadoBB").textContent
          );
          // Obtener la celda 'average'
          var average = fila.querySelector(".average");
          // Calcular la diferencia de goles dependiendo si resultadoA juega como local o visitante
          var diferenciaGolesIda;
          if (fila.querySelector(".jorn_ida").textContent.includes("C")) {
            // resultadoA juega en casa
            diferenciaGolesIda = resultadoA - resultadoB;
          } else {
            // resultadoA juega como visitante
            diferenciaGolesIda = resultadoB - resultadoA;
          }
          // Calcular la diferencia de goles para la jornada de vuelta
          var diferenciaGolesVuelta;
          if (!isNaN(resultadoAA) && !isNaN(resultadoBB)) {
            if (fila.querySelector(".jorn_ida").textContent.includes("C")) {
              // resultadoAA juega como visitante en la jornada de vuelta
              diferenciaGolesVuelta = resultadoBB - resultadoAA;
            } else {
              // resultadoAA juega en casa en la jornada de vuelta
              diferenciaGolesVuelta = resultadoAA - resultadoBB;
            }
          } else {
            diferenciaGolesVuelta = 0;
          }
          var averageTotal = diferenciaGolesIda + diferenciaGolesVuelta;
          if (!isNaN(averageTotal)) {
            // Asignar el valor del average total a la celda 'average'
            average.textContent = averageTotal;
            // Determinar el color de la celda 'average' según la diferencia de goles
            if (averageTotal > 0) {
              average.style.color = "green"; // Equipo A ganó
            } else if (averageTotal < 0) {
              average.style.color = "red"; // Equipo A perdió
            } else {
              average.style.color = "black"; // Empate
            }
          } else {
            // Si averageTotal es NaN, dejar la celda vacía
            average.textContent = "";
          }
  });

});