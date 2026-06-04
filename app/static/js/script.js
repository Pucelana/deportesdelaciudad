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
       2. SCROLL LOOP
    ========================== */
    track.addEventListener('scroll', () => {
        if (track.scrollLeft >= scrollWidth) {
            track.scrollLeft = 1; // evita salto brusco
        }

        if (track.scrollLeft <= 0) {
            track.scrollLeft = scrollWidth - 1;
        }
    });

    /* =========================
       3. DRAG MOUSE (NETFLIX)
    ========================== */
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

});