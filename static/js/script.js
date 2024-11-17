function handleFormSubmit() {
    // Show the loading text
    document.getElementById('loading').style.display = 'block';

    // Hide the loading text after 2 seconds to simulate processing time
    setTimeout(() => {
        document.getElementById('loading').style.display = 'none';
    }, 2000);

    // Allow form submission to continue
    return true;
}
