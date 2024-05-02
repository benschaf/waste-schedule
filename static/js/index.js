// -> Credit for redirecting to a url in javascript: https://stackoverflow.com/questions/503093/how-can-i-make-a-redirect-page-in-jquery-javascript
document.getElementById('postcodeForm').addEventListener('submit', function (event) {
    event.preventDefault();
    var postcode = document.getElementById('postcodeInput').value;
    var url = 'wasteschedules/location/' + postcode + '/';
    window.location.href = url;
});