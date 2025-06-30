const fileInput = document.getElementById("fileInput");
const fileStatus = document.getElementById("fileStatus");
const imagePreview = document.getElementById("imagePreview");
const resultText = document.getElementById("resultText");
const bigTxt = document.getElementById("bigTxt");
const fruitDetails = document.getElementById("fruitDetails");
const show_perc = document.getElementById("show_perc");

const startCameraBtn = document.getElementById("startCameraBtn");
const captureBtn = document.getElementById("captureBtn");
const cameraStream = document.getElementById("cameraStream");
let stream;

// ========== FILE INPUT ========== //
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    fileStatus.textContent = "File selected: " + file.name;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      imageShow.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else {
    fileStatus.textContent = "No file selected";
    imagePreview.style.display = "none";
  }
});

// ========== FORM SUBMIT ========== //
document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const formData = new FormData();
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload or capture an image.");
    return;
  }

  formData.append("file", file);

  const response = await fetch("/predict", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  // Handle responses
  if (data.name) {
    resultText.innerHTML = "✨ " + data.name + " ✨";
    document.getElementById("fruitName").textContent = data.name;
    document.getElementById("fruitCategory").textContent = data.category;
    document.getElementById("fruitDescription").textContent = data.description;
    document.getElementById("fruitBenefits").textContent = data.fruit_benefits;
    document.getElementById("smoothieRecipe").textContent = data.smoothie_recipe;
    document.getElementById("similarFruits").textContent = data.similar_fruits;
    document.getElementById("percent").textContent = data.accuracy + "%";

    resultText.style.display = "block";
    bigTxt.style.display = "none";
    fruitDetails.style.display = data.category ? "block" : "none";
    show_perc.style.display = "block";
  }

  if (data.guess) {
    resultText.innerHTML = data.guess + " (Just guessing 😇)";
    percent.innerHTML = data.accuracy + "%";
    resultText.style.display = "block";
    bigTxt.style.display = "block";
    fruitDetails.style.display = "none";
    show_perc.style.display = "block";
  }

  if (data.undetected) {
    resultText.innerHTML = data.undetected + " 😞";
    resultText.style.display = "block";
    bigTxt.style.display = "block";
    fruitDetails.style.display = "none";
    show_perc.style.display = "none";
  }

  cameraStream.style.display = "none";
  showCapture.style.display = "none";
  startCameraBtn.style.display = "block";
});

// ========== CAMERA CAPTURE ========== //
startCameraBtn.addEventListener("click", async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    cameraStream.srcObject = stream;
    cameraStream.style.display = "block";
    showCapture.style.display = "inline-block";
    fileStatus.textContent = "Camera activated.";
    fileInput.style.display = "none";
    startCameraBtn.style.display = "none";
    resultText.style.display = "none";
    fruitDetails.style.display = "none";
    show_perc.style.display = "none";
    bigTxt.style.display = "block";
    imageShow.style.display = "none";
  } catch (err) {
    // alert("Camera access denied or not available.");
    alert(err);
  }
});

captureBtn.addEventListener("click", () => {
  const canvas = document.createElement("canvas");
  canvas.width = cameraStream.videoWidth;
  canvas.height = cameraStream.videoHeight;
  const context = canvas.getContext("2d");
  context.drawImage(cameraStream, 0, 0);

  // Convert canvas to blob
  canvas.toBlob((blob) => {
    const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;

    // Show image preview
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      imageShow.style.display = "block";
    };
    reader.readAsDataURL(file);

    fileStatus.textContent = "Photo captured from camera.";
  });

  // Stop camera
  stream.getTracks().forEach((track) => track.stop());
  cameraStream.style.display = "none";
  showCapture.style.display = "none";
});


