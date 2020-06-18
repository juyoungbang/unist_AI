# Client Section



--------

# AI Planning Section

After clients' orders are finalized, order information file is generated,
like, unist_AI/solver/inputs/problem1.json.

This json file will be converted to pddl format file by script below.
```
base_dir = pathlib.Path().absolute()
save_dir = os.path.join(base_dir, 'solver', 'results')
import_dir = os.path.join(base_dir, 'solver', 'inputs')

with open(os.path.join(import_dir, f'problem{input_num}.json')) as fp:
    test_data = json.load(fp)['requests']
    
builder = ProblemFile(f"problem{input_num}", import_dir, import_dir, test_data)
builder.export()
```
converted pddl file examples are here too (unist_AI/solver/inputs/problem1.pddl)

And By using Fast Downward alorithm, AI solver is exeucted. 
We run it from python script with prepared shell script(run_fd.sh)

```
cmd = f'bash /workspace/d_avengers/solver/run_fd.sh /workspace/d_avengers/solver/inputs/problem{input_num}.pddl'
subprocess.call(shlex.split(cmd))
```

unist_AI/solver/run_fd.sh 
```
/workspace/d_avengers/downward_package/fast-downward.py /workspace/d_avengers/solver/domain.pddl $1 --heuristic "hff=cg()" --search "lazy_greedy([hff],preferred=[hff])"
mv sas_plan /workspace/d_avengers/solver/results/sas_plan
echo 'Successfully Planned.'
```

We can't use sas_plan file directly, it need to be transformed to our system's format.
By using script below, we can get unist_AI/solver/results/plan1.csv file.
```
plan_path = os.path.join(save_dir, 'sas_plan')
menu_path = os.path.join(base_dir, 'solver', 'builder', 'predefined', 'menu.json')
order_path = os.path.join(import_dir, f'problem{input_num}.json')
transform_plan(plan_path, menu_path, order_path, input_num)
```

System will send kakaotalk messages to driver with that csv result.



 

 
