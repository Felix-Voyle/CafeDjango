//burger icon animation and dropdown menu
function burgerDropMenu() {
    var burger = document.getElementById('burgerMenu');
    var links = document.getElementById("navLinks");
    var logo = document.getElementById("logo");
    burger.classList.toggle('opened');
    logo.classList.toggle('menu-logo')
    burger.setAttribute('aria-expanded', burger.classList.contains('opened'));
    if (links.style.display === "grid") {
      links.style.display = "none";
    } else {
      links.style.display = "grid";
    }
  }