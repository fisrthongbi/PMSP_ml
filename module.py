import pickle
import random
import matplotlib.pyplot as plt
from typing import List
import copy


OBJECTIVE_FUNCTION = 'T'


def CompareTwoValues(A, B) -> str:
    if A == B:
        return '='
    elif A > B:
        return '>'
    else:
        return '<'


class Job():

    def __init__(self, _id: int):
        self.ID = _id  # instance variable unique to each instance
        self.complete = False
        self.start = -1  # 작업의 시작 시간
        self.end = -1  # 작업이 끝나는 시간
        self.assignedMch = -1
        self.due = -1
        self.priority = 0

    def __repr__(self):
        return 'Job ' + str(self.ID)

    def __eq__(self, other):
        if isinstance(other, Job):
            if (other.ID == self.ID) and (other.due == self.due):
                return True
        return False

    def get_setups(self, mch_list):
        setup_times = [mch.get_setup(self) for mch in mch_list]
        result = {}
        result['Min'] = min(setup_times)
        result['Max'] = max(setup_times)
        result['Avg'] = sum(setup_times) / len(setup_times)
        return result

    def get_ptimes(self, mch_list):
        ptimes = [mch.get_ptime(self) for mch in mch_list]
        result = {}
        result['Min'] = min(ptimes)
        result['Max'] = max(ptimes)
        result['Avg'] = sum(ptimes) / len(ptimes)
        return result


class Machine:

    def __init__(self, _id: int):
        self.ID = _id  # instance variable unique to each instance
        self.available = 0  # 작업이 가능한 시점
        self.assigned = []  # machine에 할당된 job list
        self.setup = None
        self.ptime = None
        self.schedules = []
        self.priority = 0

    def __repr__(self):
        return 'Machine ' + str(self.ID)

    def get_setup(self, job: Job):
        if len(self.assigned) == 0:
            return 0
        else:
            return self.setup[self.assigned[-1].ID][job.ID]

    def get_ptime(self, job: Job):
        return self.ptime[job.ID]

    def process(self, job: Job):
        job.assignedMch = self
        ptime = self.ptime[job.ID]
        setup = self.get_setup(job)
        job.start = self.available + setup
        self.available += (ptime + setup)
        job.end = self.available
        job.complete = True
        self.assigned.append(job)
        self.schedules.append(Bar(job, setup))

    def get_min_comp(self, job_list: List[Job]):
        min_comp = float("inf")
        for job in job_list:
            exp_comp = self.available + self.get_setup(job) + self.ptime[job.ID]
            if exp_comp < min_comp:
                min_comp = exp_comp
        return min_comp


class Instance:
    type = 'Unrelated PMSP with SDST'

    def __init__(self, jobs: list, mchs: list, ptime, setups):
        self.numJob = len(jobs)
        self.numMch = len(mchs)
        self.job_list = jobs
        self.machine_list = mchs
        self.ptime = ptime  # 프로세스 타임
        self.setup = setups  # 셋업 타임

    def deepcopy(self):
        job_list = [copy.deepcopy(job) for job in self.job_list]
        mch_list = [copy.deepcopy(mch) for mch in self.machine_list]
        ptime = copy.deepcopy(self.ptime)
        setups = copy.deepcopy(self.setup)
        result = Instance(job_list, mch_list, ptime, setups)
        return result

    def make_subprob(self, mch_id: int, job_id: int):
        job_list = [copy.deepcopy(job) for job in self.job_list]
        mch_list = [copy.deepcopy(mch) for mch in self.machine_list]
        ptime = copy.deepcopy(self.ptime)
        setups = copy.deepcopy(self.setup)
        result = Instance(job_list, mch_list, ptime, setups)
        result.findMch(mch_id).process(result.findJob(job_id))
        return result

    def __repr__(self):
        return 'Instance with {0} jobs and {1} machines'.format(self.numJob, self.numMch)

    def getPTime(self, job: Job, machine: Machine):
        return self.ptime[machine.ID][job.ID]  # add time return code

    def getSetup(self, job_i: Job, job_j: Job, machine: Machine):
        return self.setup[machine.ID][job_i.ID][job_j.ID]

    def findJob(self, id: int) -> Job:
        try:
            result = [i for i in self.job_list if i.ID == id][0]
        except ValueError:
            print("No Matching Job in List")
        return result

    def findMch(self, id: int) -> Machine:
        try:
            result = [i for i in self.machine_list if i.ID == id][0]
        except ValueError:
            print("No Matching Machine in List")
        return result

    def saveFile(self, path: str):
        with open(path, mode='wb') as fw:
            pickle.dump(self, fw)

    def loadFile(self, path: str):
        with open(path, mode='rb') as fr:
            instance = pickle.load(fr)
            self.numJob = instance.numJob
            self.numMch = instance.numMch
            self.job_list = instance.job_list
            self.machine_list = instance.machine_list
            self.ptime = instance.ptime
            self.setup = instance.setup


