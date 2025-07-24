document.addEventListener("DOMContentLoaded", function() {
    const uploadArea = document.getElementById("upload-area");
    const fileInput = document.getElementById("file-input");
    const uploadStatus = document.getElementById("upload-status");
    const filePreview = document.getElementById("file-preview");
    const fileInfo = document.getElementById("file-info");
    const viewNetworkBtn = document.getElementById("view-network-btn");

    // Drag events
    uploadArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", () => {
        uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadArea.classList.remove("dragover");
        const file = e.dataTransfer.files[0];
        handleFileUpload(file);
    });

    // File input
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        handleFileUpload(file);
    });

    // View network button
    viewNetworkBtn.addEventListener("click", () => {
        window.location.href = "/network";
    });

    function handleFileUpload(file) {
        if (!file) {
            updateStatus("No file selected", "red");
            return;
        }

        if (!file.name.endsWith(".dbc")) {
            updateStatus("Invalid file type - only .dbc files accepted", "red");
            return;
        }

        updateStatus("Uploading file...", "orange");
        filePreview.innerHTML = `<em>${file.name}</em>`;

        const formData = new FormData();
        formData.append("file", file);

        fetch("/upload_dbc", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                updateStatus("DBC FILE: successfully uploaded!", "lime");
                showFileInfo(data.filename, data.message_count, data.signal_count);
            } else {
                updateStatus("Upload failed: " + data.error, "red");
                hideFileInfo();
            }
        })
        .catch(error => {
            const errorMsg = error.error || "Server error";
            updateStatus("Upload failed: " + errorMsg, "red");
            hideFileInfo();
        });
    }

    function updateStatus(message, color) {
        uploadStatus.textContent = message;
        uploadStatus.style.color = color;
    }

    function showFileInfo(filename, messageCount, signalCount) {
        document.getElementById("info-filename").textContent = filename;
        document.getElementById("info-messages").textContent = messageCount;
        document.getElementById("info-signals").textContent = signalCount;
        fileInfo.style.display = "block";
    }

    function hideFileInfo() {
        fileInfo.style.display = "none";
    }
});