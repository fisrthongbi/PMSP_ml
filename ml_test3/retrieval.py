from module import *
from typing import List
import copy
import pandas as pd
from cp import *

JS_FIRST = True  # Job Sequencing -> Machine Allocation
# Features for Job Sequencing -> Machine Allocation
# Number of Waiting Tardy Jobs, Earliest Start Time, Tightest Due Date, SumPTime, SumSTime, AvgDue, MaxDue, MinDue
FEATURES_JS_JM = ['Regret', 'NumWaitingJob',
                  'STime_A_Avg', 'STime_B_Avg', 'STime_A_VS_B_Avg', 'STime_A_VS_B_Avg_Diff',
                  'STime_A_Min', 'STime_B_Min', 'STime_A_VS_B_Min', 'STime_A_VS_B_Min_Diff',
                  'STime_A_Max', 'STime_B_Max', 'STime_A_VS_B_Max', 'STime_A_VS_B_Max_Diff',
                  'PTime_A_Avg', 'PTime_B_Avg', 'PTime_A_VS_B_Avg', 'PTime_A_VS_B_Avg_Diff',
                  'PTime_A_Min', 'PTime_B_Min', 'PTime_A_VS_B_Min', 'PTime_A_VS_B_Min_Diff',
                  'PTime_A_Max', 'PTime_B_Max', 'PTime_A_VS_B_Max', 'PTime_A_VS_B_Max_Diff',
                  'Due_A', 'Due_B', 'Due_A_VS_B', 'Due_A_VS_B_Diff'
                  ]
FEATURES_MA_JM = ['Regret', 'NumWaitingJob',
                  'STime_A', 'STime_B', 'STime_A_VS_B', 'STime_A_VS_B_Diff',
                  'PTime_A', 'PTime_B', 'PTime_A_VS_B', 'PTime_A_VS_B_Diff',
                  'CompTime_A', 'CompTime_B', 'CompTime_A_VS_B', 'CompTime_A_VS_B_Diff',
                  'Start_A', 'Start_B', 'Start_A_VS_B', 'Start_A_VS_B_Diff',
                  'Tardy_A', 'Tardy_B', 'Tardy_A_VS_B', 'Tardy_A_VS_B_Diff',
                  ]
DROP_FEATURES_JS_JM = [
                  'STime_A_Avg', 'STime_B_Avg',
                  'STime_A_Min', 'STime_B_Min',
                  'STime_A_Max', 'STime_B_Max',
                  'PTime_A_Avg', 'PTime_B_Avg',
                  'PTime_A_Min', 'PTime_B_Min',
                  'PTime_A_Max', 'PTime_B_Max',
                  'Due_A', 'Due_B'
                  ]
DROP_FEATURES_MA_JM = [
                  'STime_A', 'STime_B',
                  'PTime_A', 'PTime_B',
                  'CompTime_A', 'CompTime_B',
                  'Start_A', 'Start_B',
                  'Tardy_A', 'Tardy_B',
                  ]


# Features for Machine Allocation -> Job Sequencing
FEATURES_JS_MJ = ['Machine', 'Regret', 'NumWaitingJob', 'STime_A', 'STime_B', 'STime_A_VS_B', 'PTime_A', 'PTime_B',
                'PTime_A_VS_B']
FEATURES_MA_MJ = ['Regret', 'NumWaitingJob', 'STime_A', 'STime_B', 'STime_A_VS_B']


