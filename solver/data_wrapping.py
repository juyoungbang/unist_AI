import json
import math
import pandas as pd

from .run import run_all  

def orders_format(l_map, input_num):
    with open(f'/workspace/d_avengers/solver/inputs/problem{input_num}.json') as json_file:
        json_data = json.load(json_file)   
        
    order_list = []
    for key, val in json_data['requests'].items():
        menu_list = ''
        for order in val['orders']:
            menu_list += (order['menu'] + '*' + str(order['qty']) + ' ')

        loc_id= l_map[(l_map['IN_X'] == val['location'][0]) & (l_map['IN_Y'] == val['location'][1])].iloc[0, 2]
        loc_nm = l_map[(l_map['IN_X'] == val['location'][0]) & (l_map['IN_Y'] == val['location'][1])].iloc[0, 3]
        
        request = {"title": f"{loc_nm}",
                   "description": menu_list,
                   "link": {"web": f"https://map.kakao.com/link/map/{loc_id}"}}
        order_list.append(request)

    orders = [{
                  "listCard": {
                      "header": {
                          "title": "Order List"
                      },
                      "items": order_list
                  }
              }]
   
    return orders

def format_fplan(userID, input_num):
    run_all(input_num)

    user_info = pd.read_csv("/workspace/d_avengers/user_info.csv", index_col=0)
    l_map = pd.read_csv("/workspace/d_avengers/solver/location_mapping.csv")
    plan = pd.read_csv(f"/workspace/d_avengers/solver/results/plan{input_num}.csv")

    outputs = []
    outputs.extend(orders_format(l_map, input_num))

    items = []
    for i in range(5):
        msg = ''
        if plan.iloc[i, 3] == "pick-up":
            msg = f"Pick up {plan.iloc[i, 4]} order(s)."
        else:
            msg = f"Deliver order(s)."

        loc_id = l_map[(l_map['IN_X'] == plan.iloc[i, 0]) & (l_map['IN_Y'] == plan.iloc[i, 1])].iloc[0, 2]
        loc_nm = l_map[(l_map['IN_X'] == plan.iloc[i, 0]) & (l_map['IN_Y'] == plan.iloc[i, 1])].iloc[0, 3]

        action = {"title": f"{loc_nm}",
                  "description": msg,
                  "link": {"web": f"https://map.kakao.com/link/to/{loc_id}"}}
        items.append(action)

    listCard = {
                   "listCard": {
                       "header": {
                           "title": "Recommended Schedule(1)"
                       },
                       "items": items
                   }
               }
    outputs.append(listCard)

    items = []
    for i in range(5, 10):
        msg = ''
        if plan.iloc[i, 3] == "pick-up":
            msg = f"Pick up {plan.iloc[i, 4]} order(s)."
        else:
            msg = f"Deliver order(s)."
       
        loc_id = l_map[(l_map['IN_X'] == plan.iloc[i, 0]) & (l_map['IN_Y'] == plan.iloc[i, 1])].iloc[0, 2]
        loc_nm = l_map[(l_map['IN_X'] == plan.iloc[i, 0]) & (l_map['IN_Y'] == plan.iloc[i, 1])].iloc[0, 3]

        action = {"title": f"{loc_nm}",
                  "description": msg,
                  "link": {"web": f"https://map.kakao.com/link/to/{loc_id}"}}
        items.append(action)

    listCard = {
               "listCard": {
                   "header": {
                       "title": "Recommended Schedule(2)"
                   },
                   "items": items,
                   "buttons": [
                       {
                           "label": "Next",
                           "action": "block",
                           "blockId": "5eeafbef501c670001e5378a"
                       }
                   ]
               }
           }
    outputs.append(listCard)

    return outputs

def format_nplan(userID, input_num):
    user_info = pd.read_csv("/workspace/d_avengers/user_info.csv", index_col=0)
    l_map = pd.read_csv("/workspace/d_avengers/solver/location_mapping.csv")
    plan = pd.read_csv(f"/workspace/d_avengers/solver/results/plan{input_num}.csv", index_col=0)

    outputs = []

    for i in range(2):
        items = []
        for j in range(5):
            msg = ''
            if plan.iloc[5*i+j, 3] == "pick-up":
                msg = f"Pick up {plan.iloc[5*i+j, 4]} order(s)."
            else:
                msg = f"Deliver order(s)."

            loc_id = l_map[(l_map['IN_X'] == plan.iloc[5*i+j, 0]) & (l_map['IN_Y'] == plan.iloc[5*i+j, 1])].iloc[0, 2]
            loc_nm = l_map[(l_map['IN_X'] == plan.iloc[5*i+j, 0]) & (l_map['IN_Y'] == plan.iloc[5*i+j, 1])].iloc[0, 3]

            action = {"title": f"{loc_nm}",
                      "description": msg,
                      "link": {"web": f"https://map.kakao.com/link/to/{loc_id}"}}
            items.append(action)

        listCard = {
                       "listCard": {
                           "header": {
                               "title": f"Recommended Schedule({i+3})"
                           },
                           "items": items
                       }
                   }
        outputs.append(listCard)

    items = []
    i = 2
    for j in range(len(plan)-5*i):
        msg = ''
        if plan.iloc[5*i+j, 3] == "pick-up":
            msg = f"Pick up {plan.iloc[5*i+j, 4]} order(s)."
        else:
            msg = f"Deliver order(s)."

        loc_id = l_map[(l_map['IN_X'] == plan.iloc[5*i+j, 0]) & (l_map['IN_Y'] == plan.iloc[5*i+j, 1])].iloc[0, 2]
        loc_nm = l_map[(l_map['IN_X'] == plan.iloc[5*i+j, 0]) & (l_map['IN_Y'] == plan.iloc[5*i+j, 1])].iloc[0, 3]

        action = {"title": f"{loc_nm}",
                  "description": msg,
                  "link": {"web": f"https://map.kakao.com/link/to/{loc_id}"}}
        items.append(action)       

    listCard = {
               "listCard": {
                   "header": {
                       "title": f"Recommended Schedule({i+3})"
                   },
                   "items": items,
                   "buttons": [
                       {
                           "label": "Done",
                           "action": "block",
                           "blockId": "5edd45726fe05800015f26e5"
                       }
                   ]
               }
           }
    outputs.append(listCard)

    return outputs
