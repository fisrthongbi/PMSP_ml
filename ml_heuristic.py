from module import *
import copy
import pandas as pd
from chefboost import Chefboost as chef
import retrieval


JS_Model = None
MA_Model = None


def get_regret(row: List, model) -> float:
    return chef.predict(model, row)


def learn_model(js_path: str = 'datasets/js.csv', ma_path: str = 'datasets/ma.csv'):
    df_js = pd.read_csv(js_path, encoding_errors='ignore')
    df_ma = pd.read_csv(ma_path, encoding_errors='ignore')
    df_js = df_js.drop(columns=retrieval.DROP_FEATURES_JS_JM)
    df_ma = df_ma.drop(columns=retrieval.DROP_FEATURES_MA_JM)
    config = {'algorithm': 'Regression', 'max_depth': 5, 'enableParallelism': False}
    model_js = chef.fit(df_js, config, target_label='Regret')
    model_ma = chef.fit(df_ma, config, target_label='Regret')
    return model_js, model_ma


def learn_model_sep(js_path: str = 'datasets/js.csv', ma_path: str = 'datasets/ma.csv'):
    df_js = pd.read_csv(js_path, encoding_errors='ignore')
    df_ma = pd.read_csv(ma_path, encoding_errors='ignore')
    df_js = df_js.drop(columns=retrieval.DROP_FEATURES_JS_JM)
    df_ma = df_ma.drop(columns=retrieval.DROP_FEATURES_MA_JM)

    df_js_binary = df_js.copy()
    df_js_binary.loc[df_js_binary['Regret'] != 0, 'Regret'] = 'Yes'
    df_js_binary.loc[df_js_binary['Regret'] == 0, 'Regret'] = 'No'

    df_ma_binary = df_ma.copy()
    df_ma_binary.loc[df_ma_binary['Regret'] != 0, 'Regret'] = 'Yes'
    df_ma_binary.loc[df_ma_binary['Regret'] == 0, 'Regret'] = 'No'

    config = {'algorithm': 'C4.5', 'max_depth': 5, 'enableParallelism': False}
    model_js_binary = chef.fit(df_js_binary, config, target_label='Regret')
    model_ma_binary = chef.fit(df_ma_binary, config, target_label='Regret')

    df_js = df_js[df_js['Regret'] > 0]
    df_ma = df_ma[df_ma['Regret'] > 0]

    config = {'algorithm': 'Regression', 'max_depth': 5, 'enableParallelism': False}
    model_js = chef.fit(df_js, config, target_label='Regret')
    model_ma = chef.fit(df_ma, config, target_label='Regret')

    return model_js_binary, model_js, model_ma_binary, model_ma


def ml_scheduling(_prob: Instance, model_js, model_ma, ml_alg: str = 'None'):
    prob = copy.deepcopy(_prob)

    def prioritize_jobs(job_list: List[Job]):
        if ml_alg == 'DT':
            for JobA in job_list:
                for JobB in job_list:
                    if JobA is not JobB:
                        row = retrieval.add_row_js(prob, JobA, JobB, no_label=True)
                        regret = get_regret(model=model_js, row=row)
                        JobA.priority += regret

        else:  # If there is no rule, randomly select
            for job in job_list:
                job.priority = random.uniform(0.0, 1.0)
        return sorted((job for job in job_list if job.complete is False), key=lambda j: j.priority)

    def prioritize_mchs(mch_list: List[Machine], chosen_job: Job):
        if ml_alg == 'DT':
            for MchA in mch_list:
                for MchB in mch_list:
                    if MchA is not MchB:
                        row = retrieval.add_row_ma(prob, MchA, MchB, chosen_job, no_label=True)
                        regret = get_regret(model=model_ma, row=row)
                        MchA.priority += regret

        else:  # If there is no rule, randomly select
            for mch in mch_list:
                mch.priority = random.uniform(0.0, 1.0)
        return sorted((mch for mch in mch_list), key=lambda m: m.priority)

    wait_jobs = prioritize_jobs(prob.job_list)

    while len(wait_jobs) != 0:
        chosen_job = wait_jobs[0]
        sorted_mchs = prioritize_mchs(prob.machine_list, chosen_job)
        chosen_mch = sorted_mchs[0]
        chosen_mch.process(chosen_job)
        wait_jobs = prioritize_jobs(prob.job_list)

    obj = get_obj(prob)
    result = Schedule('ML Scheduling with {0}'.format(ml_alg), prob, obj=obj)
    result.print_schedule()

    return result


def ml_scheduling_sep(_prob: Instance, model_js_binary, model_js, model_ma_binary, model_ma, ml_alg: str = 'None'):
    prob = copy.deepcopy(_prob)

    def prioritize_jobs(job_list: List[Job]):
        if ml_alg == 'DT':
            for JobA in job_list:
                for JobB in job_list:
                    if JobA is not JobB:
                        row = retrieval.add_row_js(pd.DataFrame(), prob, JobA, JobB, 0, no_label=True)
                        diff = get_regret(model=model_js_binary, row=row)

                        regret = get_regret(model=model_js, row=row)
                        JobA.priority += regret

        else:  # If there is no rule, randomly select
            for job in job_list:
                job.priority = random.uniform(0.0, 1.0)
        return sorted((job for job in job_list if job.complete is False), key=lambda j: j.priority)

    def prioritize_mchs(mch_list: List[Machine], chosen_job: Job):
        if ml_alg == 'DT':
            for MchA in mch_list:
                for MchB in mch_list:
                    if MchA is not MchB:
                        row = retrieval.add_row_ma(prob, MchA, MchB, chosen_job, no_label=True)
                        regret = get_regret(model=model_ma, row=row)
                        MchA.priority += regret

        else:  # If there is no rule, randomly select
            for mch in mch_list:
                mch.priority = random.uniform(0.0, 1.0)
        return sorted((mch for mch in mch_list), key=lambda m: m.priority)

    wait_jobs = prioritize_jobs(prob.job_list)

    while len(wait_jobs) != 0:
        chosen_job = wait_jobs[0]
        sorted_mchs = prioritize_mchs(prob.machine_list, chosen_job)
        chosen_mch = sorted_mchs[0]
        chosen_mch.process(chosen_job)
        wait_jobs = prioritize_jobs(prob.job_list)

    obj = get_obj(prob)
    result = Schedule('ML Scheduling with {0}'.format(ml_alg), prob, obj=obj)
    result.print_schedule()

    return result


def get_BPs_Comb(bps: List[float], numSplits: int) -> List[tuple]:
    bounds = []
    size = len(bps)
    if size < (numSplits - 1):
        return None
    elif size == (numSplits - 1):
        return None
    else:
        bps.sort()
        for i in range(0, size - 1):
            bounds.append(((bps[i] + bps[i + 1]) / 2))

    if MIN_DIST_BPS == True:
        bound_dist = RANGE_TOLERANCE * (max(bounds) - min(bounds)) / numSplits
        comb_set = [x for x in combinations(bounds, numSplits - 1) if check_distance(x, bound_dist)]
        if len(comb_set) == 0:
            return None
        else:
            if SAMPLE_RATIO != -1:
                comb_set = random.choices(comb_set, k=getSampleSize(SAMPLE_RATIO, len(comb_set)))
                # comb_set = random.choices(comb_set, k=2)
    else:
        comb_set = list(combinations(bounds, numSplits - 1))
        if len(comb_set) == 0:
            return None
        else:
            if SAMPLE_RATIO != -1:
                comb_set = random.choices(comb_set, k=getSampleSize(SAMPLE_RATIO, len(comb_set)))
                # comb_set = random.choices(comb_set, k=2)
    return comb_set