def add_row_js(df: pd.DataFrame, prob: Instance, Job_A: Job, Job_B: Job, regret: float, mch: Machine = None, no_label=False):
    row = dict()

    if JS_FIRST:
        row['NumWaitingJob'] = len([job for job in prob.job_list if job.complete is False])

        jobA_setups = Job_A.get_setups(prob.machine_list)
        jobB_setups = Job_B.get_setups(prob.machine_list)
        row['STime_A_Avg'] = jobA_setups['Avg']
        row['STime_B_Avg'] = jobB_setups['Avg']
        row['STime_A_VS_B_Avg'] = CompareTwoValues(jobA_setups['Avg'], jobB_setups['Avg'])
        row['STime_A_VS_B_Avg_Diff'] = jobA_setups['Avg'] - jobB_setups['Avg']

        row['STime_A_Min'] = jobA_setups['Min']
        row['STime_B_Min'] = jobB_setups['Min']
        row['STime_A_VS_B_Min'] = CompareTwoValues(jobA_setups['Min'], jobB_setups['Min'])
        row['STime_A_VS_B_Min_Diff'] = jobA_setups['Min'] - jobB_setups['Min']

        row['STime_A_Max'] = jobA_setups['Max']
        row['STime_B_Max'] = jobB_setups['Max']
        row['STime_A_VS_B_Max'] = CompareTwoValues(jobA_setups['Max'], jobB_setups['Max'])
        row['STime_A_VS_B_Max_Diff'] = jobA_setups['Max'] - jobB_setups['Max']

        jobA_ptimes = Job_A.get_ptimes(prob.machine_list)
        jobB_ptimes = Job_B.get_ptimes(prob.machine_list)
        row['PTime_A_Avg'] = jobA_ptimes['Avg']
        row['PTime_B_Avg'] = jobB_ptimes['Avg']
        row['PTime_A_VS_B_Avg'] = CompareTwoValues(jobA_ptimes['Avg'], jobB_ptimes['Avg'])
        row['PTime_A_VS_B_Avg_Diff'] = jobA_ptimes['Avg'] - jobB_ptimes['Avg']

        row['PTime_A_Min'] = jobA_ptimes['Min']
        row['PTime_B_Min'] = jobB_ptimes['Min']
        row['PTime_A_VS_B_Min'] = CompareTwoValues(jobA_ptimes['Min'], jobB_ptimes['Min'])
        row['PTime_A_VS_B_Min_Diff'] = jobA_ptimes['Min'] - jobB_ptimes['Min']

        row['PTime_A_Max'] = jobA_ptimes['Max']
        row['PTime_B_Max'] = jobB_ptimes['Max']
        row['PTime_A_VS_B_Max'] = CompareTwoValues(jobA_ptimes['Max'], jobB_ptimes['Max'])
        row['PTime_A_VS_B_Max_Diff'] = jobA_ptimes['Max'] - jobB_ptimes['Max']

        row['Due_A'] = Job_A.due
        row['Due_B'] = Job_B.due
        row['Due_A_VS_B'] = CompareTwoValues(Job_A.due, Job_B.due)
        row['Due_A_VS_B_Diff'] = Job_A.due - Job_B.due

        row['Regret'] = regret
    else:
        pass # To Be Implemented

    if no_label is True:
        for k in DROP_FEATURES_JS_JM:
            row.pop(k, None)
        values = list(row.values())
        return values

    df = pd.concat([df, pd.DataFrame.from_records([row])], ignore_index=True)
    return df


def add_row_ma(df: pd.DataFrame, prob: Instance, Mch_A: Machine, Mch_B: Machine, regret: float, chosen_job: Job = None, no_label=False):
    row = dict()

    if JS_FIRST:
        row['NumWaitingJob'] = len([job for job in prob.job_list if job.complete is False])

        row['STime_A'] = Mch_A.get_setup(chosen_job)
        row['STime_B'] = Mch_B.get_setup(chosen_job)
        row['STime_A_VS_B'] = CompareTwoValues(Mch_A.get_setup(chosen_job), Mch_B.get_setup(chosen_job))
        row['STime_A_VS_B_Diff'] = Mch_A.get_setup(chosen_job) - Mch_B.get_setup(chosen_job)

        row['PTime_A'] = Mch_A.get_ptime(chosen_job)
        row['PTime_B'] = Mch_B.get_ptime(chosen_job)
        row['PTime_A_VS_B'] = CompareTwoValues(Mch_A.get_ptime(chosen_job), Mch_B.get_ptime(chosen_job))
        row['PTime_A_VS_B_Diff'] = Mch_A.get_ptime(chosen_job) - Mch_B.get_ptime(chosen_job)

        row['Start_A'] = Mch_A.available
        row['Start_B'] = Mch_B.available
        row['Start_A_VS_B'] = CompareTwoValues(Mch_A.available, Mch_B.available)
        row['Start_A_VS_B_Diff'] = Mch_A.available - Mch_B.available

        comptime_A = Mch_A.available + Mch_A.get_setup(chosen_job) + Mch_A.get_ptime(chosen_job)
        comptime_B = Mch_B.available + Mch_B.get_setup(chosen_job) + Mch_B.get_ptime(chosen_job)
        row['CompTime_A'] = comptime_A
        row['CompTime_B'] = comptime_B
        row['CompTime_A_VS_B'] = CompareTwoValues(comptime_A, comptime_B)
        row['CompTime_A_VS_B_Diff'] = comptime_A - comptime_B

        Tardy_A = max(comptime_A - chosen_job.due, 0)
        Tardy_B = max(comptime_B - chosen_job.due, 0)
        row['Tardy_A'] = Tardy_A
        row['Tardy_B'] = Tardy_B
        row['Tardy_A_VS_B'] = CompareTwoValues(Tardy_A, Tardy_B)
        row['Tardy_A_VS_B_Diff'] = Tardy_A - Tardy_B

        row['Regret'] = regret
    else:
        pass # To Be Implemented

    if no_label is True:
        for k in DROP_FEATURES_MA_JM:
            row.pop(k, None)
        values = list(row.values())
        return values

    # df = df.append(row, ignore_index=True)
    df = pd.concat([df, pd.DataFrame.from_records([row])], ignore_index=True)
    return df


