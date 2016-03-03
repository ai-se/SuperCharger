
def standard_random(problem, n, center=False):
    dataset = []
    for run in range(n): dataset.append(problem.generateInput(center))
    return dataset


def sway(problem, n):

    dataset_size = 100 * n  # 50 times the population

    # center size population
    dataset = standard_random(problem, dataset_size, center=True)

    # Spectral Reduction
    dataset = spectral_cleanup(problem, dataset)

    import pdb
    pdb.set_trace()



'''#################################### Utilities ############################################'''


def find_opposing_population(problem, dataset):
    def find_opposite(point, center):
        assert(len(point) == len(center)), "Something is wrong"
        new_point = [0 for _ in xrange(len(point))]
        for i in xrange(len(new_point)):
            new_point[i] = center[i] + (center[i] - point[i])

        if problem.validate(new_point) is False: exit()
        return new_point

    def find_center(problem):
        center = [0 for _ in xrange(len(problem.decisions))]
        for i, decision in enumerate(problem.decisions):
            center[i] = decision.low + (decision.up - decision.low)/2
        return center

    CP = []
    center = find_center(problem)
    from random import random
    for data in dataset:
        opposite = find_opposite(data, center)
        assert(len(opposite) == len(data)), "Something is wrong"
        temp = [0 for _ in xrange(len(opposite))]
        for count, (i, j) in enumerate(zip(data, opposite)):
            if i <= center[count]: temp[count] = i + (j - i) * random()
            else: temp[count] = j + (i - j) * random()
        CP.append(temp)
    return CP


from InitialPopulationGeneration.Utilities.Fastmap.Slurp import slurp
from InitialPopulationGeneration.Utilities.Fastmap.The import The, rstop
from InitialPopulationGeneration.Utilities.Fastmap.Moo import Moo


def spectral_cleanup(problem, dataset):

    # Compile population into table form used by WHERE
    t = slurp([row + ["?" for _ in problem.objectives] for row in dataset], problem.buildHeader().split(","))

    # Initialize some parameters for WHERE
    The.allowDomination = True
    The.alpha = 1
    for i, row in enumerate(t.rows):
        row.evaluated = False

    # Run WHERE
    m = Moo(problem, t, len(t.rows), N=1).divide(minnie=rstop(t))

    print "Where done"
    # Organizing
    NDLeafs = m.nonPrunedLeaves()  # The surviving non-dominated leafs
    allLeafs = m.nonPrunedLeaves() + m.prunedLeaves()  # All of the leafs

    # After mutation: Check how many rows were actually evaluated
    numEval = 0
    for leaf in allLeafs:
        for row in leaf.table.rows:
            if row.evaluated:
                numEval += 1

    # After mutation; Convert back to JMOO Data Structures
    population = []
    for leaf in NDLeafs:
        for row in leaf.table.rows:
                population.append([x for x in row.cells[:len(problem.decisions)]])

    return population
