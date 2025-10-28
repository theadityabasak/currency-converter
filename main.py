from flask import Flask, request, jsonify
import requests
from datetime import datetime
import csv
import os

app = Flask(__name__)

def get_live_rate(base, target):
    try:
        url = f"https://api.frankfurter.app/latest?from={base}&to={target}"
        data = requests.get(url).json()
        return data['rates'][target]
    except Exception:
        return None

def save_to_csv(base, target, rate):
    filename = 'conversion_history.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['base', 'target', 'rate', 'timestamp'])
        writer.writerow([base, target, rate, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

@app.route('/convert')
def convert():
    base = request.args.get('base', '').upper()
    target = request.args.get('target', '').upper()
    
    if not base or not target:
        return jsonify({"error": "Please provide both base and target parameters"}), 400
    
    rate = get_live_rate(base, target)
    if rate:
        save_to_csv(base, target, rate)
        return jsonify({
            "base": base,
            "target": target,
            "rate": rate,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({"error": "Invalid input or API error"}), 400

if __name__ == '__main__':
    app.run(debug=True)