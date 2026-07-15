document.addEventListener("DOMContentLoaded", () => {

    const track = document.querySelector('.netflix-track');
    if (!track) return;

    /* =========================
       1. CLONAR PARA INFINITO
    ========================== */
    const items = Array.from(track.children);

    items.forEach(item => {
        const clone = item.cloneNode(true);
        track.appendChild(clone);
    });

    let scrollWidth = track.scrollWidth / 2;

    /* =========================
       2. LOOP INFINITO (SIN SALTOS)
    ========================== */
    track.addEventListener('scroll', () => {
        if (track.scrollLeft >= scrollWidth) {
            track.scrollLeft -= scrollWidth;
        }

        if (track.scrollLeft <= 0) {
            track.scrollLeft += scrollWidth;
        }
    });

    /* =========================
       3. AUTO SCROLL (NETFLIX STYLE)
    ========================== */
    let speed;
    function setSpeed() {
    const width = window.innerWidth;

    if (width <= 576) {
        speed = 0.35; // móvil (más suave)
    } else if (width <= 992) {
        speed = 0.6; // tablet
    } else {
        speed = 0.7; // desktop
    }
}
setSpeed();
window.addEventListener('resize', setSpeed);
    let isPaused = false;

    function autoScroll() {
        if (!isPaused) {
            track.scrollLeft += speed;
        }
        requestAnimationFrame(autoScroll);
    }

    autoScroll();

    /* =========================
       4. DRAG MOUSE (MANUAL CONTROL)
    ========================== */
    let isDown = false;
    let startX;
    let scrollLeft;

    track.addEventListener('mousedown', (e) => {
        isDown = true;
        isPaused = true; // pausa autoplay

        track.classList.add('active');

        startX = e.pageX - track.offsetLeft;
        scrollLeft = track.scrollLeft;
    });

    track.addEventListener('mouseleave', () => {
        isDown = false;
        isPaused = false;
        track.classList.remove('active');
    });

    track.addEventListener('mouseup', () => {
        isDown = false;
        isPaused = false;
        track.classList.remove('active');
    });

    track.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();

        const x = e.pageX - track.offsetLeft;
        const walk = (x - startX) * 2;

        track.scrollLeft = scrollLeft - walk;
    });

});

/* Admin */
document.addEventListener("DOMContentLoaded", () => {

    const track = document.querySelector('.admin-track');
    if (!track) return;

    let isDown = false;
    let startX;
    let scrollLeft;

    track.addEventListener('mousedown', (e) => {
        isDown = true;
        track.classList.add('active');

        startX = e.pageX - track.offsetLeft;
        scrollLeft = track.scrollLeft;
    });

    track.addEventListener('mouseleave', () => {
        isDown = false;
        track.classList.remove('active');
    });

    track.addEventListener('mouseup', () => {
        isDown = false;
        track.classList.remove('active');
    });

    track.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();

        const x = e.pageX - track.offsetLeft;
        const walk = (x - startX) * 2;

        track.scrollLeft = scrollLeft - walk;
    });

    // soporte táctil
    let touchStartX = 0;

    track.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].pageX;
        scrollLeft = track.scrollLeft;
    });

    track.addEventListener('touchmove', (e) => {
        const x = e.touches[0].pageX;
        const walk = (x - touchStartX) * 2;

        track.scrollLeft = scrollLeft - walk;
    });

});