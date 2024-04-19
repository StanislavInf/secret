const menuButton = document.querySelector(".menu-button");
const closeMenuButton = document.querySelector(".close-menu-button");

menuButton.addEventListener("click", toggleMenu);
closeMenuButton.addEventListener("click", toggleMenu);

function toggleMenu() {
  document.body.classList.toggle("sidebar-open");
}