def export_files(df_js: pd.DataFrame, js_path: str, df_ma: pd.DataFrame, ma_path: str):
    path_js, file_js = os.path.split(js_path)
    path_ma, file_ma = os.path.split(ma_path)
    if path_js != path_ma:
        raise NameError('js and ma paths must be at the same location')
    if not os.path.exists(path_js):
        os.makedirs(path_js)
    if os.path.exists(js_path):
        df_js.to_csv(js_path, header=False, index=False, mode='a')
    else:
        df_js.to_csv(js_path, index=False, mode='w')
    if os.path.exists(ma_path):
        df_ma.to_csv(ma_path, header=False, index=False, mode='a')
    else:
        df_ma.to_csv(ma_path, index=False, mode='w')

    print('done')


def retrieve_decisions(_prob: Instance, _schedule: Schedule, js_path: str ='datasets/js.csv', ma_path: str ='datasets/ma.csv') -> pd.DataFrame:
    if JS_FIRST:
        df_js = pd.DataFrame(columns=FEATURES_JS_JM)
        df_ma = pd.DataFrame(columns=FEATURES_MA_JM)
    else:  # To be implemented
        df_js = pd.DataFrame(columns=FEATURES_JS_MJ)
        df_ma = pd.DataFrame(columns=FEATURES_MA_MJ)

    prob = copy.deepcopy(_prob)
    schedule = copy.deepcopy(_schedule.bars)
    schedule = sorted(schedule, key=lambda x: x.start, reverse=False)
    start_times = [bar.start for bar in schedule]
    rank = [start_times.index(s) for s in start_times]
    for idx, rank in enumerate(rank):
        job = prob.findJob(schedule[idx].job.ID)
        job.priority = rank
        job.assignedMch = schedule[idx].machine

    wait_jobs = prob.job_list

    while len(wait_jobs) != 0:
        # TODO Non-delay is not Optimal in this case - See Pinedo's Textbook
        # Job Sequencing First VS Machine Allocation First
        # Machine Regret can be checked by taking the maximum of all the regrets from waiting jobs
        # machines = sorted((mch for mch in prob.machine_list), key=lambda m: m.available)

        if JS_FIRST:
            jobs = sorted((job for job in wait_jobs), key=lambda j: j.priority)
            chosen_job = jobs[0]
            best_objs = []
            min_obj_chosen = float("inf")
            min_obj_schedule = None
            min_obj_mch = None
            for mch in prob.machine_list:
                sub_prob = prob.make_subprob(mch.ID, chosen_job.ID)
                sub_schedule_opt = cp_scheduling_subprob(sub_prob, time_limit=60)
                best_objs.append([chosen_job, mch, sub_prob, sub_schedule_opt])
                if sub_schedule_opt.objective < min_obj_chosen:
                    min_obj_chosen = sub_schedule_opt.objective
                    min_obj_schedule = sub_schedule_opt
                    min_obj_mch = mch
            for test in best_objs:
                mch = test[1]
                mch_obj = test[3].objective
                if mch.ID != min_obj_mch.ID:
                    regret = mch_obj - min_obj_chosen
                    if regret < 0:
                        return min_obj_schedule
                    df_ma = add_row_ma(df_ma, prob, min_obj_mch, mch, 0, chosen_job)
                    df_ma = add_row_ma(df_ma, prob, mch, min_obj_mch, regret, chosen_job)

            for job in wait_jobs:
                if job is not chosen_job:
                    df_js = add_row_js(df_js, prob, chosen_job, job, 0)
                    # Regret Calculation for all machines and take the minimum
                    other_objs = []
                    min_obj_other = float("inf")
                    min_obj_schedule = None
                    min_obj_mch = None
                    for mch in prob.machine_list:
                        sub_prob = prob.make_subprob(mch.ID, job.ID)
                        sub_schedule_opt = cp_scheduling_subprob(sub_prob, time_limit=60)
                        other_objs.append([job, mch, sub_prob, sub_schedule_opt])
                        if sub_schedule_opt.objective < min_obj_other:
                            min_obj_other = sub_schedule_opt.objective
                            min_obj_schedule = sub_schedule_opt
                            min_obj_mch = mch

                    for test in other_objs:
                        mch = test[1]
                        mch_obj = test[3].objective
                        if mch.ID != min_obj_mch.ID:
                            regret = mch_obj - min_obj_other
                            if regret < 0:
                                raise ValueError('regret must be positive')
                            df_ma = add_row_ma(df_ma, prob, min_obj_mch, mch, 0, job)
                            df_ma = add_row_ma(df_ma, prob, mch, min_obj_mch, regret, job)

                    regret = min_obj_other - min_obj_chosen
                    if regret < 0:
                        return min_obj_schedule
                    df_js = add_row_js(df_js, prob, job, chosen_job, regret)

            bar = [bar for bar in schedule if bar.job.ID == chosen_job.ID][0]
            chosen_mch = prob.findMch(bar.machine)
        else:
            pass

        chosen_mch.process(chosen_job)
        wait_jobs = sorted((job for job in prob.job_list if job.complete is False), key=lambda j: j.priority)

    export_files(df_js, js_path, df_ma, ma_path)

    return None

