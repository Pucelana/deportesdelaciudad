document.addEventListener("DOMContentLoaded", () => {

  const botones = document.querySelectorAll(".tab-btn");
  const secciones = document.querySelectorAll(".tab-pane");

  function activarTab(tabId, botonActivo) {

    // ocultar todo
    secciones.forEach(sec => {
      sec.classList.add("d-none");
      sec.classList.remove("active");
    });

    // mostrar solo el correcto
    const target = document.getElementById(tabId);

    if (target) {
      target.classList.remove("d-none");
      target.classList.add("active");
    }

    // estado botones
    botones.forEach(b => b.classList.remove("active"));
    botonActivo.classList.add("active");
  }

  botones.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      activarTab(btn.dataset.tab, btn);
    });
  });

  // activar primero por defecto
  const first = document.querySelector(".tab-btn");
  if (first) {
    activarTab(first.dataset.tab, first);
  }

});