from flask import Flask, render_template_string, jsonify, request
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    html = """
    <html>
    <head><title>My Flask EC2 App</title></head>
    <body style="font-family: Arial; margin: 40px;">
        <h1>Welcome to Flask App on EC2!</h1>
        <p>This app is running directly on EC2 without Docker.</p>
        <ul>
            <li><a href="/fetch">/fetch - External API Call</a></li>
            <li><a href="/health">/health - Health Check</a></li>
        </ul>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/fetch')
def fetch_data():
    url = 'https://jsonplaceholder.typicode.com/todos'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[:5]
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/health')
def health():
    return jsonify({"status": "App is healthy and running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
