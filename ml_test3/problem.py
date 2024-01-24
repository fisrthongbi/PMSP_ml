import random
from module import *
import pickle
num=0
for i in range(30):
    num += 1
    a = 10
    problem = generate_prob(200 , 10)
    with open('problem_XL{}.pickle'.format(num), mode='wb') as fw:
        pickle.dump(problem, fw)

