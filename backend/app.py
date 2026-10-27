from flask import Flask, jsonify
import socket

app = Flask(__name__)


@app.route("/api/message")
def message():
    return jsonify(
        service="backend",
        message="Hello from the BACKEND service!",
        pod=socket.gethostname(),
    )


@app.route("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