def retrieve_decisions_rh(_prob: Instance, js_path: str ='datasets/js.csv', ma_path: str ='datasets/ma.csv') -> pd.DataFrame:
    if JS_FIRST:
        df_js = pd.DataFrame(columns=FEATURES_JS_JM)
        df_ma = pd.DataFrame(columns=FEATURES_MA_JM)
    else:  # To be implemented
        df_js = pd.DataFrame(columns=FEATURES_JS_MJ)
        df_ma = pd.DataFrame(columns=FEATURES_MA_MJ)

    prob = copy.deepcopy(_prob)
    wait_jobs = prob.job_list

    while len(wait_jobs) != 0:
        # TODO Non-delay is not Optimal in this case - See Pinedo's Textbook
        # Job Sequencing First VS Machine Allocation First
        # Machine Regret can be checked by taking the maximum of all the regrets from waiting jobs
        # machines = sorted((mch for mch in prob.machine_list), key=lambda m: m.available)

        if JS_FIRST:
            perf = {}
            for job in wait_jobs:
                min_obj_value = float("inf")
                min_obj_schedule = None
                min_obj_mch = None
                mch_perf = {}
                for mch in prob.machine_list:
                    sub_prob = prob.make_subprob(mch.ID, job.ID)
                    sub_schedule_opt = cp_scheduling_subprob(sub_prob, time_limit=60)
                    mch_perf[mch.ID] = sub_schedule_opt.objective
                    if sub_schedule_opt.objective < min_obj_value:
                        min_obj_value = sub_schedule_opt.objective
                        min_obj_schedule = sub_schedule_opt
                        min_obj_mch = mch
                for mch in prob.machine_list:
                    if mch is not min_obj_mch:
                        df_ma = add_row_ma(df_ma, prob, min_obj_mch, mch, 0, job)
                        df_ma = add_row_ma(df_ma, prob, mch, min_obj_mch, mch_perf[mch.ID]-mch_perf[min_obj_mch.ID], job)
                perf[job.ID] = [min_obj_value, min_obj_schedule, min_obj_mch, mch_perf]
                job.priority = min_obj_value

            jobs = sorted((job for job in wait_jobs), key=lambda j: j.priority)

            chosen_job = jobs[0]

            for job in wait_jobs:
                if job is not chosen_job:
                    df_js = add_row_js(df_js, prob, chosen_job, job, 0)
                    df_js = add_row_js(df_js, prob, job, chosen_job, perf[job.ID][0]-perf[chosen_job.ID][0])

            chosen_mch = perf[chosen_job.ID][2]
        else:
            pass

        chosen_mch.process(chosen_job)
        wait_jobs = sorted((job for job in prob.job_list if job.complete is False), key=lambda j: j.priority)

    obj = get_obj(prob)
    result = Schedule('RH_CP', prob, obj=obj)

    export_files(df_js, js_path, df_ma, ma_path)

    return result