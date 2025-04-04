document.addEventListener('DOMContentLoaded', (event) => {
    const maxLength = 16; // Ajusta el número de caracteres según tus necesidades
    const equipoCells = document.querySelectorAll('.size_equipos');
    
    equipoCells.forEach(cell => {
      const text = cell.textContent;
      if (text.length > maxLength) {
        cell.textContent = text.slice(0, maxLength) + '...';
      }
    });
  });