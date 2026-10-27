import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Same namespace, so the Kubernetes Service name alone is enough.
# "backend-service" is resolved by cluster DNS to the backend Service.
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:5000")


@app.route("/")
def index():
    try:
        resp = requests.get(f"{BACKEND_URL}/api/message", timeout=5)
        resp.raise_for_status()
        return jsonify(
            service="frontend",
            called=BACKEND_URL,
            backend_response=resp.json(),
        )
    except requests.RequestException as exc:
        return jsonify(service="frontend", error=str(exc)), 502


@app.route("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
