document.addEventListener("DOMContentLoaded", () => {
  const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:8000' 
      : '';

  // Elements
  const btnCamera = document.getElementById("btn-camera");
  const btnUpload = document.getElementById("btn-upload");
  const viewCamera = document.getElementById("view-camera");
  const viewUpload = document.getElementById("view-upload");
  
  const videoElement = document.getElementById("videoElement");
  const canvasElement = document.getElementById("canvasElement");
  const captureBtn = document.getElementById("captureBtn");
  const cameraStatus = document.getElementById("camera-status");

  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("fileInput");
  const imagePreviewContainer = document.getElementById("image-preview-container");
  const imagePreview = document.getElementById("image-preview");
  const analyzeImageBtn = document.getElementById("analyzeImageBtn");

  const resultContent = document.getElementById("result-content");
  const loadingState = document.getElementById("loading-state");
  const copyBtn = document.getElementById("copyBtn");

  let stream = null;
  let capturedBase64 = null;

  // --- TABS ---
  const viewWelcome = document.getElementById("view-welcome");
  const startCameraBtn = document.getElementById("startCameraBtn");
  const startUploadBtn = document.getElementById("startUploadBtn");
  const modeToggleContainer = document.getElementById("mode-toggle-container");

  // Initial State is Welcome View. Tabs inactive.
  btnCamera.classList.remove("active");
  btnUpload.classList.remove("active");

  startCameraBtn.addEventListener("click", () => {
    viewWelcome.classList.add("hidden");
    modeToggleContainer.classList.remove("hidden");
    btnCamera.click();
  });

  startUploadBtn.addEventListener("click", () => {
    viewWelcome.classList.add("hidden");
    modeToggleContainer.classList.remove("hidden");
    btnUpload.click();
  });

  btnCamera.addEventListener("click", () => {
    viewWelcome.classList.add("hidden");
    btnCamera.classList.add("active");
    btnUpload.classList.remove("active");
    viewCamera.classList.remove("hidden");
    viewUpload.classList.add("hidden");
    startCamera();
  });

  btnUpload.addEventListener("click", () => {
    viewWelcome.classList.add("hidden");
    btnUpload.classList.add("active");
    btnCamera.classList.remove("active");
    viewUpload.classList.remove("hidden");
    viewCamera.classList.add("hidden");
    stopCamera();
  });

  // --- CAMERA LOGIC ---
  async function startCamera() {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: "environment", width: { ideal: 1920 }, height: { ideal: 1080 } } 
      });
      videoElement.srcObject = stream;
      cameraStatus.innerText = "Align code within the frame and capture";
    } catch (err) {
      console.error("Camera error:", err);
      cameraStatus.innerText = "Could not access camera. Please check permissions.";
    }
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      stream = null;
    }
  }

  captureBtn.addEventListener("click", () => {
    if (!stream) return;
    
    // Draw current frame to canvas
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    const ctx = canvasElement.getContext("2d");
    ctx.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
    
    // Convert to base64
    capturedBase64 = canvasElement.toDataURL("image/jpeg", 0.9);
    
    // Visual flash
    const overlay = document.querySelector(".camera-overlay");
    overlay.style.background = "rgba(255,255,255,0.8)";
    setTimeout(() => {
      overlay.style.background = "transparent";
    }, 100);

    extractText(capturedBase64);
  });

  // --- UPLOAD LOGIC ---
  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  });

  function handleFile(file) {
    if (!file.type.startsWith("image/")) {
      alert("Please upload an image file.");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      capturedBase64 = e.target.result;
      imagePreview.src = capturedBase64;
      dropZone.classList.add("hidden");
      imagePreviewContainer.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
  }

  analyzeImageBtn.addEventListener("click", () => {
    if (capturedBase64) {
      extractText(capturedBase64);
    }
  });

  // --- API CALL ---
  async function extractText(base64Data) {
    // Show loading
    resultContent.classList.add("hidden");
    resultContent.classList.remove("empty");
    copyBtn.classList.add("hidden");
    loadingState.classList.remove("hidden");

    try {
      const response = await fetch(`${apiBase}/api/practice/extract-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_base64: base64Data })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      
      // Render markdown text
      resultContent.innerHTML = marked.parse(data.extracted_text);
      
      // Syntax highlighting for code blocks
      document.querySelectorAll('#result-content pre code').forEach((block) => {
        hljs.highlightElement(block);
      });

      // Show result
      loadingState.classList.add("hidden");
      resultContent.classList.remove("hidden");
      copyBtn.classList.remove("hidden");
      
      // Save raw text for copying
      resultContent.setAttribute("data-raw", data.extracted_text);

    } catch (err) {
      console.error(err);
      loadingState.classList.add("hidden");
      resultContent.classList.remove("hidden");
      resultContent.innerHTML = `<p style="color: #ff6b6b">Failed to extract text. ${err.message}</p>`;
    }
  }

  // --- COPY LOGIC ---
  copyBtn.addEventListener("click", () => {
    const textToCopy = resultContent.getAttribute("data-raw") || resultContent.innerText;
    navigator.clipboard.writeText(textToCopy).then(() => {
      const originalHTML = copyBtn.innerHTML;
      copyBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
      setTimeout(() => {
        copyBtn.innerHTML = originalHTML;
      }, 2000);
    });
  });

  // Start camera by default removed for better UX
});
