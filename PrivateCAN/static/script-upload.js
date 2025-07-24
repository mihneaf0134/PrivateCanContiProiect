const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-input");
const uploadStatus = document.getElementById("upload-status");

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

function handleFileUpload(file) {
  if (!file || !file.name.endsWith(".dbc")) {
    uploadStatus.textContent = "Upload failed: invalid file type!";
    uploadStatus.style.color = "red";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload_dbc", {
    method: "POST",
    body: formData,
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        uploadStatus.textContent = "DBC FILE: successfully uploaded!";
        uploadStatus.style.color = "lime";
      } else {
        uploadStatus.textContent = "Upload failed: " + data.error;
        uploadStatus.style.color = "red";
      }
    })
    .catch(() => {
      uploadStatus.textContent = "Upload failed: server error";
      uploadStatus.style.color = "red";
    });
}

