"""
    This file is part of GALE,
    Copyright Joe Krall, 2014.

    GALE is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GALE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with GALE.  If not, see <http://www.gnu.org/licenses/>.
"""

from Fastmap.Slurp import *
from Fastmap.Moo import *
from jmoo_individual import *


def gale_8_WHERE(problem, population, configuration, values_to_be_passed):
    "The Core method behind GALE"

    from Utilities.where import where
    import numpy as np
    decisions = np.array([pop.decisionValues for pop in population])
    leaves = where(decisions)
    filled_leaves = []
    for leaf in leaves:
        temp_list = [jmoo_individual(problem, list(member), None) for member in leaf]
        filled_leaves.append(temp_list)

    return filled_leaves, 0


def gale_8_Mutate(problem, leaves, configuration):

    def mutate(candidate, SouthPole, NorthPole):
        mutant = [None for _ in xrange(len(candidate.decisionValues))]
        g = abs(SouthPole.x - NorthPole.x)
        for attr in range(0, len(problem.decisions)):
            # just some naming shortcuts
            me = candidate.decisionValues[attr]
            good = SouthPole.decisionValues[attr]
            bad = NorthPole.decisionValues[attr]
            dec = problem.decisions[attr]

            # Find direction to mutate (Want to mutate towards good pole)
            if me > good:  d = -1
            if me < good:  d = +1
            if me == good: d = 0
            mutant[attr] = min(dec.up, max(dec.low, (me + me * g * d) * 1.1))

        return jmoo_individual(problem, mutant, None)

    #################
    # Mutation Phase
    #################

    new_population = []
    # Keep track of evals
    number_of_evaluations = 0

    for leaf in leaves:
        initial_length = len(leaf)
        sorted_population = fastmap(problem, leaf)
        # print "sorted_population: ", len(sorted_population), len([g for g in sorted_population if g.fitness.valid])
        number_of_evaluations += 2

        good_ones = sorted_population[:initial_length/2]
        # print "good_ones: ", len(good_ones), len([g for g in good_ones if g.fitness.valid])
        mutants = [mutate(good_one, sorted_population[0], sorted_population[-1]) for good_one in good_ones]
        # print "mutants: ", len(mutants)

        excess = initial_length - (len(good_ones) + len(mutants))
        random_points = [jmoo_individual(problem, problem.generateInput(), None) for _ in xrange(excess)]
        # print "excess: ", excess

        new_population += good_ones
        new_population += mutants
        new_population += random_points
        # print "new_population: ", len(new_population)
        assert(initial_length == len(good_ones) + len(mutants) + len(random_points)), "Something is wrong"



    # print len(new_population), configuration["Universal"]["Population_Size"]
    assert(len(new_population) == configuration["Universal"]["Population_Size"]), "Something is wrong"
    return new_population, number_of_evaluations


def furthest(individual, population):
    from euclidean_distance import euclidean_distance
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


def fastmap(problem, true_population):
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

    for true_pop in true_population:
        if list_equality(true_pop.decisionValues, west_indi.decisionValues): true_pop.fitness.fitness = west_indi.fitness.fitness
        if list_equality(true_pop.decisionValues, east_indi.decisionValues): true_pop.fitness.fitness = east_indi.fitness.fitness


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
    temp_list =  sorted(true_population, key=lambda pop: pop.x)
    return temp_list




def gale_8_Regen(problem, unusedslot, mutants, configuration):
    
    return mutants, 0
