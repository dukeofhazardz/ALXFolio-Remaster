document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector("header");
  
  var scrollThreshold = 50;

  function handleScroll() {
    if (window.scrollY > scrollThreshold) {
      header.classList.add("navbar-scrolled");
    } else {
      header.classList.remove("navbar-scrolled");
    }
  }

  window.addEventListener("scroll", handleScroll);
});