// Trigger all popovers
// -> Credit for popovers: https://getbootstrap.com/docs/5.2/components/popovers/#overview
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
