import os
import pathlib


class Node:
    def __init__(self, name=None, args=None, option=None, **kwargs):
        self.name = name
        self.args = args
        self.option = option

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.name}_{self.args}_{self.option}"


class Task:
    def __init__(self, specs):
        self.instances = []
        
        if not isinstance(specs, list):
            specs = [specs]

        for spec in specs:
            self.instances.append(Node(**spec))

    @property
    def conetents(self):
        raise NotImplementedError()

    @property
    def pddl(self):
        return f"(:{self.symbol} {self.content})"

    @property
    def pddl_component(self):
        return f":{self.symbol} {self.content}"

    def parameterize(self, specs):
        if not isinstance(specs, list):
            specs = [specs]

        for spec in specs:
            spec['args'] = [f"?{x}" for x in spec['args']]

        return specs

class Object(Task):
    """Things in the world that interest us.
    """

    symbol = "objects"

    @property
    def content(self):
        return " ".join([x.name for x in self.instances])

class Predicate(Task):
    """Properties of objects that we are interested in; can be true or false   

    ROOM(x) – true iff x is a room
    at-ball(x, y) – true iff x is a ball, y is a room, and x is in y
    """

    symbol = "predicates"

    @property
    def content(self):
        # (ROOM ?x ?y)
        parts = []
        for instance in self.instances:
            name = instance.name
            args = " ".join([f"?{x}" for x in instance.args])
            parts.append(f"({name} {args})")

        return " ".join(parts)

class State(Task):
    """The state of the world that we start in
    ROOM(rooma) and ROOM(roomb) are true.
        -> (:init (ROOM rooma) (ROOM roomb))
    """

    symbol = "init"

    @property
    def content(self):
        # (ROOM ?x ?y)
        parts = []
        for instance in self.instances:
            name = instance.name
            args = " ".join(instance.args)

            if hasattr(instance, 'flag'):
                value = f"({instance.flag} ({name} {args}))"
            else:
                value = f"({name} {args})"
            parts.append(value)

        return " ".join(parts)

class Goal(Task):
    """Things that we want to be true.
    
    (:goal (and (at-ball ball1 roomb)
                (at-ball ball2 roomb)
                (at-ball ball3 roomb)
                (at-ball ball4 roomb)))

    """

    symbol = "goal"

    @property
    def content(self):
        # (ROOM ?x ?y)
        parts = {}
        for instance in self.instances:
            name = instance.name
            args = " ".join(instance.args)

            if hasattr(instance, 'flag'):
                value = f"({instance.flag} ({name} {args}))"
            else:
                value = f"({name} {args})"

            try:
                parts[instance.option] += " " + value
            except:
                parts[instance.option] = value

        content = ""
        for option, value in parts.items():
            content += f"({option} {value})"
            
        return content

class Parameter(Task):
    """Action component based on predicate
    """
    symbol = "parameters"

    def __init__(self, args):
        return super().__init__({"args":args})

    @property
    def content(self):
        parts = []
        for instance in self.instances:
            name = instance.name
            args = " ".join([f"?{x}" for x in instance.args])
            parts.append(f"({args})")

        return " ".join(parts)

class Precondition(Goal):
    """Action component based on predicate
    """
    symbol = "precondition"

class Effect(Goal):
    """Action component based on predicate
    """
    symbol = "effect"

class Action(Task):
    """Ways of changing the state of the world
    
    task: Movement operator
    Action/Operator:
        Description: The robot can move from x to y.
        Precondition: ROOM(x), ROOM(y) and at-robby(x) are true.
        Effect: at-robby(y) becomes true. at-robby(x) becomes false.
        Everything else doesn’t change.

    In PDDL:
        (:action move :parameters (?x ?y)
        :precondition (and (ROOM ?x) (ROOM ?y)
        (at-robby ?x))
        :effect (and (at-robby ?y)
        (not (at-robby ?x))))
    """
    
    symbol = 'action'

    def __init__(self, name, args, precondition, effect, **kwargs):
        self.name = name
        self.args = Parameter(args)

        precondition = self.parameterize(precondition)
        self.precondition = Precondition(precondition)

        effect = self.parameterize(effect)
        self.effect = Effect(effect)                    
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def content(self):
        parts = [
            self.name, 
            self.args.pddl_component, 
            self.precondition.pddl_component, 
            self.effect.pddl_component
            ]
        return " ".join(parts)
        
if __name__ == "__main__":
    action_kwargs = {
        "name": "move",
        "args": ["x", "y"],
        "precondition": [
            {"name": "ROOM", "args": ["x"], "option": "and"},
            {"name": "ROOM", "args": ["y"], "option": "and"},
        ],
        "effect": [
            {"name": "at-robby", "args": ["y"], "option": "and"},
            {"name": "at-robby", "args": ["x"], "option": "and", "flag":"not"},
        ]
    }

    task = Action(**action_kwargs)
    print(task.content)
    print(task.pddl)