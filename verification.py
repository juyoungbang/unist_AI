import pandas as pd


def _checkID(userID):
    user_info = pd.read_csv("user_info.csv", index_col=0)

    if userID in user_info.index:
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "basicCard": {
                               "title": user_info.loc[userID, "NAME"]+"("+user_info.loc[userID, "REGION"]+")",
                               "description": "Is this your profile?",
                               "thumbnail": {
                                   "imageUrl": "https://github.com/juyoungbang/unist_AI/blob/master/etc/"+user_info.loc[userID, "AFFILIATION"]+".png?raw=true"
                               },
                               "buttons": [
                                   {
                                       "action": "block",
                                       "label": "Yes",
                                       "blockId": "5ebfffaed30dd70001af2557"
                                   },
                                   {
                                       "action":  "block",
                                       "label": "No",
                                       "blockId": "5ec14e73d30dd70001af27b5"
                                   }
                               ]
                           }
                       }
                   ]
               }}

        return res
    else:
        res = {"version": "2.0",
               "template": {
                   "outputs": [
                       {
                           "simpleText": {
                               "text": "You are not a verified user."
                           }
                       }
                   ]
               }}

        return res


def _no(userID):
    user_info = pd.read_csv("user_info.csv", index_col=0)

    res = {"version": "2.0",
           "template": {
               "outputs": [
                   {
                       "basicCard": {
                           "title": "Contact your affiliation to resolve the problem.",
                           "buttons": [
                               {
                                   "action": "phone",
                                   "label": user_info.loc[userID, "DIRECTOR_NUM"],
                                   "phoneNumber": user_info.loc[userID, "DIRECTOR_NUM"]
                               }
                           ]
                       }
                   }
               ]
           }}

    return res    