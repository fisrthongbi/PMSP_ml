import pickle
def mean_f(x):
    result = sum(x)/len(x)
    return result

prob_name = 'XL'

"""with open('cp_scheduling_ortools_answer_{}30.pickle'.format(prob_name), mode='rb') as fr:
    cp_scheduling_ortools = pickle.load(fr)
    print('cp_ortools time : ', mean_f(cp_scheduling_ortools['time']))
    print('cp_ortools object_value : ', mean_f(cp_scheduling_ortools['object_value']))
    print(cp_scheduling_ortools['status'])

with open('cp_scheduling_answer_{}30.pickle'.format(prob_name), mode='rb') as fs:
    cp_scheduling_answer = pickle.load(fs)
    print('cp_scheduling_answer time : ', mean_f(cp_scheduling_answer['time']))
    print('cp_scheduling_answer object_value : ', mean_f(cp_scheduling_answer['object_value']))
    print(cp_scheduling_answer['status'])

with open('milp_scheduling_ortools_answer_{}30.pickle'.format(prob_name), mode='rb') as ff:
    milp_scheduling_ortools = pickle.load(ff)
    print('milp_scheduling_ortools time : ', mean_f(milp_scheduling_ortools['time']))
    print('milp_scheduling_ortools object_value : ', mean_f(milp_scheduling_ortools['object_value']))
    print(milp_scheduling_ortools['status'])

with open('milp_scheduling_answer_{}30.pickle'.format(prob_name), mode='rb') as fO:
    milp_scheduling = pickle.load(fO)
    print('milp_scheduling time : ', mean_f(milp_scheduling['time']))
    print('milp_scheduling object_value : ', mean_f(milp_scheduling['object_value']))
    print(milp_scheduling['status'])

with open('pulp_scheduling_answer_{}30.pickle'.format(prob_name), mode='rb') as fg:
    pulp_scheduling = pickle.load(fg)
    print('pulp_scheduling time: ', mean_f(pulp_scheduling['time']))
    print('pulp_scheduling object_value : ', mean_f(pulp_scheduling['object_value']))
    print(pulp_scheduling['status'])

with open('gurobi_milp_answer_{}30.pickle'.format(prob_name), mode='rb') as fP:
    gurobi_milp_answer_MM30 = pickle.load(fP)
    print('gurobi_milp_answer_MM30 time: ', mean_f(gurobi_milp_answer_MM30['time']))
    print('gurobi_milp_answer_MM30 object_value : ', mean_f(gurobi_milp_answer_MM30['object_value']))
    print(gurobi_milp_answer_MM30['status'])
"""
with open('milp_scheduling_ortools_answer_5minute_{}30.pickle'.format(prob_name), mode='rb') as ff:
    milp_scheduling_ortools = pickle.load(ff)
    print('milp_scheduling_ortools time : ', mean_f(milp_scheduling_ortools['time']))
    print('milp_scheduling_ortools object_value : ', mean_f(milp_scheduling_ortools['object_value']))
    print(milp_scheduling_ortools['status'])

with open('problem_{}8.pickle'.format(prob_name), mode='rb') as fP:
    user_loaded1 = pickle.load(fP)
with open('problem_{}9.pickle'.format(prob_name), mode='rb') as fP:
    user_loaded2 = pickle.load(fP)
print("1123213")
print("1123213")

# 7개 job 모두 optimal