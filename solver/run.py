import pathlib
import os
import json
import subprocess
import shlex

from .builder.file import ProblemFile
from .builder.transform import transform_plan

def run_all(input_num):
    base_dir = pathlib.Path().absolute()
    save_dir = os.path.join(base_dir, 'solver', 'results')
    import_dir = os.path.join(base_dir, 'solver', 'inputs')

    with open(os.path.join(import_dir, f'problem{input_num}.json')) as fp:
        test_data = json.load(fp)['requests']

    builder = ProblemFile(f"problem{input_num}", import_dir, import_dir, test_data)
    builder.export()

    # Execute Fast Downward
    cmd = f'bash /workspace/d_avengers/solver/run_fd.sh /workspace/d_avengers/solver/inputs/problem{input_num}.pddl'
    subprocess.call(shlex.split(cmd))

    plan_path = os.path.join(save_dir, 'sas_plan')
    menu_path = os.path.join(base_dir, 'solver', 'builder', 'predefined', 'menu.json')
    order_path = os.path.join(import_dir, f'problem{input_num}.json')
    transform_plan(plan_path, menu_path, order_path, input_num)