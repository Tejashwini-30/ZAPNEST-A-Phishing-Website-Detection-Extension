"""
main.py — Unified Flask backend for phishing detection
------------------------------------------------------
✅ Serves both the local web UI and Chrome extension
✅ Uses trained XGBoost pipeline (phishing_simple_model.pkl)
✅ Returns probability + readable result
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import traceback
from utils import load_pipeline, extract_features_from_url, prepare_input

# Initialize app
app = Flask(__name__)
CORS(app)

# Load the trained model
pipe = load_pipeline()
print("🎯 Backend ready: Model + pipeline initialized")

# --------------------------------------------
# 🖥️ WEB UI TEMPLATE
# --------------------------------------------
HTML = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Phishing URL Detector</title></head>
<body style="font-family:Arial;background:#f6f7fb;padding:40px;">
<div style="background:#fff;padding:24px;border-radius:10px;box-shadow:0 8px 20px rgba(0,0,0,0.1);max-width:600px;margin:auto;">
  <h2>🔍 Phishing URL Detector</h2>
  <form method="POST">
    <input name="url" placeholder="Enter a URL (e.g. https://www.google.com)" style="width:90%;padding:10px;border:1px solid #ccc;border-radius:6px;">
    <button style="padding:10px 14px;background:#1976d2;color:#fff;border:none;border-radius:6px;">Check</button>
  </form>
  {% if result %}
  <p style="font-weight:bold;margin-top:15px;color:{{color}}">{{result}}</p>
  <p>Confidence (Phishing): {{conf}}</p>
  <pre style="background:#f7f9fb;padding:10px;border-radius:6px;">{{features}}</pre>
  {% endif %}
</div></body></html>
"""

# --------------------------------------------
# 🌐 WEB PAGE ROUTE (for testing)
# --------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        try:
            feats = extract_features_from_url(url)
            df = prepare_input(feats)
            prob_phish = float(pipe.predict_proba(df)[0][0])  # class 0 = phishing
            pred = "⚠️ Phishing Website" if prob_phish >= 0.5 else "✅ Legitimate Website"
            color = "#c62828" if prob_phish >= 0.5 else "#2e7d32"
            return render_template_string(
                HTML, result=pred, conf=f"{prob_phish:.3f}", color=color, features=feats
            )
        except Exception as e:
            traceback.print_exc()
            return render_template_string(
                HTML, result=f"❌ Error: {e}", conf="N/A", color="#b71c1c", features={}
            )
    return render_template_string(HTML, result=None, conf=None, color="#000", features={})


# --------------------------------------------
# 🔗 API ROUTE (for Chrome Extension)
# --------------------------------------------
@app.route("/predict_url", methods=["POST"])
def predict_url():
    """
    JSON input: { "url": "https://example.com" }
    JSON output: { "prediction": "Phishing"/"Legitimate", "confidence": 0.87, "features": {...} }
    """
    try:
        data = request.get_json()
        url = data.get("url", "").strip()
        feats = extract_features_from_url(url)
        df = prepare_input(feats)
        prob_phish = float(pipe.predict_proba(df)[0][0])  # class 0 = phishing
        label = "Phishing" if prob_phish >= 0.5 else "Legitimate"
        return jsonify({
            "url": url,
            "prediction": label,
            "confidence": round(prob_phish, 3),
            "features": feats
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# --------------------------------------------
# 🚀 ENTRY POINT
# --------------------------------------------
if __name__ == "__main__":
    print("🚀 Flask backend running at: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
