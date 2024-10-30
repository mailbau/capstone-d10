import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/dbforwarder', methods=['POST'])
def dbforwarder():
    if not request.json or 'destination_url' not in request.json or 'method' not in request.json:
        return jsonify({"error": "Invalid request format. 'destination_url' and 'method' are required."}), 400

    destination_url = request.json.pop('destination_url')
    method = request.json.pop('method')
    payload = request.json

    try:
        response = requests.request(
            method=method,
            url=destination_url,
            json=payload
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
    try:
        response_data = response.json()  # Fallback to JSON if not HTML
    except ValueError:
        response_data = response.text

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5001, debug=True, host='0.0.0.0')