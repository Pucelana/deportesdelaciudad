document.addEventListener("DOMContentLoaded", () => {

  const carouselInner = document.querySelector('#carouselExampleControls .carousel-inner');

  if (!carouselInner) return;

  if (!window.matchMedia("(max-width: 768px)").matches) return;

  // duplicar contenido
  carouselInner.innerHTML += carouselInner.innerHTML;

  let speed = 0.25 + Math.random() * 0.1;
  let paused = false;

  function loop() {
    if (!paused) {
      carouselInner.scrollLeft += speed;

      if (carouselInner.scrollLeft >= carouselInner.scrollWidth / 2) {
        carouselInner.scrollLeft = 0;
      }
    }

    requestAnimationFrame(loop);
  }

  loop();

  carouselInner.addEventListener('touchstart', () => paused = true);
  carouselInner.addEventListener('touchend', () => {
    paused = false;
  });

});