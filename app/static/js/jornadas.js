document.querySelectorAll(".btn-jornada").forEach(btn => {
  btn.addEventListener("click", function (e) {
    e.preventDefault();

    const target = this.dataset.target;

    // quitar active botones
    document.querySelectorAll(".btn-jornada")
      .forEach(b => b.classList.remove("active"));

    this.classList.add("active");

    // ocultar jornadas
    document.querySelectorAll(".jornada-contenido")
      .forEach(j => j.classList.remove("active"));

    // mostrar seleccionada
    const section = document.getElementById(target);
    if (section) section.classList.add("active");
  });
});