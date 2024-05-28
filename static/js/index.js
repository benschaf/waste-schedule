// -> Credit for redirecting to a url in javascript: https://stackoverflow.com/questions/503093/how-can-i-make-a-redirect-page-in-jquery-javascript
// Event Listener for the postcode form
document.getElementById('postcodeForm').addEventListener('submit', function (event) {
    event.preventDefault();
    var postcode = document.getElementById('postcodeInput').value;
    let url = window.location.href;
    url = url.substring(0, url.lastIndexOf('wasteschedules/')) + 'wasteschedules/location/' + postcode + '/';
    window.location.href = url;
});
