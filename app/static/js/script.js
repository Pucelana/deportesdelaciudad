document.addEventListener("DOMContentLoaded", () => {

  const carouselInner = document.querySelector(
    '#carouselExampleControls .carousel-inner'
  );

  if (!carouselInner) return;

  // activar solo hasta tablets
  if (!window.matchMedia("(max-width: 1200px)").matches) return;

  // duplicar contenido
  carouselInner.innerHTML += carouselInner.innerHTML;

  // detectar tablet pequeña
  const smallTablet = window.innerWidth >= 600 && window.innerWidth <= 820;

  // velocidad especial
  let speed = smallTablet ? 1 : 0.35;

  let paused = false;

  // FORZAR overflow real
  carouselInner.style.minWidth = "max-content";

  function loop() {

    if (!paused) {

      carouselInner.scrollLeft += speed;

      // reinicio infinito
      if (
        carouselInner.scrollLeft >=
        (carouselInner.scrollWidth / 2)
      ) {

        carouselInner.scrollLeft = 0;
      }
    }

    requestAnimationFrame(loop);
  }

  // esperar renderizado real
  setTimeout(() => {

    if (
      carouselInner.scrollWidth >
      carouselInner.clientWidth
    ) {

      loop();

    } else {

      console.log("No hay overflow horizontal");
    }

  }, 300);

  // pausa táctil
  carouselInner.addEventListener(
    'touchstart',
    () => paused = true
  );

  carouselInner.addEventListener(
    'touchend',
    () => paused = false
  );

});