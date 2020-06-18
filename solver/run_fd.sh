/workspace/d_avengers/downward_package/fast-downward.py /workspace/d_avengers/solver/domain.pddl $1 --heuristic "hff=cg()" --search "lazy_greedy([hff],preferred=[hff])"
mv sas_plan /workspace/d_avengers/solver/results/sas_plan
echo 'Successfully Planned.'