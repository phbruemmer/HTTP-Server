function setupMessageButton() {
    const button = document.getElementById('showMessageButton');
    if (button) {
        button.addEventListener('click', function() {
            alert('Alert!');
        });
    } else {
        console.error('No Button ID found.')
    }
}