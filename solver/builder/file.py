import pathlib
import os
import json

from .base import *
from pprint import pprint    

#http://csci431.artifice.cc/notes/pddl.html

class FileBuilder:
    def __init__(self, name, save_dir, import_dir):
        self.name = name
        self.save_dir = save_dir
        self.import_dir = import_dir

    def export(self):
        path = os.path.join(self.save_dir, f"{self.name}.pddl")

        with open(path, "w") as f:
            f.write(self.content)

    def show(self):
        print(self.content)

    def load_json(self, path):
        with open(path) as fp:
            data = json.load(fp)

        return data

    @property
    def content(self):
        raise NotImplementedError()

class DomainFile(FileBuilder):

    symbol = "domain"

    def __init__(self, name, save_dir, import_dir):
        super().__init__(name, save_dir, import_dir)

        self.predicate = None
        self.actions = []

        self.read_predicate()
        self.read_actions()
        
    def read_predicate(self):
        predicates = self.load_json(os.path.join(self.import_dir, 'predicates.json'))
        self.predicate = Predicate(predicates)

    def read_actions(self):
        actions = self.load_json(os.path.join(self.import_dir, 'actions.json'))

        for name, spec in actions.items():
            self.actions.append(Action(**spec))

    @property
    def content(self):
        """ predicates + actions
        (define (domain <domain name>)
            <PDDL code for predicates>
            <PDDL code for first action>
            [...]
            <PDDL code for last action>
        )
        """

        parts = [
            f"(define (domain {self.name})",
            self.predicate.pddl_component,
            ]
        parts.extend([x.pddl for x in self.actions])
        
        content = "\n\t".join(parts)
        content += "\n)"
        return content

class ProblemFile(FileBuilder):

    symbol = 'problem'

    def __init__(self, name, save_dir, import_dir, problem_data):
        super().__init__(name, save_dir, import_dir)

        self.domain_name = name
        self.name = name
        self.data = problem_data

        self.object = None
        self.state = None
        self.goal = None

        self.num_stores = 7
        self.store_list = [{'name': f's{i}'} for i in range(self.num_stores)]
        self.space_size = 7
        self.space_list = [{'name': f't{i}'} for i in range(self.space_size)]

        self.preprocess()
        self.process_distances()

        self.read_objects()
        self.read_state()
        self.read_goal()

    def read_menu(self):
         menu_path = os.path.join('/'.join(self.import_dir.split('/')[:-1]), 'builder', 'predefined', 'menu.json')
         menu = self.load_json(menu_path)

         self.menu = {}
         for content in menu:
             self.menu[content['menu']] = content['name']
             self.locations[content['name']] = content['location']

    def preprocess(self):
        data = self.data

        # objects 
        self.customer_list = []
        self.food_list = []

        # states
        self.obj_at = {}
        self.orders = {}
        self.locations = {}

        self.read_menu()

        food_cnt = 0
        for c, info in self.data.items():
            self.customer_list.append({'name': c})

            for order in info['orders']:
                for i in range(order['qty']) :
                    food_id = f'f{food_cnt}'
                    self.food_list.append({'name': food_id})
                    self.obj_at[food_id] = self.menu[order['menu']]
                    self.orders[food_id] = c

                    food_cnt += 1

            self.locations[c] = info['location']

    def process_distances(self):
        base = "(= (total-cost) 0)\n"
        dist = "\t(= (distance {} {}) {})\n"

        for loc1, coord1 in self.locations.items():
            for loc2, coord2 in self.locations.items():
                distance = int(((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2) ** 0.5)
                base += dist.format(loc1, loc2, distance)

        base += '\t)'
        self.distance_pddl = base

    def read_objects(self):
        """
        """
        objects = []
        objects.extend(self.store_list)
        objects.extend(self.customer_list)
        objects.extend(self.food_list)
        objects.extend(self.space_list)
        self.object = Object(objects)

    def read_state(self):
        """
        Customer / Store / Food

            - Set customers, stores, foods
            - Set food locations to store
        """

        states = []

        states.append({"name":"driver-at","args":[self.customer_list[0]['name']]})

        for customer in self.customer_list:
            states.append({"name":"customer","args":[customer['name']]})

        for store in self.store_list:
            states.append({"name":"store","args":[store['name']]})

        foods = [s['name'] for s in self.food_list]
        for food in foods:
            states.append({"name":"food", "args":[food]})
            states.append({"name":"order-done", "args":[food], "flag":"not"})

        for space in self.space_list:
            states.append({"name":"space","args":[space['name']]})

        for food, store in self.obj_at.items():
            states.append({"name":"obj-at","args":[food, store]})

        for food, customer in self.orders.items():
            states.append({"name":"order","args":[food, customer]})

        # total cost part

        self.state = State(states)

    def read_goal(self):
        """
        - Dirver
            - All capacity = 0
        - Customer
            - All order delivered   
        """
        goals = []
        foods = [s['name'] for s in self.food_list]

        for food in foods:
            goals.append({
                "name" : "order-done",
                "args" : [food],
                "option" : "and"
                })

        self.goal = Goal(goals)

    @property
    def content(self):
        """ objects + initial-states + goals
        (define (problem <problem name>)
            (:domain <domain name>)
            <PDDL code for objects>
            <PDDL code for initial state>
            <PDDL code for goal specification>
        )
        """

        parts = [
            f"(define (problem {self.name})",
            f"(:domain deliver)",
            self.object.pddl,
            self.state.pddl[:-1],
            self.distance_pddl,
            self.goal.pddl,
            "(:metric minimize (total-cost))"
            ]
        
        content = "\n\t".join(parts)
        content += "\n)"
        return content

class PddlBuilder(FileBuilder):
    def __init__(self, raw_data, save_dir, import_dir):
        req_id, problem_data = self.process_data(raw_data)

        super().__init__(req_id, save_dir, import_dir)
        self.domain = DomainFile(req_id, save_dir, import_dir)
        self.problem = ProblemFile(req_id, save_dir, import_dir, problem_data)

    def process_data(self, raw_data):
        return raw_data['req_id'], raw_data['requests']

    def export(self):
        self.domain.export()
        self.problem.export()

    @property
    def content(self):
        return "PddlFildBuilder"
    
if __name__ == "__main__":
    save_dir = pathlib.Path().absolute()
    import_dir = os.path.join(save_dir, 'predefined')

    with open(r'C:\Users\kjw940506\source\repos\unist_aip\aip\tests\inputs\example_build_input.json') as fp:
        test_data = json.load(fp)['requests']

    builder = ProblemFile('deliver', save_dir, import_dir, test_data)
    builder.export()
