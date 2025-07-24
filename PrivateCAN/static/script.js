document.addEventListener("DOMContentLoaded", function() {
    // Connect button functionality
    const connectBtn = document.getElementById("connectBtn");
    if (connectBtn) {
        connectBtn.addEventListener("click", function() {
            fetch('/connect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                const status = document.getElementById("status");
                if (data.status === 'connected') {
                    status.textContent = "Connected :D";
                    status.style.color = "#0f0";
                } else {
                    status.textContent = "Connection failed :(";
                    status.style.color = "#f00";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const status = document.getElementById("status");
                status.textContent = "Connection error :(";
                status.style.color = "#f00";
            });
        });
    }
});