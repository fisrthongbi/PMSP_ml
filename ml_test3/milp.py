from module import *
from docplex.mp.model import Model
from ortools.linear_solver import pywraplp
from heuristic import *
import pickle
import numpy as np
def milp_scheduling(prob:Instance):

    SJ = range(0, prob.numJob)
    SM = range(0, prob.numMch)
    s = prob.setup
    p = prob.ptime
    M = 0
    max_s = np.array(s).max()
    for i in SJ:
        M = M + max([row[i] for row in p])
        M = M + max_s
    M2 = M + max_s
    model = Model(name='PMSP')

    # 결정변수
    C_i = {i: model.continuous_var(lb=0, name='C_' + str(i)) for i in SJ}
    C_ik = {(i, k): model.continuous_var(lb=0, name='C_' + str(i) + '_' + str(k)) for i in SJ for k in SM}
    S_ik = {(i, k): model.continuous_var(lb=0, name='S_' + str(i) + '_' + str(k)) for i in SJ for k in SM}
    y_ik = {(i, k): model.binary_var(name='y_' + str(i) + '_' + str(k)) for i in SJ for k in SM}
    z_ijk = {(i, j, k): model.binary_var(name='z_' + str(i) + '_' + str(j) + '_' + str(k)) for i in SJ for j in SJ for k
             in SM if i < j}

    constraint_1 = {(i, k): model.add_constraint(
        ct=C_ik[i, k] + S_ik[i, k] <= M * y_ik[i, k],
        ctname="constraint_1_{0}_{1}".format(i, k)) for i in SJ for k in SM}

    constraint_2 = {(i, k): model.add_constraint(
        ct=C_ik[i, k] >= S_ik[i, k] + p[k][i] - M * (1 - y_ik[i, k]),
        ctname="constraint_2_{0}_{1}".format(i, k)) for i in SJ for k in SM}

    constraint_3 = {(i, j, k): model.add_constraint(
        ct=S_ik[i, k] >= C_ik[j, k] + s[k][j][i]*y_ik[j, k] - M2*z_ijk[i, j, k],
        ctname="constraint_3_{0}_{1}_{2}".format(i, j, k)) for k in SM for i in SJ for j in SJ if i < j}

    constraint_4 = {(i, j, k): model.add_constraint(
        ct=S_ik[j, k] >= C_ik[i, k] + s[k][i][j]*y_ik[i, k] - M2*(1 - z_ijk[i, j, k]),
        ctname="constraint_4_{0}_{1}_{2}".format(i, j, k)) for k in SM for i in SJ for j in SJ if i < j}

    constraint_5 = {(i): model.add_constraint(
        ct=model.sum(y_ik[i, k] for k in SM) == 1,
        ctname="constraint_5_{0}".format(i)) for i in SJ}

    constraint_6 = {(i): model.add_constraint(
        ct=model.sum(C_ik[i, k] for k in SM) <= C_i[i],
        ctname="constraint_6_{0}".format(i)) for i in SJ}

    # 목적함수
    model.minimize(model.sum(C_i[i] for i in SJ))
    model.set_time_limit(300)
    result = model.solve(log_output=True)
    print('Cplex Objective - '+ str(result.objective_value))

    prob = copy.deepcopy(prob) # To prevent changing the original copy
    for i in SJ:
        for j in SJ:
            if i < j:
                for k in SM:
                    if round(result.get_value(z_ijk[(i, j, k)])) > 0:
                        job_i = prob.findJob(i)
                        job_i.priority -= 1

    MA = {i: [] for i in SM}
    for i in SJ:
       for k in SM:
           if round(result.get_value(y_ik[i, k])) > 0:
               print('Job {0} on Machine {1} completed at {2}'.format(i, k, int(result.get_value(C_ik[i, k]))))
               job_i = prob.findJob(i)
               job_i.end = result.get_value(C_ik[i, k])
               MA[k].append(job_i)
    for k in SM:
        MA[k] = sorted((job for job in MA[k]), key=lambda m: m.end)
        machine = prob.findMch(k)
        for job in MA[k]:
            machine.process(job)

    obj = get_obj(prob)
    result = Schedule('MILP_CPLEX', prob, obj=obj)
    result.print_schedule()

    return result
    # if "FEASIBLE" in result.solve_status.name:
    #     return result
    # elif "OPTIMAL" in result.solve_status.name:
    #     return result
    # else:
    #     return result

    """print('Objective Value - '+ str(result.objective_value))
        for i in SJ:
            print("job {0} ends at {1}".format(i, result.get_value(C_i[i])))
            for k in SM:
                if result.get_value(y_ik[i, k]) > 0:
                    print("\t at machine {0} starts from {1} to {2} with p = {3}".format(k, result.get_value(S_ik[i, k]), result.get_value(C_ik[i, k]) , p[k][i]))
                    # milp_bars[k].append(match_job_bar(prob, )"""

    """#위의 결과를 스케줄에 할당하여 저장
    schedule_list = [[] for i in range(prob.numMch)]
    for i in SJ:
        for k in SM:
            if int(y_ik[i, k]) == 1 :
                schedule_list[k].append(i)
    return Schedule('milp', prob, schedule_list)"""


