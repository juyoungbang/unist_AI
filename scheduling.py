import pandas as pd
from solver.data_rapping import format_fplan, format_nplan

def _generate_schedule(userID):
    user_info = pd.read_csv("user_info.csv", index_col=0)

    res = {"version": "2.0",
           "template": {
               "outputs": [
                   {
                       "basicCard": {
                           "title": "Welcome, "+user_info.loc[userID, "NAME"]+"!",
                           "description": "Your scheduling can take up to 3 minutes. Continue?",
                           "buttons": [
                               {
                                   "label": "Continue",
                                   "action": "block",
                                   "blockId": "5ebfffcf1276c30001314792"
                               },
                               {
                                   "label": "Quit",
                                   "action": "block",
                                   "blockId": "5ec20f34031ba40001167126"
                               }
                           ]
                       }
                   }
               ]
           }}

    return res

def _continue_scheduling(userID):
    res = {"version": "2.0",
           "template": {
               "outputs": format_fplan(userID, 3)
           }}

    return res

def _next_schedule(userID):
    res = {"version": "2.0",
           "template": {
               "outputs": format_nplan(userID, 3)
           }}

    return res  