import pandas as pd

def _generate_schedule(userID):
    user_info = pd.read_csv("user_info.csv", index_col=0)
    
    res = {"version": "2.0",
           "template": {
               "outputs": [
                   {
                       "basicCard": {
                           "title": "Welcome, "+user_info.loc[userID, "NAME"]+". Your schedule is being generated. It can take up to 3 minutes",
                           "buttons": [
                               {
                                   "label" : "Continue",
                                   "action" : "block",
                                   "blockId" : "5ebfffcf1276c30001314792"
                               },
                               {
                                   "label" : "Quit",
                                   "action" : "block",
                                   "blockId" : "5ec20f34031ba40001167126"
                               } 
                           ]
                       }
                   }
               ]
           }}
    
    return res

def _continue_scheduling(userID)
    res = {"version" : "2.0",
           "template": { 
               "outputs": [
                   {
                       "simpleText": {
                           "text": "Thank you for your patience."
                       }
                   }
                ]              
            }}