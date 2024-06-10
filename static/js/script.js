document.addEventListener('DOMContentLoaded', function () {
    // -> Credit for popovers: https://getbootstrap.com/docs/5.2/components/popovers/#overview
    // Trigger all popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));

    // Event Listener for navbar background toggling on scroll
    window.addEventListener('scroll', (event) => {
        const navBar = document.getElementsByTagName('nav')[0];
        if (window.scrollY > 0) {
            navBar.classList.remove('bg-transparent');
            navBar.classList.add('shadow-lg');
        } else {
            if (!navBar.classList.contains('bg-transparent')) {
                navBar.classList.add('bg-transparent');
                navBar.classList.remove('shadow-lg');
            }
        }
    });

    // Event Listener for toggler background toggling on click
    document.getElementsByClassName('navbar-toggler')[0].addEventListener('click', (event) => {
        if (window.scrollY == 0) {
            const navBar = document.getElementsByTagName('nav')[0];
            if (!navBar.classList.contains('bg-transparent')) {
                navBar.classList.add('bg-transparent');
                navBar.classList.remove('shadow-lg');
            } else {
                navBar.classList.remove('bg-transparent');
                navBar.classList.add('shadow-lg');
            }
        }
    });

    // Remove the message elements after 5 seconds
    setTimeout(function () {
        let alerts = document.querySelectorAll('.message-class');
        alerts.forEach(function (alert) {
            alert.style.display = 'none';
        });
    }, 5000);
});