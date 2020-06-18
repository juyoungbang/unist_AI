import re 
import os
import json

import pandas as pd

def load_json(path):
    with open(path) as fp:
        data = json.load(fp)

    return data

def load_locations(menu_path, order_path):
    location = {}

    menu = load_json(menu_path)
    for content in menu:
        location[content['name']] = content['location']

    customers = load_json(order_path)['requests']
    for name, content in customers.items():
        location[name] = content['location']

    return location

def convert_table(plan, location):
    table = pd.DataFrame([], columns=['x', 'y', 'name', 'action', 'qty'])

    for idx, action in enumerate(plan):
        s = re.sub(r"\(|\)", "", action).upper()
        terms = s.split(" ")

        #########################################
        # print the MATCH or DRAW actions here. #
        #########################################
        func = terms[0]
        args = terms[1:]

        if func in ['PICK-UP', 'DELIVER']:
            name = args[1].lower()
            x = location[name][0]
            y = location[name][1]
            action = func.lower()
            table.loc[idx, :] = [x, y, name, action, 1]
    
    return table

def transform_plan(plan_path, menu_path, order_path, input_num):
    plan = []
    location = load_locations(menu_path, order_path)
    with open(plan_path) as infile:
        for line in infile:
            s = line.strip()
            if s == '': continue
            plan.append(s)

    table = convert_table(plan, location)
    
    table.to_csv(f'/workspace/d_avengers/solver/results/plan{input_num}.csv')

if __name__ == "__main__":
    transform_plan()