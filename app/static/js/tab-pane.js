document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {

    // quitar activos
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

    // activar botón
    btn.classList.add('active');

    // activar contenido
    const tab = document.getElementById(btn.dataset.tab);
    tab.classList.add('active');

  });
});