document.addEventListener('DOMContentLoaded', function() {
    const multipleItemCarousel = document.querySelector('#carouselExampleControls');
    if (multipleItemCarousel) {
      const carousel = new bootstrap.Carousel(multipleItemCarousel, {
        interval: false // Disable automatic cycling
      });
      
      const carouselInner = document.querySelector('.carousel-inner');
      const carouselWidth = carouselInner.scrollWidth;
      const cardWidth = document.querySelector('.carousel-item').offsetWidth;
      let scrollPosition = 0;
  
      document.querySelector('.carousel-control-next').addEventListener('click', function() {
        if (scrollPosition < (carouselWidth - cardWidth * 2)) {
          scrollPosition += cardWidth;
          carouselInner.scrollBy({ left: cardWidth, behavior: 'smooth' });
        }
      });
  
      document.querySelector('.carousel-control-prev').addEventListener('click', function() {
        if (scrollPosition > 0) {
          scrollPosition -= cardWidth;
          carouselInner.scrollBy({ left: -cardWidth, behavior: 'smooth' });
        }
      });
    } else {
      console.error('Elemento no encontrado con el ID carouselExampleControls');
    }
  });