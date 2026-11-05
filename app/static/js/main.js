document.addEventListener("DOMContentLoaded", () => {
  // 1. Add class to HTML for JS styling
  document.documentElement.classList.add("js-ready");

  // 2. Navbar background on scroll
  const header = document.querySelector(".site-header");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header.style.background = "var(--bg)";
    } else {
      header.style.background = "linear-gradient(to bottom, rgba(11,11,15,0.9) 0%, rgba(11,11,15,0) 100%)";
    }
  });

  // 3. Horizontal Scroll Controls
  const scrollBtns = document.querySelectorAll(".scroll-btn");
  scrollBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      const row = e.target.closest(".row-header").nextElementSibling;
      const scrollAmount = row.clientWidth * 0.8;
      if (btn.classList.contains("next")) {
        row.scrollBy({ left: scrollAmount, behavior: "smooth" });
      } else {
        row.scrollBy({ left: -scrollAmount, behavior: "smooth" });
      }
    });
  });
});
// Mobile Menu Logic
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const closeMenuBtn = document.getElementById('closeMenu');
const mobileMenu = document.getElementById('mobileMenu');

if (mobileMenuBtn && mobileMenu) {
  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.add('active');
  });
}
if (closeMenuBtn && mobileMenu) {
  closeMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('active');
  });
}
