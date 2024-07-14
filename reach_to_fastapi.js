async function send_to_reach() {
    const from_link = document.getElementById('from_link').value;
    const to_link = document.getElementById('to_link').value;
    try {
        const response = await fetch('http://127.0.0.1:8000/reach', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ from_link: from_link, to_link: to_link })
        });
        const result = await response.text();
        document.getElementById('responseContainer').style.display = 'block';
        document.getElementById('response').innerHTML = `${result}`;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('responseContainer').style.display = 'block';
        document.getElementById('response').innerHTML = 'Error: Unable to send data to the server.';
    }
}
