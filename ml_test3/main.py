from pulp import pulp, LpStatusOptimal, LpStatus
from module import *
from milp import *
from cp import *
import heuristic
import random
import time
import multiprocessing
import pickle
import pandas as pd
from gurobi import *
from pp import pulp_scheduling
import typing
from retrieval import *
from ml_heuristic import *
from statistics import mean
import csv

if __name__ == '__main__':
    record = []
    model_js_binary, model_js, model_ma_binary, model_ma = learn_model_sep()
    for i in range(30):
        numJob = random.randint(10, 20)

        test_instance = generate_prob(numJob=numJob, numMch=3, tau=0.2)
        # test_instance.saveFile('datasets/train/pmsp_sdst_{0}.prob'.format(i+1))
        test_instance.loadFile('datasets/train/pmsp_sdst_{0}.prob'.format(i+1))
        schedule_ml = ml_scheduling_sep(test_instance, model_js_binary, model_js, model_ma_binary, model_ma, 'DT')

        schedule_rh = retrieve_decisions_rh(test_instance)
        # new_instance = generate_prob(numJob=5, numMch=3, tau=0.2)
        # new_instance.loadFile('datasets/train/pmsp_sdst_{0}.prob'.format(i+1))

        # schedule = heuristic.scheduling(test_instance, 'MST')
        # schedule = milp_scheduling(test_instance)
        schedule_mst = scheduling(test_instance, 'MST')
        schedule_cp = cp_scheduling(test_instance, time_limit=3600, init_sol=schedule_mst)
        schedule_spt = scheduling(test_instance, 'SPT')
        schedule_rnd = scheduling(test_instance, 'RND')

        # record.append([schedule_cp.objective, schedule_spt.objective, schedule_mst.objective, schedule_rnd.objective, schedule_ml.objective])
        record.append([schedule_rh.objective, schedule_cp.objective, schedule_spt.objective, schedule_mst.objective, schedule_rnd.objective])
        # result = schedule_cp
        # cp_initial = result.objective
        # imp_cnt = 0
        # while result is not None:
        #     temp_schedule = retrieve_decisions(test_instance, result)
        #     if temp_schedule is None:
        #         with open('datasets/train/pmsp_sdst_{0}.cp'.format(i+1), mode='wb') as fw:
        #             pickle.dump(result, fw)
        #         print('Done')
        #     else:
        #         imp_cnt += 1
        #         result = temp_schedule
        #         if imp_cnt == 3:
        #             imp_cnt = 0
        #             result = cp_scheduling(test_instance, time_limit=600, init_sol=result)
        #             print('Check - Reinitiate the warm-start process with result')

    print(*map(mean, zip(*record)))
    with open('out.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(record)
    print('EOP')

    # pd.cut(df["Yourcolumns"],
    #        bins=[0, 2.5, 3, 3.25, 3.5, 3.75, 4],
    #        labels=["Very bad", "Bad", "Average", "good", "Very good", "Excellent"])
    # this_bps = np.unique(data[:, attr.id]).tolist()

    #schedule.print_schedule()
    #draw_gantt_chart(schedule, test_instance)

    # schedule = milp_scheduling(test_instance)
    # schedule.print_schedule()
    #draw_gantt_chart(schedule, test_instance)

    # schedule = cp_scheduling(test_instance)
    # schedule = milp_scheduling_ortools(test_instance)
    # schedule = cp_scheduling_ortools(test_instance)
