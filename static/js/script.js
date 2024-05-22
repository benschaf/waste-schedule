// Trigger all popovers
// -> Credit for popovers: https://getbootstrap.com/docs/5.2/components/popovers/#overview
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

window.addEventListener('scroll', (event) => {
    if (window.scrollY > 0) {
        console.log('scrolling');
        document.getElementsByTagName('nav')[0].classList.remove('bg-transparent');
    } else {
        if (!document.getElementsByTagName('nav')[0].classList.contains('bg-transparent')) {
            document.getElementsByTagName('nav')[0].classList.add('bg-transparent');
        }
    }
});

document.getElementsByClassName('navbar-toggler')[0].addEventListener('click', (event) => {
    if (window.scrollY == 0) {
        if (!document.getElementsByTagName('nav')[0].classList.contains('bg-transparent')) {
            document.getElementsByTagName('nav')[0].classList.add('bg-transparent');
        } else {
            document.getElementsByTagName('nav')[0].classList.remove('bg-transparent');
        }
    }
});