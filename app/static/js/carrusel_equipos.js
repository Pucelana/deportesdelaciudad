document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {

    // quitar active de todos
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

    // activar botón actual
    btn.classList.add('active');

    // ocultar todas las slides
    document.querySelectorAll('.carousel-item').forEach(el => {
      el.classList.remove('active');
    });

    // mostrar la seleccionada
    const target = btn.dataset.target;
    const el = document.getElementById(target);

    if (el) {
      el.classList.add('active');
    }
  });
});