document.addEventListener("DOMContentLoaded", function() {
    // Edit Signal modal logic
    const modal = document.getElementById("edit-signal-modal");
    const openModalBtn = document.getElementById("edit-signal-btn");
    const closeModalBtn = document.getElementById("close-modal");

    if (openModalBtn) {
        openModalBtn.addEventListener("click", () => {
            modal.style.display = "flex";
        });
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

    const signalForm = document.getElementById("edit-signal-form");
    if (signalForm) {
        signalForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const signalData = Object.fromEntries(formData.entries());

            fetch('/api/update_signal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(signalData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    modal.style.display = "none";
                    alert('Signal updated successfully!');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating signal');
            });
        });
    }

    // Message Modal
    const msgModal = document.getElementById("edit-message-modal");
    const openMsgBtn = document.getElementById("edit-message-btn");
    const closeMsgBtn = document.getElementById("close-message-modal");

    if (openMsgBtn) {
        openMsgBtn.addEventListener("click", () => {
            msgModal.style.display = "flex";
        });
    }

    if (closeMsgBtn) {
        closeMsgBtn.addEventListener("click", () => {
            msgModal.style.display = "none";
        });
    }

    window.addEventListener("click", (e) => {
        if (e.target === msgModal) {
            msgModal.style.display = "none";
        }
    });

    const msgForm = document.getElementById("edit-message-form");
    if (msgForm) {
        msgForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const messageData = Object.fromEntries(formData.entries());

            fetch('/api/update_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(messageData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    msgModal.style.display = "none";
                    alert('Message updated successfully!');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating message');
            });
        });
    }
});