import module
import pickle
import numpy as np
import random
import copy


with open("problem1.pickle", mode='rb') as fr:
    test_instance = pickle.load(fr)
class chrosome:
    def __init__(self, prob : test_instance):
        self.prob = prob
        self.chrosome = []
        self.schedule_list = [[] for _ in range(self.prob.numMch)]
        self.total_time = 0
        for j in np.random.permutation(self.prob.job_list):
            self.chrosome.append([j, random.choice(self.prob.machine_list)])

    def __eq__(self, other):
        if not isinstance(other, chromosome):
            return NotImplemented
        return self.chromosome == other.chromosome

    # 뭔지 모르겠음
    def __hash__(self):
        return hash(str(self.schedule_list) + str(self.total_time))

    def sheduling(self):
        self.schedule_list = [[] for _ in range(self.prob.numMch)]
        for l in self.prob.machine_list:
            for k in range(self.prob.numJob):
                if self.chrosome[k][1] == l:
                    self.schedule_list[l.ID].append(self.chrosome[k][0])
        return self.schedule_list
    def add_totaltime(self):
        for i in self.prob.machine_list:
            start_time = 0
            befo = -1
            for j in self.schedule_list[i.ID]:
                if befo != -1:
                    start_time += self.prob.setup[i.ID][befo][j.ID]
                befo = j.ID
                start_time = start_time + self.prob.ptime[0][j.ID]
            self.total_time += start_time
        return self.total_time

    def mutation(self):  # population : generate_initial_population
        random_job = random.sample(range(0, self.prob.numJob), 2)
        # 작업 위치 변경
        ########## 작업을 변경 ##########
        ex1 = self.chrosome[random_job[0]][0]
        ex2 = self.chrosome[random_job[1]][0]
        self.chrosome[random_job[0]][0] = ex2
        self.chrosome[random_job[1]][0] = ex1
        self.chrosome = self.chrosome
        return self.chrosome

def crossover_operator(population):
    random_chrosmoe_num = random.sample(range(1, len(population)), 2)
    random_ch1 = population[random_chrosmoe_num[0]]
    random_ch2 = population[random_chrosmoe_num[1]]
    random_cut = random.sample(range(0, random_ch1.prob.numJob), 1)
    ex1 = copy.deepcopy(random_ch1)
    ex2 = copy.deepcopy(random_ch2)
    chrosome = ex1.chrosome[random_cut[0]:]
    for i in range(len(ex2.chrosome)):
        if not any(ex2.chrosome[i][0] in sublist for sublist in chrosome): #TODO 같은 job인데 ==에서는 다르다는고 나옴(해결)
            chrosome.append(ex2.chrosome[i])
    ex1.chrosome = chrosome
    return ex1

def tournament_selection(population, tournament_size):
    selected_population = []
    while len(selected_population) < len(population):
        # 토너먼트 크기를 전체 모집단 크기로 제한
        tournament_group_size = min(tournament_size, len(population))
        tournament_group = random.sample(population, tournament_group_size)

        # 토너먼트 그룹 중에서 가장 좋은 개체를 선택
        winner = min(tournament_group, key=lambda x: x.total_time)

        # 선택된 개체를 결과 리스트에 추가
        selected_population.append(winner)

    return selected_population
elite_ratio = 0.5
tournament_size = 5

if __name__ == '__main__':
    for r in range(1):  # 한실험당 10번 진행
        for k in range(10):  # generation
            population = []
            for o in range(100):
                with open("problem1.pickle", mode='rb') as fr:
                    test_instance = pickle.load(fr)
                for i in range(30):  # 반복되는 수만큼 유전자 생성
                    box = chromosome(test_instance)
                    box.schedule_list = box.sheduling()
                    box.total_time = box.add_totaltime()
                    population.append(box)
                    # population.append(generate_initial_population(test_instance))
                selected_population = tournament_selection(population, tournament_size)
                # 가장 좋은 개체를 엘리트 비율에 따라 선택하여 다음 세대로 유지
                elite_count = int(len(population) * elite_ratio)
                elite_individuals = sorted(population, key=lambda x: x.total_time)[:elite_count]
                selected_population.extend(elite_individuals)

                for i in range(0):  # 반복되는 수만큼 돌연변이 생성
                    random_chromosome = copy.deepcopy(population[random.sample(range(1, len(population)), 1)[0]])
                    random_chromosome.chromosome = random_chromosome.mutation()
                    random_chromosome.schedule_list = random_chromosome.sheduling()
                    random_chromosome.total_time = random_chromosome.add_totaltime()
                    population.append(random_chromosome)

                selected_population = tournament_selection(population, tournament_size)
                # 가장 좋은 개체를 엘리트 비율에 따라 선택하여 다음 세대로 유지
                elite_count = int(len(population) * elite_ratio)
                elite_individuals = sorted(population, key=lambda x: x.total_time)[:elite_count]
                selected_population.extend(elite_individuals)

                for i in range(0):  # 반복되는 수만큼 유전자 조합하여 생성
                    crossed_chromosome = crossover_operator(population)
                    crossed_chromosome.schedule_list = crossed_chromosome.sheduling()
                    crossed_chromosome.total_time = crossed_chromosome.add_totaltime()
                    population.append(crossed_chromosome)
                selected_population = tournament_selection(population, tournament_size)
                # 가장 좋은 개체를 엘리트 비율에 따라 선택하여 다음 세대로 유지
                elite_count = int(len(population) * elite_ratio)
                elite_individuals = sorted(population, key=lambda x: x.total_time)[:elite_count]
                selected_population.extend(elite_individuals)

        with open('GA_answer_111{}.pickle'.format(r + 1), mode='wb') as fw:
            pickle.dump(selected_population, fw)

