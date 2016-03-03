# this file has experiment which wuold check whether fastmap can be used to supplement non dominated sort
from __future__ import division



def furthest(individual, population):
    from Techniques.euclidean_distance import euclidean_distance
    distances = sorted([[euclidean_distance(individual, pop), pop] for pop in population], key=lambda x: x[0], reverse=True)
    return distances[0][-1]


def projection(a, b, c):
    """
    Fastmap projection distance
    :param a: Distance from West
    :param b: Distance from East
    :param c: Distance between West and East
    :return: FastMap projection distance(float)
    """
    return (a**2 + c**2 - b**2) / (2*c+0.00001)


def new_fastmap(problem, true_population):
    """
    Fastmap function that projects all the points on the principal component
    :param problem: Instance of the problem
    :param population: Set of points in the cluster population
    :return:
    """

    def list_equality(lista, listb):
        for a, b in zip(lista, listb):
            if a != b: return False
        return True

    from random import choice
    from Techniques.euclidean_distance import euclidean_distance

    decision_population = [pop.decisionValues for pop in true_population]
    one = choice(decision_population)
    west = furthest(one, decision_population)
    east = furthest(west, decision_population)

    west_indi = jmoo_individual(problem,west, None)
    east_indi = jmoo_individual(problem,east, None)
    west_indi.evaluate()
    east_indi.evaluate()


    # Score the poles
    n = len(problem.decisions)
    weights = []
    for obj in problem.objectives:
        # w is negative when we are maximizing that objective
        if obj.lismore:
            weights.append(+1)
        else:
            weights.append(-1)
    weightedWest = [c * w for c, w in zip(west_indi.fitness.fitness, weights)]
    weightedEast = [c * w for c, w in zip(east_indi.fitness.fitness, weights)]
    westLoss = loss(weightedWest, weightedEast, mins=[obj.low for obj in problem.objectives],
                    maxs=[obj.up for obj in problem.objectives])
    eastLoss = loss(weightedEast, weightedWest, mins=[obj.low for obj in problem.objectives],
                    maxs=[obj.up for obj in problem.objectives])

    # Determine better Pole
    if eastLoss < westLoss:
        SouthPole, NorthPole = east_indi, west_indi
    else:
        SouthPole, NorthPole = west_indi, east_indi


    east = SouthPole.decisionValues
    west = NorthPole.decisionValues

    c = euclidean_distance(east, west)
    tpopulation = []
    for one in decision_population:
        a = euclidean_distance(one, west)
        b = euclidean_distance(one, east)
        tpopulation.append([one, projection(a, b, c)])

    for tpop in tpopulation:
        for true_pop in true_population:
            if list_equality(tpop[0], true_pop.decisionValues):
                true_pop.x = tpop[-1]

    for i, true_pop in enumerate(true_population):
        if list_equality(west, true_pop.decisionValues):
            true_pop.fitness = west_indi.fitness
        elif list_equality(east, true_pop.decisionValues):
            true_pop.fitness = east_indi.fitness


    temp_list = sorted(true_population, key=lambda pop: pop.x)
    ranklist = [t.id for t in temp_list]
    return true_population, ranklist, temp_list[0], temp_list[-1]


def add_id_to_population(x_population):
    for count, pop in enumerate(x_population):
        x_population[count].id = count
    return x_population


def do_fastmap_domination(problem, population, Configurations):
    add_scores = {}
    repeat = 20
    population = add_id_to_population(population)
    for _ in xrange(repeat):
        population, ranklist, east, west = new_fastmap(problem, population)
        for rank, rl in enumerate(ranklist):
            if str(rl) in add_scores.keys():
                add_scores[str(rl)] += rank
            else:
                add_scores[str(rl)] = rank

    from operator import itemgetter
    sorted_population_id = [int(i[0]) for i in sorted(add_scores.items(), key=itemgetter(1))][:Configurations["Universal"]["Population_Size"]]
    sorted_population = []
    for i, pop in enumerate(population):
        if pop.id in sorted_population_id:
            sorted_population.append(pop)

    return sorted_population, len([p for p in sorted_population if p.valid])



