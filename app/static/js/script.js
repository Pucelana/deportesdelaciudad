const multipleItemCarousel = document.querySelector('#carouselExampleControls');

if (multipleItemCarousel && window.matchMedia("(min-width:320px)").matches) {
    const carousel = new bootstrap.Carousel(multipleItemCarousel, {
        interval: false
    });

    const carouselInner = $('.carousel-inner')[0];
    const carouselItem = $('.carousel-item').width();

    if (carouselInner && carouselItem) {
        let carouselWidth = carouselInner.scrollWidth;
        let cardWidth = carouselItem;
        let scrollPosition = 0;

        $('.carousel-control-next').on('click', function () {
            if (scrollPosition < (carouselWidth - (cardWidth * 2))) {
                scrollPosition = scrollPosition + cardWidth;
                $('.carousel-inner').animate({ scrollLeft: scrollPosition }, 600);
            }
        });

        $('.carousel-control-prev').on('click', function () {
            if (scrollPosition > 0) {
                scrollPosition = scrollPosition - cardWidth;
                $('.carousel-inner').animate({ scrollLeft: scrollPosition }, 600);
            }
        });
    }
} else {
    //console.warn('No se encontró el carrusel o pantalla demasiado pequeña');
    if (multipleItemCarousel) {
        $(multipleItemCarousel).addClass('slide');
    }
}