class Schedule:
    def __init__(self, _alg: str, instance, obj: float):
        self.algorithm = _alg
        self.instance = instance
        self.objective = obj
        self.bars = []
        self.comp_time = 'None'
        self.status = 'None'
        for m in self.instance.machine_list:
            for bar in m.schedules:
                self.bars.append(bar)

    def __repr__(self):
        return 'Schedule obtained by {0} - Objective: {1} (Total Setup Times: {2})'.format(self.algorithm, self.objective, get_total_setups(self.instance))

    def print_schedule(self):
        for m in self.instance.machine_list:
            for bar in m.schedules:
                print(bar)



class Bar:
    def __init__(self, job, setup: int):
        self.seq = job.ID
        self.job = job
        self.machine = job.assignedMch.ID
        self.start = job.start
        self.end = job.end
        self.setup = setup

    def __repr__(self):
        return 'Job {0} at Machine {1} : Setup ({2} - {3}, {4}) Processing {5} - {6}'.format(self.job.ID, self.machine, self.start - self.setup, self.start, self.setup, self.start, self.end)


def generate_prob(numJob: int, numMch: int, tau: int=0.4, rho: int=0.8) -> Instance:

    job_list = []
    machine_list = []
    jobs = [*range(0, numJob)]
    machines = [*range(0, numMch)]

    # Generated from Kim et al. (2002) at Robotics and Computer Integrated Manufacturing
    # Above Study is based on the production data for 1 week
    # obtained from a compound semiconductor manufacturing company located in Iksan, Chonbuk, Korea
    job_list += [Job(i) for i in jobs]
    machine_list += [Machine(i) for i in machines]
    ptimes = [[random.randint(30, 60) for j in jobs] for m in machines]
    smallest_ptime = 60
    for m in machines:
        for j in jobs:
            if ptimes[m][j] < smallest_ptime:
                smallest_ptime = ptimes[m][j]
    for m in machines:
        machine_list[m].ptime = ptimes[m]
        machine_list[m].available = 0

    smallest_stime = 90
    setup_matrix = [*range(0, numMch)]
    for m in machines:
        for j in jobs:
            for j in jobs:
                setup_matrix[m] = [[random.randint(10, 90) for j in jobs] for j in jobs]
                for j1 in jobs:
                    for j2 in jobs:
                        if setup_matrix[m][j1][j2] < smallest_stime:
                            smallest_stime = setup_matrix[m][j1][j2]
        machine_list[m].setup = setup_matrix[m]

    P = (numJob*(smallest_stime + smallest_ptime))/numMch
    for j in jobs:
        lb = round(P*(1-tau-rho/2))
        ub = round(P*(1-tau+rho/2))
        job_list[j].due = random.randint(lb, ub)

    return Instance(job_list, machine_list, ptimes, setup_matrix)


def get_obj(prob: Instance, objective=OBJECTIVE_FUNCTION):
    result = 0
    if objective == 'C':
        for m in prob.machine_list:
            for job in m.assigned:
                result += job.end
    elif objective == 'Cmax':
        cmax = 0
        for m in prob.machine_list:
            for job in m.assigned:
                if cmax < job.end:
                    cmax = job.end
        result = cmax
    elif objective == 'T':
        for m in prob.machine_list:
            for job in m.assigned:
                result += max(job.end-job.due, 0)
    return result


def get_total_setups(prob: Instance):
    result = 0
    for m in prob.machine_list:
        for bar in m.schedules:
            result += bar.setup
    return result