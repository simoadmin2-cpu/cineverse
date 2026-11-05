document.addEventListener("DOMContentLoaded", () => {
  // Navbar Scroll
  const header = document.querySelector(".site-header");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) header.style.background = "var(--bg)";
    else header.style.background = "linear-gradient(to bottom, rgba(11,11,15,0.9) 0%, rgba(11,11,15,0) 100%)";
  });

  // Horizontal Scroll
  document.querySelectorAll(".scroll-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const row = e.target.closest(".row-header").nextElementSibling;
      const scrollAmount = row.clientWidth * 0.8;
      if (btn.classList.contains("next")) row.scrollBy({ left: scrollAmount, behavior: "smooth" });
      else row.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    });
  });

  // Hero Auto-Slider
  const heroSlides = document.querySelectorAll('.hero-slide');
  const heroInfos = document.querySelectorAll('.hero-info');
  
  if (heroSlides.length > 1) {
    let currentSlide = 0;
    setInterval(() => {
      // Hide current
      heroSlides[currentSlide].style.opacity = '0';
      heroInfos[currentSlide].style.display = 'none';
      
      // Next slide
      currentSlide = (currentSlide + 1) % heroSlides.length;
      
      // Show next
      heroSlides[currentSlide].style.opacity = '1';
      heroInfos[currentSlide].style.display = 'block';
    }, 5000); // 5 seconds
  }

  // Mobile Menu
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const closeMenuBtn = document.getElementById('closeMenu');
  const mobileMenu = document.getElementById('mobileMenu');
  if (mobileMenuBtn && mobileMenu) mobileMenuBtn.addEventListener('click', () => mobileMenu.classList.add('active'));
  if (closeMenuBtn && mobileMenu) closeMenuBtn.addEventListener('click', () => mobileMenu.classList.remove('active'));
});
