from verification import _checkID, _no
from scheduling import _generate_schedule, _continue_scheduling
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/verification/checkID", methods=["POST"])
def checkID():
    req = request.get_json()
    userID = req["userRequest"]["user"]["properties"]["plusfriendUserKey"]
    res = _checkID(userID)

    return jsonify(res)


@app.route("/verification/no", methods=["POST"])
def no():
    req = request.get_json()
    userID = req["userRequest"]["user"]["properties"]["plusfriendUserKey"]
    res = _no(userID)

    return jsonify(res)


@app.route("/scheduling/generate_schedule", methods=["POST"])
def generate_schedule():
    req = request.get_json()
    userID = req["userRequest"]["user"]["properties"]["plusfriendUserKey"]
    res = _generate_schedule(userID)
    
    return jsonify(res)


@app.route("/scheduling/continue", methods=["POST"])
def continue_scheduling():
    req = request.get_json()
    userID = req["userRequest"]["user"]["properties"]["plusfriendUserKey"] 
    res = _continue_scheduling(userID)

    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)