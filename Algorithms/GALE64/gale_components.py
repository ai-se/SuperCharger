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


def gale_64_WHERE(problem, population, configuration, values_to_be_passed):
    "The Core method behind GALE"

    # Compile population into table form used by WHERE
    t = slurp([[x for x in row.decisionValues] + ["?" for y in problem.objectives] for row in population],
              problem.buildHeader().split(","))

    # Initialize some parameters for WHERE
    The.allowDomination = True
    The.alpha = 1
    for i, row in enumerate(t.rows):
        row.evaluated = False

    # Run WHERE
    m = Moo(problem, t, len(t.rows), N=1).divide(minnie=rstop(t))

    # Organizing
    NDLeafs = m.nonPrunedLeaves()  # The surviving non-dominated leafs
    allLeafs = m.nonPrunedLeaves() + m.prunedLeaves()  # All of the leafs

    # After mutation: Check how many rows were actually evaluated
    numEval = 0
    for leaf in allLeafs:
        for row in leaf.table.rows:
            if row.evaluated:
                numEval += 1

    return NDLeafs, numEval


def polynomial_mutation(problem, individual, configuration):
    from numpy.random import random
    eta_m_ = configuration["NSGAIII"]["ETA_M_DEFAULT_"]
    distributionIndex_ = eta_m_
    output = jmoo_individual(problem, individual.decisionValues)

    probability = 1/len(problem.decisions)
    for var in xrange(len(problem.decisions)):
        if random() <= probability:
            y = individual.decisionValues[var]
            yU = problem.decisions[var].up
            yL = problem.decisions[var].low
            delta1 = (y - yL)/(yU - yL)
            delta2 = (yU - y)/(yU - yL)
            rnd = random()

            mut_pow = 1.0/(eta_m_ + 1.0)
            if rnd < 0.5:
                xy = 1.0 - delta1
                val = 2.0 * rnd + (1 - 2 * rnd) * (xy ** (distributionIndex_ + 1.0))
                deltaq = val ** mut_pow - 1
            else:
                xy = 1.0 - delta2
                val = 2.0 * (1.0-rnd) + 2.0 * (rnd-0.5) * (xy ** (distributionIndex_+1.0))
                deltaq = 1.0 - (val ** mut_pow)


            y +=  deltaq * (yU - yL)
            if y < yL: y = yL
            if y > yU: y = yU

            output.decisionValues[var] = y

    return output


def sbxcrossover(problem, parent1, parent2, configuration):

    EPS = 1.0e-14
    distribution_index = configuration["NSGAIII"]["ETA_C_DEFAULT_"]
    probability = configuration["NSGAIII"]["SBX_Probability"]
    from numpy.random import random
    offspring1 = jmoo_individual(problem, parent1.decisionValues)
    offspring2 = jmoo_individual(problem, parent2.decisionValues)

    number_of_variables = len(problem.decisions)
    if random() <= probability:
        for i in xrange(number_of_variables):
            valuex1 = offspring1.decisionValues[i]
            valuex2 = offspring2.decisionValues[i]
            if random() <= 0.5:
                if abs(valuex1 - valuex2) > EPS:
                    if valuex1 < valuex2:
                        y1 = valuex1
                        y2 = valuex2
                    else:
                        y1 = valuex2
                        y2 = valuex1

                    yL = problem.decisions[i].low
                    yU = problem.decisions[i].up
                    rand = random()
                    beta = 1.0 + (2.0 * (y1 - yL) / (y2 - y1))
                    alpha = 2.0 - beta ** (-1 * (distribution_index + 1.0))

                    if rand <= 1/alpha:
                        betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (distribution_index + 1.0))
                    else:
                        betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (distribution_index + 1.0))

                    c1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
                    beta = 1.0 + (2.0 * (yU - y2) / (y2 - y1))
                    alpha = 2.0 - beta ** -(distribution_index + 1.0)

                    if rand <= (1.0 / alpha):
                        betaq = (rand * alpha) ** (1.0 / (distribution_index + 1.0))
                    else:
                        betaq = ((1.0 / (2.0 - rand * alpha)) ** (1.0 / (distribution_index + 1.0)))

                    c2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1))

                    if c1 < yL: c1 = yL
                    if c2 < yL: c2 = yL
                    if c1 > yU: c1 = yU
                    if c2 > yU: c2 = yU

                    if random() <= 0.5:
                        offspring1.decisionValues[i] = c2
                        offspring2.decisionValues[i] = c1
                    else:
                        offspring1.decisionValues[i] = c1
                        offspring2.decisionValues[i] = c2
                else:
                    offspring1.decisionValues[i] = valuex1
                    offspring2.decisionValues[i] = valuex2
            else:
                offspring1.decisionValues[i] = valuex2
                offspring2.decisionValues[i] = valuex1

    return offspring1, offspring2