import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from jmoo_properties import *
from jmoo_core import *

problems =[
    dtlz1(9, 5),
    dtlz2(14, 5),
    dtlz3(14, 5),
    dtlz4(14, 5),
    dtlz5(14, 5),
    dtlz6(14, 5),
    dtlz1(7, 3),
    dtlz2(12, 3),
    dtlz3(12, 3),
    dtlz4(12, 3),
    dtlz5(12, 3),
    dtlz6(12, 3),
    dtlz1(12, 8),
    dtlz2(17, 8),
    dtlz3(17, 8),
    dtlz4(17, 8),
    dtlz5(17, 8),
    dtlz6(17, 8),
    dtlz1(14, 10),
    dtlz2(19, 10),
    dtlz3(19, 10),
    dtlz4(19, 10),
    dtlz5(19, 10),
    dtlz6(19, 10),
    dtlz1(19, 15),
    dtlz2(24, 15),
    dtlz3(24, 15),
    dtlz4(24, 15),
    dtlz5(24, 15),
    dtlz6(24, 15),
]

Configurations = {
    "Universal": {
        "Repeats" : 5,
        "Population_Size" : 100,
        "No_of_Generations" : 20
    },
    "NSGAIII": {
        "SBX_Probability": 1,
        "ETA_C_DEFAULT_" : 30,
        "ETA_M_DEFAULT_" : 20
    },
    "GALE": {
        "GAMMA" : 0.15,  #Constrained Mutation Parameter
        "EPSILON" : 1.00,  #Continuous Domination Parameter
        "LAMBDA" :  3,     #Number of lives for bstop
        "DELTA"  : 1       # Accelerator that increases mutation size
    },
    "DE": {
        "F" : 0.75, # extrapolate amount
        "CF" : 0.3, # prob of cross over
    },
    "MOEAD" : {
        "niche" : 20,  # Neighbourhood size
        "SBX_Probability": 1,
        "ETA_C_DEFAULT_" : 20,
        "ETA_M_DEFAULT_" : 20,
        "Theta" : 5
    },
    "STORM": {
        "STORM_EXPLOSION" : 5,
        "STORM_POLES" : 20,  # number of actual poles is 2 * ANYWHERE_POLES
        "F" : 0.75, # extrapolate amount
        "CF" : 0.3, # prob of cross over
        "STORM_SPLIT": 6,  # Break and split into pieces
        "GAMMA" : 0.15,
    }
}

def assign_ids(before, after):
    for a in after:
        for b in before:
            equal = True
            for bb, aa in zip(b.decisionValues, a.decisionValues):
                if bb != aa:
                    equal = False
                    break
            if equal is True: a.id = b.id
    return after


def compare_methods(problem):
    initialPopulation(problem, Configurations["Universal"]["Population_Size"] * 2, "unittesting")
    population = problem.loadInitialPopulation(Configurations["Universal"]["Population_Size"] * 2, "unittesting")
    population = add_id_to_population(population)
    approx, approx_eval = do_fastmap_domination(problem, population)

    # non dominated sorting
    from jmoo_algorithms import selNSGA2
    final_solutions, _ = selNSGA2(problem, [], population, Configurations)

    approx_id = [a.id for a in approx]
    final_id = [f.id for f in assign_ids(population, final_solutions)]

    count = 0
    for aid in approx_id:
        if aid in final_id: count += 1

    # print "Name: ",problem.name, " Match: ", round((count/len(final_id)) * 100, 2), "Approx Evals: ", approx_eval, "Total Evaluation: ", Configurations["Universal"]["Population_Size"] * 2
    return round((count/len(final_id)) * 100, 2)

if __name__ == "__main__":
    for problem in problems:
        print "Problem Name: ", problem.name,
        temp = []
        for _ in xrange(10):
            temp.append(compare_methods(problem))
        print "Average Accuracy : ", mean(temp)

