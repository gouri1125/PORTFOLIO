// Loading screen
window.addEventListener('load', () => {
    document.querySelector('.loader').classList.add('hidden');
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

// Mobile menu
document.querySelector('.hamburger').addEventListener('click', () => {
    document.getElementById('nav-menu').classList.toggle('active');
});
