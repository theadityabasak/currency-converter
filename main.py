from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

def get_live_rate(base, target):
    """
    Fetch the live exchange rate between two currencies using Frankfurter API.
    Returns the rate as a float or None if an error occurs.
    """
    url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # ensures 4xx/5xx errors raise exceptions
        data = response.json()
        return data.get('rates', {}).get(target)
    except (requests.RequestException, ValueError, KeyError):
        return None

@app.route('/convert')
def convert():
    base = request.args.get('base', '').upper()
    target = request.args.get('target', '').upper()

    if not base or not target:
        return jsonify({"error": "Please provide both base and target parameters"}), 400

    rate = get_live_rate(base, target)
    if rate is not None:
        return jsonify({
            "base": base,
            "target": target,
            "rate": rate,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify({"error": "Invalid input or API error"}), 400

if __name__ == '__main__':
    app.run(debug=True)
