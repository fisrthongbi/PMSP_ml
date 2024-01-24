from module import *
import copy


def scheduling(_prob: Instance, rule: str) -> Schedule:
    '''
    This function is for finding a feasible solution for a given scheduling problem instance.
    :param prob: Problem Instance
    :param rule: Scheduling Rule (e.g. EDD, SPT, MST)
    :return: Schedule Result with Objective Function
    '''

    prob = copy.deepcopy(_prob)

    def update_priority(job_list, mch_list):
        for j in job_list:
            if j.complete is False:
                if rule == 'EDD':
                    j.priority = j.due
                elif rule == 'SPT':  # This is an example of SPT
                    # j.priority = sum([m.ptime[j.ID] for m in mch_list])
                    j.priority = min(mch_list, key=lambda m: m.available).ptime[j.ID]
                elif rule == 'MST':  # This is an example of MST (Minimum Setup Time)
                    j.priority = min(mch_list, key=lambda m: m.available).get_setup(j)
                else: # If there is no rule, randomly select
                    j.priority = random.uniform(0.0, 1.0)
        return sorted((job for job in job_list if job.complete is False), key=lambda j: j.priority)

    wait_jobs = update_priority(prob.job_list, prob.machine_list)

    while len(wait_jobs) != 0:
        machines = sorted((mch for mch in prob.machine_list), key=lambda m: m.available)
        machines[0].process(wait_jobs[0])
        wait_jobs = update_priority(prob.job_list, prob.machine_list)

    obj = get_obj(prob)
    result = Schedule(rule, prob, obj=obj)
    result.print_schedule()

    return result
