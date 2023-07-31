//burger icon animation and dropdown menu
function burgerDropMenu() {
    var burger = document.getElementById('burgerMenu');
    var links = document.getElementById("navLinks");
    burger.classList.toggle('opened');
    burger.setAttribute('aria-expanded', burger.classList.contains('opened'));
    if (links.style.display === "grid") {
      links.style.display = "none";
    } else {
      links.style.display = "grid";
    }
  }