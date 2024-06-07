// Show the download instructions modal when the download button is clicked
const downloadButtons = document.getElementsByClassName('downloadButton');
for (const downloadButton of downloadButtons) {
    downloadButton.addEventListener('click', () => {
        const downloadInstructionsModal = new bootstrap.Modal(document.getElementById('downloadInstructionsModal'));
        downloadInstructionsModal.show();
    });
}
