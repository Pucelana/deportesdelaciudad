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
    let speed = 0.8;
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