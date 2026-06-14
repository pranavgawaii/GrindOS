document.addEventListener("DOMContentLoaded", () => {
  const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:8000' 
      : '';

  // Elements
  const btnCamera = document.getElementById("btn-camera");
  const btnUpload = document.getElementById("btn-upload");
  const viewUpload = document.getElementById("view-upload");
  
  const cameraInput = document.getElementById("cameraInput");
  const fileInput = document.getElementById("fileInput");
  const dropZone = document.getElementById("drop-zone");
  const imagePreviewContainer = document.getElementById("image-preview-container");
  const imagePreview = document.getElementById("image-preview");
  const analyzeImageBtn = document.getElementById("analyzeImageBtn");

  const resultContent = document.getElementById("result-content");
  const loadingState = document.getElementById("loading-state");
  const copyBtn = document.getElementById("copyBtn");

  const viewWelcome = document.getElementById("view-welcome");
  const startCameraBtn = document.getElementById("startCameraBtn");
  const startUploadBtn = document.getElementById("startUploadBtn");
  const modeToggleContainer = document.getElementById("mode-toggle-container");

  // Redesigned Control Elements
  const btnRotate = document.getElementById("btn-rotate");
  const btnExpand = document.getElementById("btn-expand");
  const btnChangeImage = document.getElementById("btn-change-image");
  
  // Lightbox elements
  const lightboxModal = document.getElementById("lightboxModal");
  const lightboxImage = document.getElementById("lightboxImage");
  const closeLightbox = document.getElementById("closeLightbox");

  let capturedBase64 = null;

  // Initial State is Welcome View. Tabs inactive.
  btnCamera.classList.remove("active");
  btnUpload.classList.remove("active");

  // Welcome Screen actions
  startCameraBtn.addEventListener("click", () => {
    cameraInput.click();
  });

  startUploadBtn.addEventListener("click", () => {
    fileInput.click();
  });

  // Top toggle tab actions
  btnCamera.addEventListener("click", () => {
    cameraInput.click();
  });

  btnUpload.addEventListener("click", () => {
    fileInput.click();
  });

  // Listen for file selections
  cameraInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleImageSelection(e.target.files[0], "camera");
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleImageSelection(e.target.files[0], "upload");
    }
  });

  // Drag-and-drop
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
      handleImageSelection(e.dataTransfer.files[0], "upload");
    }
  });

  // Core handler to load, downscale, and auto-process selected image
  async function handleImageSelection(file, source) {
    if (!file.type.startsWith("image/")) {
      alert("Please select an image file.");
      return;
    }

    // Set active tab styling
    if (source === "camera") {
      btnCamera.classList.add("active");
      btnUpload.classList.remove("active");
    } else {
      btnUpload.classList.add("active");
      btnCamera.classList.remove("active");
    }

    // Show loading indicators
    resultContent.classList.add("hidden");
    resultContent.classList.remove("empty");
    copyBtn.classList.add("hidden");
    loadingState.classList.remove("hidden");

    try {
      let width, height, imageSource;
      let isBitmap = false;

      if (typeof window.createImageBitmap === "function") {
        // createImageBitmap automatically respects EXIF orientation
        const bitmap = await createImageBitmap(file);
        width = bitmap.width;
        height = bitmap.height;
        imageSource = bitmap;
        isBitmap = true;
      } else {
        // Fallback for older browsers
        const dataUrl = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = (e) => resolve(e.target.result);
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
        const img = await new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = () => resolve(image);
          image.onerror = reject;
          image.src = dataUrl;
        });
        width = img.width;
        height = img.height;
        imageSource = img;
      }

      // Downscale image if it exceeds 1600px to ensure Vercel 4.5MB payload limit is respected
      const canvas = document.createElement("canvas");
      const maxDim = 1600;

      if (width > maxDim || height > maxDim) {
        if (width > height) {
          height = Math.round((height * maxDim) / width);
          width = maxDim;
        } else {
          width = Math.round((width * maxDim) / height);
          height = maxDim;
        }
      }

      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(imageSource, 0, 0, width, height);

      // Clean up bitmap if used
      if (isBitmap && typeof imageSource.close === "function") {
        imageSource.close();
      }

      // Convert to high quality compressed JPEG (saving size dramatically)
      capturedBase64 = canvas.toDataURL("image/jpeg", 0.85);

      // Update preview image
      imagePreview.src = capturedBase64;
      
      // Hide welcome screen and show preview container
      viewWelcome.classList.add("hidden");
      viewUpload.classList.remove("hidden");
      dropZone.classList.add("hidden");
      imagePreviewContainer.classList.remove("hidden");
      modeToggleContainer.classList.remove("hidden");

      // Automatically call vision API extraction
      extractText(capturedBase64);

    } catch (err) {
      console.error("Error loading image:", err);
      // Fallback: load using simple FileReader without downscaling to keep orientation
      try {
        const dataUrl = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = (e) => resolve(e.target.result);
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
        capturedBase64 = dataUrl;
        imagePreview.src = capturedBase64;
        
        viewWelcome.classList.add("hidden");
        viewUpload.classList.remove("hidden");
        dropZone.classList.add("hidden");
        imagePreviewContainer.classList.remove("hidden");
        modeToggleContainer.classList.remove("hidden");

        extractText(capturedBase64);
      } catch (fallbackErr) {
        console.error("Fallback image load failed:", fallbackErr);
        alert("Failed to load image. Please try another one.");
        loadingState.classList.add("hidden");
        resultContent.classList.remove("hidden");
        resultContent.classList.add("empty");
      }
    }
  }

  analyzeImageBtn.addEventListener("click", () => {
    if (capturedBase64) {
      extractText(capturedBase64);
    }
  });

  // Discard & Reset flow
  btnChangeImage.addEventListener("click", () => {
    capturedBase64 = null;
    imagePreview.src = "";
    
    // Reset inputs
    cameraInput.value = "";
    fileInput.value = "";
    
    // Display welcome panel
    imagePreviewContainer.classList.add("hidden");
    dropZone.classList.remove("hidden");
    viewUpload.classList.add("hidden");
    modeToggleContainer.classList.add("hidden");
    viewWelcome.classList.remove("hidden");
    
    // Reset tabs
    btnCamera.classList.remove("active");
    btnUpload.classList.remove("active");
    
    // Clear results
    resultContent.innerHTML = '<p class="placeholder-text">Capture or upload an image to see the extracted text here.</p>';
    resultContent.classList.add("empty");
    resultContent.classList.remove("hidden");
    copyBtn.classList.add("hidden");
    loadingState.classList.add("hidden");
  });

  // Canvas Image Rotation (90 degrees clockwise)
  btnRotate.addEventListener("click", () => {
    if (!capturedBase64) return;

    // Show loading indicators
    resultContent.classList.add("hidden");
    copyBtn.classList.add("hidden");
    loadingState.classList.remove("hidden");

    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      // Swap width and height for 90 degree rotation
      canvas.width = img.height;
      canvas.height = img.width;
      
      const ctx = canvas.getContext("2d");
      
      // Translate to center, rotate 90 deg clockwise, and draw
      ctx.translate(canvas.width / 2, canvas.height / 2);
      ctx.rotate((90 * Math.PI) / 180);
      ctx.drawImage(img, -img.width / 2, -img.height / 2);
      
      // Regenerate base64 image data
      capturedBase64 = canvas.toDataURL("image/jpeg", 0.85);
      imagePreview.src = capturedBase64;
      
      // Auto-extract rotated text
      extractText(capturedBase64);
    };
    img.src = capturedBase64;
  });

  // Fullscreen Expand (Lightbox modal)
  const openLightbox = () => {
    if (!capturedBase64) return;
    lightboxImage.src = capturedBase64;
    lightboxModal.style.display = "flex";
  };

  imagePreview.addEventListener("click", openLightbox);
  btnExpand.addEventListener("click", openLightbox);

  // Close Lightbox
  const closeLightboxModal = () => {
    lightboxModal.style.display = "none";
    lightboxImage.src = "";
  };

  closeLightbox.addEventListener("click", closeLightboxModal);
  lightboxModal.addEventListener("click", (e) => {
    if (e.target === lightboxModal) {
      closeLightboxModal();
    }
  });

  // ESC key to close lightbox
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && lightboxModal.style.display === "flex") {
      closeLightboxModal();
    }
  });

  // Vision API Call
  async function extractText(base64Data) {
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
        let errorMsg = `API Error: ${response.status}`;
        try {
          const errData = await response.json();
          if (errData && errData.detail) {
            errorMsg = `${errData.detail}`;
          }
        } catch (_) {}
        throw new Error(errorMsg);
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

  // Copy to clipboard
  copyBtn.addEventListener("click", () => {
    const textToCopy = resultContent.getAttribute("data-raw") || resultContent.innerText;
    navigator.clipboard.writeText(textToCopy).then(() => {
      const copyBtnSvg = copyBtn.querySelector("svg");
      const copyBtnSpan = copyBtn.querySelector("span");
      
      const originalHTML = copyBtn.innerHTML;
      
      copyBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> <span style="color: #10b981;">Copied!</span>`;
      setTimeout(() => {
        copyBtn.innerHTML = originalHTML;
      }, 2000);
    });
  });
});
