document.getElementById("checkBtn").addEventListener("click", async () => {
  const statusDiv = document.getElementById("status");
  statusDiv.textContent = "Analyzing...";
  statusDiv.className = "";

  // Get current tab URL
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const currentURL = tab.url;

  try {
    const response = await fetch("http://localhost:5000/predict_url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: currentURL })
    });

    const data = await response.json();

    if (data.prediction === "Phishing") {
      statusDiv.textContent = `⚠️ Phishing Detected! (Confidence: ${data.confidence})`;
      statusDiv.className = "phish";
    } else {
      statusDiv.textContent = `✅ Safe Website (Confidence: ${data.confidence})`;
      statusDiv.className = "safe";
    }
  } catch (err) {
    console.error("Error:", err);
    statusDiv.textContent = "❌ Could not connect to backend.";
  }
});
