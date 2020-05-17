from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/login/getID", methods=['POST'])
def getID():
    req = request.get_json()
    
    ans = {
        
    }
    
    return jsonify(ans)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)