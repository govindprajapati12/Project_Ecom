const mobileMenuButton = document.getElementById('mobile-menu-button');
const mainNav = document.getElementById('main-nav');

mobileMenuButton.addEventListener('click', () => {
    mainNav.classList.toggle('show');
});

