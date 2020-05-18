import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/verification/checkID", methods=["POST"])
def checkID():
    req = request.get_json()
    userID = req["userRequest"]["user"]["properties"]["plusfriendUserKey"]
    print(userID)
    user_info = pd.read_csv("user_info.csv", index_col=0)
    if userID in user_info.index:
        res = { "version" : "2.0",
                "template" : { 
                    "outputs" : [
                        {
                            "simpleText" : {
                                "text" : "Are you " + user_info.loc[userID, "NAME"] + " in " + user_info.loc[userID, "REGION"] + "?" 
                            }
                        }
                    ],
                    "quickReplies" : [
                        {
                            "messageText" : "Yes",
                            "label" : "Yes",
                            "action" : "block",
                            "blockId" : "5ebfffaed30dd70001af2557"
                        },
                        {
                            "messageText" : "No",
                            "label" : "No",
                            "action" : "block",
                            "blockId" : "5ec14e73d30dd70001af27b5"
                        }                        
                    ]
                }
        }
        
        return jsonify(res)
    else:
        res = { "version" : "2.0",
                "template" : { 
                    "outputs" : [
                        {
                            "simpleText" : {
                                "text" : "You are not a verified user."
                            }
                        }
                    ]

                }
        }

        return jsonify(res)

@app.route("/scheduling/generate_schedule", methods=["POST"])
def generate_schedule():
    req = request.get_json()
    userID = req["userRequest"]["user"]["properties"]["plusfriendUserKey"]   
    user_info = pd.read_csv("user_info.csv", index_col=0)
    
    res = { "version" : "2.0",
            "template" : { 
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : "Welcome, " + user_info.loc[userID, "NAME"] + ". Your schedule is being generated. It can take up to 3 minutes."
                        }
                    }
                ],
                "quickReplies" : [
                    {
                        "messageText" : "Continue",
                        "label" : "Continue",
                        "action" : "block",
                        "blockId" : "5ebfffcf1276c30001314792"
                    },
                    {
                        "messageText" : "Quit",
                        "label" : "Quit",
                        "action" : "block",
                        "blockId" : "5ec20f34031ba40001167126"
                    }                        
                ]               
            }
    }
    
    return jsonify(res)

@app.route("/scheduling/continue", methods=["POST"])
def continue_():
    req = request.get_json()
    
    res = { "version" : "2.0",
            "template" : { 
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : "Thank you for your patience."
                        },
                        "simpleImage" : {
                            "imageUrl" : "example_image.png",
                            "altText" : "Schedule Overview"
                        }
                    }
                ],
                              
            }
    }
    
    return jsonify(ResourceWarning)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)