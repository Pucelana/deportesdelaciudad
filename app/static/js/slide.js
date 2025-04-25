document.querySelectorAll('#carouselNavTabs .nav-link').forEach((link, index) => {
    link.addEventListener('click', () => {
      document.querySelectorAll('#carouselNavTabs .nav-link').forEach(el => el.classList.remove('active'));
      link.classList.add('active');
    });
  });