def variation(problem, individual_index, population, configuration):
    """ SBX regeneration Technique """

    from random import randint
    another_parent = individual_index
    while another_parent == individual_index: another_parent = randint(0, len(population)-1)

    from copy import deepcopy
    parent1 = deepcopy(population[individual_index])
    parent2 = deepcopy(population[another_parent])

    child1, _ = sbxcrossover(problem, parent1, parent2, configuration)
    mchild1 = polynomial_mutation(problem, child1, configuration)

    return mchild1

def gale_64_Mutate(problem, NDLeafs, configuration):
    #################
    # Mutation Phase
    #################
    # Keep track of evals
    numEval = 0

    population = []
    for leaf in NDLeafs:

        initial_size = len(leaf.table.rows)

        # print "Number of mutants: ", len(leaf.table.rows)
        # Pull out the Poles
        east = leaf.table.rows[0]
        west = leaf.table.rows[-1]

        # Evaluate those poles if needed
        if not east.evaluated:
            for o, objScore in enumerate(problem.evaluate(east.cells)):
                east.cells[-(len(problem.objectives) - o)] = objScore
            east.evaluated = True
            numEval += 1
        if not west.evaluated:
            for o, objScore in enumerate(problem.evaluate(west.cells)):
                west.cells[-(len(problem.objectives) - o)] = objScore
            west.evaluated = True
            numEval += 1

        # Score the poles
        n = len(problem.decisions)
        weights = []
        for obj in problem.objectives:
            # w is negative when we are maximizing that objective
            if obj.lismore:
                weights.append(+1)
            else:
                weights.append(-1)
        weightedWest = [c * w for c, w in zip(west.cells[n:], weights)]
        weightedEast = [c * w for c, w in zip(east.cells[n:], weights)]
        westLoss = loss(weightedWest, weightedEast, mins=[obj.low for obj in problem.objectives],
                        maxs=[obj.up for obj in problem.objectives])
        eastLoss = loss(weightedEast, weightedWest, mins=[obj.low for obj in problem.objectives],
                        maxs=[obj.up for obj in problem.objectives])

        # Determine better Pole
        if eastLoss < westLoss:
            to_be_mutated = leaf.table.rows[:int(len(leaf.table.rows)/2)]
        else:
            to_be_mutated = leaf.table.rows[:int(len(leaf.table.rows)/2)]

        to_be_mutated_jmoo = []
        for row in to_be_mutated:
            if row.evaluated:
                to_be_mutated_jmoo.append(jmoo_individual(problem, [x for x in row.cells[:len(problem.decisions)]],
                                                  [x for x in row.cells[len(problem.decisions):]]))
            else:
                to_be_mutated_jmoo.append(jmoo_individual(problem, [x for x in row.cells[:len(problem.decisions)]], None))

        for i in xrange(initial_size - len(to_be_mutated)):
            index = i%len(to_be_mutated_jmoo)
            mutant = variation(problem, index, to_be_mutated_jmoo, configuration)
            to_be_mutated_jmoo.append(mutant)

        members_evaluated = sum([1 for i in to_be_mutated_jmoo if i.valid])
        while members_evaluated <= 2:
            from random import randint
            index = randint(0, len(to_be_mutated_jmoo)-1)
            to_be_mutated_jmoo[index].evaluate()
            numEval += 1
            members_evaluated += 1
            print "> ", members_evaluated

        population += to_be_mutated_jmoo

    return population, numEval


def gale_64_Regen(problem, unusedslot, mutants, configuration):
    howMany = configuration["Universal"]["Population_Size"] - len(mutants)
    # Generate random individuals
    population = []
    for i in range(howMany):
        population.append(jmoo_individual(problem, problem.generateInput(), None))
    
    return mutants+population, 0
