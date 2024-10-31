from flask import Flask, jsonify, request
from flask_sse import sse


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix="/stream")


@app.route("/")
def home():
    return jsonify({"message": "Hello from this API!"})


@app.route("/control", methods=['POST'])
def control_host():

    data = request.get_json()
    command = data["command"]

    if command == "shutdown":
        sse.publish({"command": "shutdown"}, type="command")
    elif command == "snip":
        sse.publish({"command": "snip"}, type="command")
    elif command == "webcam":
        sse.publish({"command": "webcam"}, type="command")
    else:
        sse.publish({"command": "no action"}, type="command")

    return jsonify({"message": "Yeah!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7701, debug=True)