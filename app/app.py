from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
requests_total = Counter('flask_app_requests_total', 'Total HTTP Requests')

@app.route("/")
def hello():
    requests_total.inc()
    return "Hello from Flask + K8s!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
