async function send_to_reach() {
    const from_link = document.getElementById('from_link').value;
    const to_link = document.getElementById('to_link').value;
    const loadingMessage = document.getElementById('loading');
    const responseContainer = document.getElementById('responseContainer');
    loadingMessage.style.display = 'block';
    responseContainer.style.display = 'none';
    startLoadingAnimation();
    try {
        const response = await fetch('http://127.0.0.1:8000/reach', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ from_link: from_link, to_link: to_link })
        });
        const result = await response.json();
        document.getElementById('responseContainer').style.display = 'block';
        if (result.error) {
            document.getElementById('response').innerHTML = `<p><strong>Error:</strong> ${result.error}</p>`;
        } else {
            const formattedResult = `<b>Links found:</b> ${result.links}
                <br><b>Shortest path:</b> ${result.path}
                <br><b>Time:</b> ${result.time}
            `;
            document.getElementById('response').innerHTML = formattedResult;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('responseContainer').style.display = 'block';
        document.getElementById('response').innerHTML = `Error: ${error.message}`;
    }
    finally {
        stopLoadingAnimation();
        loadingMessage.style.display = 'none';
    }
}

function startLoadingAnimation() {
    const loadingMessage = document.getElementById('loading');
    let dots = '';
    loadingInterval = setInterval(() => {
        dots += '.';
        if (dots.length > 3) {
            dots = '';
        }
        loadingMessage.textContent = `Loading${dots}`;
    }, 500);
}

function stopLoadingAnimation() {
    clearInterval(loadingInterval);
    const loadingMessage = document.getElementById('loading');
    loadingMessage.textContent = 'Loading';
}
