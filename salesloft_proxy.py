from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/proxy-to-salesloft', methods=['POST'])
def proxy_to_salesloft():
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({"error": "Missing API Key"}), 400

    incoming_data = request.get_json()
    if not incoming_data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 422

    # 🔍 DEBUG: print the JSON you're sending to Salesloft
    print("\n=== Incoming JSON sent to Salesloft ===")
    print(incoming_data)

    try:
        response = requests.post(
            "https://api.salesloft.com/v2/cadence_imports.json",
            headers={
                "Authorization": api_key,
                "Content-Type": "application/json"
            },
            json=incoming_data,
            timeout=10  # add a timeout to avoid hanging
        )

        print("\n=== Salesloft API Response ===")
        print("Status:", response.status_code)
        print(response.text)

        return (response.text, response.status_code, response.headers.items())

    except requests.exceptions.RequestException as e:
        print("\n🚨 Request to Salesloft failed:", e)
        return jsonify({"error": "Failed to reach Salesloft API", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3001)
