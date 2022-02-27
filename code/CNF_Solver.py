from CNF_Creator import *
import numpy as np
import math
import random, time
from operator import itemgetter

def fit_clause(assign, sent):
    '''
    Calculates number of clauses satisfied for a particular sentence in a population
    '''
    sat = 0
    for i in sent:
        for j in i:
            if (j > 0 and assign[abs(j) - 1] == 1) or (j < 0 and assign[abs(j) - 1] == 0):
                sat = sat + 1
                break
    return sat


def fitness(sent, pop):
    '''
    Calculates fitness percentage for a population using "fit_clause"
    '''
    return [(fit_clause(i, sent) / len(sent)) * 100.0 for i in pop]


def parent_pref(sent, pop):
    '''
    Calculates preference order for selecting parents using "fit_clause"
    Higher fitness = Higher probability to get selected as a parent
    '''
    popFit = []
    fitSum = 0
    for i in pop:
        fit = fit_clause(i,sent)
        popFit.append(fit**50)
    for i in popFit:
        fitSum += i
    percentage_fit = [i / fitSum for i in popFit]
    return percentage_fit


def gen_rand_assign():
    '''
    Generates a random assignment of 1's and 0's of size 50
    '''
    return np.random.randint(2, size=50)


def gen_pop(pop_sz):
    '''
    Generates a population of random assignments of size "pop_sz"
    '''
    pop = []
    for i in range(pop_sz):
        pop.append(gen_rand_assign())
    return pop


def reproduce(sentence, par1, par2):
    '''
    Crossover of 2 parents by randomly generating a crossover point
    '''
    cross = random.choice(range(len(par1) - 1))
    c1 = []
    c2 = []
    for i in range(cross):
        c1.append(par1[i])
        c2.append(par2[i])
    for i in range(cross, len(par1)):
        c1.append(par2[i])
        c2.append(par1[i])
    return c1,c2


def mutate(par):
    '''
    Mutates a single value in an assignment with an 95% probability
    '''
    if(np.random.randint(100) > 95):
        return par
    i = random.randint(0,len(par)-1)
    par[i] = par[i] ^ 1
    return par


def next_gen(sent, old):
    '''
    Creates a new generation by reproducing and mutating the old generation
    Chooses the next generation in the following way:
    - Combines old and new generation
    - uses the "parent_pref" to choose 50 of them randomly
    '''
    n = len(old)
    new_gen = []
    best_gen=[]
    for i in range(n):
        p1, p2 = random.choices(old, parent_pref(sent, old), k=2)
        off1, off2 = reproduce(sent, p1, p2)
        off1 = mutate(off1)
        off2 = mutate(off2)
        new_gen.append(off1)
        new_gen.append(off2)
    for i in range(len(old)):
        best_gen.append(old[i])
    for i in range(len(new_gen)):
        best_gen.append(new_gen[i])
    return random.choices(best_gen, weights=parent_pref(sent, best_gen), k=len(old))

def get_best_assign(sent, pop):
    '''
    Calculates best assignment corresponding to the best fitness value
    '''
    pop_fitness = fitness(sent, pop)
    max_fitness = max(pop_fitness)
    for i in range(len(pop_fitness)):
        if pop_fitness[i] == max_fitness:
            best_assign = pop[i]
            break
    return best_assign, max_fitness

def simulate(sentence):
    '''
    Simulates the Genetic Algorithm
    '''
    pop = gen_pop(20)
#     print(pop)
    best_pop = pop
    st = time.time()
    end = st + 45
    while time.time() <= end:
        max_fit = max(fitness(sentence, pop))
        new_pop = next_gen(sentence, pop)
        new_max_fit = max(fitness(sentence, new_pop))
        if new_max_fit > max(fitness(sentence, best_pop)):
            best_pop = new_pop
        best_assign, best_pop_fit = get_best_assign(sentence, best_pop)
        if best_pop_fit == 100:
            break
        pop = new_pop
    fintime = time.time() - st
    if (time.time() - st) > 45:
        fintime = 45.00
    return best_pop_fit, fintime, best_assign

# def plot_fitness(y, fin):
#     '''
#     Plots fitness vs m
#     '''
#     plt.plot(y, fin)
#     plt.xlabel("Number of Clauses")
#     plt.ylabel("Fitness")
#     plt.show()
    
# def plot_time(y, time):
#     '''
#     Plots time vs m
#     '''
#     plt.plot(y, time)
#     plt.xlabel("Number of Clauses")
#     plt.ylabel("Time taken")
#     plt.show()
    
def tf_assign(assign): 
    '''
    Converts 1's and 0's to corresponding +ve and -ve literal values for giving best asssignment
    '''
    tf = []
    for i in range(len(assign)):
        if assign[i]==1:
            tf.append(i+1)
        else:
            tf.append(-(i+1))
    return tf

def main():
    '''
    Runs the Genetic Algorithm for various various number of clauses in a sentence
    '''
    numb_iter = 1 
    cnfC = CNF_Creator(n=50)
    st=100
    end = st + (numb_iter-1)*20 + 1
    fin=[]
    totTime=[]
    for m in range(st,end,20):
        sentence = cnfC.CreateRandomSentence(m)
#         sentence = ReadCNFfromCSVfile()
        temp = []
        acc, time, best_assign = simulate(sentence)
        fin.append(acc)
        totTime.append(time)
#     plot_fitness(list(range(st,end,20)), fin)
#     plot_time(list(range(st,end,20)), totTime)
    print('\n\n')
    print('Roll No : 2018B4A70786G')
    print('Number of clauses in CSV file : ',len(sentence))
    print('Best model : ', tf_assign(best_assign))
    print('Fitness value of best model : ', fin[0], ' %')
    print('Time taken : ', totTime[0], ' seconds')
    print('\n\n')

if __name__ == '__main__':
    main()