def milp_scheduling_ortools(prob:Instance):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    SJ = range(0, prob.numJob)
    SM = range(0, prob.numMch)
    s = prob.setup
    p = prob.ptime
    M = 0
    max_s = np.array(s).max()
    for i in SJ:
        M = M + max([row[i] for row in p])
        M = M + max_s
    M2 = M + max_s
    infinity = solver.infinity()

    C_i= {i: solver.NumVar(0, infinity, 'C_' + str(i)) for i in SJ}
    C_ik ={(i,k): solver.NumVar(0, infinity, 'C_' + str(i) + '_' + str(k)) for i in SJ for k in SM}
    S_ik ={(i,k): solver.NumVar(0, infinity, 'S_' + str(i) + '_' + str(k)) for i in SJ for k in SM}
    y_ik ={(i,k): solver.IntVar(0, 1, 'y_' + str(i) + '_' + str(k)) for i in SJ for k in SM}
    z_ijk ={(i,j,k) : solver.IntVar(0, 1, 'z_' + str(i) + '_' + str(j) + '_' + str(k)) for i in SJ for j in SJ for k in SM}

    # Add Constraints
    constraint_1 = {(i,k) : solver.Add(C_ik[i,k] + S_ik[i,k] <= M * y_ik[i,k]) for i in SJ for k in SM }
    constraint_2 = {(i,k) : solver.Add(C_ik[i,k] >= S_ik[i,k] + p[k][i] - M * (1 - y_ik[i,k])) for i in SJ for k in SM }
    constraint_3 = {(i,j,k) : solver.Add(S_ik[i,k] >= C_ik[j,k] + s[k][j][i] * y_ik[j,k] - M2 * z_ijk[i,j,k]) for k in SM for i in SJ for j in SJ if i < j}
    constraint_4 = {(i,j,k) : solver.Add(S_ik[j,k] >= C_ik[i,k] + s[k][i][j] * y_ik[i,k] - M2 * (1 - z_ijk[i,j,k])) for k in SM for i in SJ for j in SJ if i < j}
    constraint_5 = {(i) : solver.Add(solver.Sum(y_ik[i,k] for k in SM) == 1) for i in SJ}
    constraint_6 = {(i) : solver.Add(solver.Sum(C_ik[i,k] for k in SM) <= C_i[i]) for i in SJ}

    solver.Minimize(sum([C_i[i] for i in SJ]))
    solver.set_time_limit(300*1000)
    solver.EnableOutput()
    status = solver.Solve()



    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        return solver
    elif status == pywraplp.Solver.FEASIBLE:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        return solver
    else:
        print("답이 없습니다.")
        return solver