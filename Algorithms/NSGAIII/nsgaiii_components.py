from __future__ import division
from os.path import realpath, abspath, split, join
from inspect import currentframe, getfile
from sys import path


cmd_subfolder = realpath(abspath(join(split(getfile(currentframe()))[0], "..")))
if cmd_subfolder not in path: path.insert(0, cmd_subfolder)
from DEAP.tools.emo import sortNondominated


cmd_subfolder = realpath(abspath(join(split(getfile(currentframe()))[0], "../..")))
if cmd_subfolder not in path: path.insert(0, cmd_subfolder)
from jmoo_individual import *
# from jmoo_properties import *
from jmoo_algorithms import *
from random import random


# ---------------------- Helper --------------------------------

division_dict = {"3": [12,0],
                 "5": [6,0],
                 "8": [3,2],
                 "10": [3, 2],
                 "15": [2, 1]}

class Node(object):
    def __init__(self, data=-1, level=0, parent=None):
        self.data = data
        self.level = level
        self.children = []
        self.parent = parent

    def add_child(self, obj):
        self.children.append(obj)


def tree(node, n, p, level=0):
    if level == 0:
        from numpy import arange
        for i in [j for j in arange(0, 1 + 10e-10, 1 / p)]:
            node.add_child(Node(i, level + 1))
        for child in node.children:
            tree(child, n, p, level + 1)
    elif level < (n - 1):
        other_beta = 0

        # Traversing up the tree to get other values of beta
        temp = node
        while temp is not None:
            other_beta += temp.data
            temp = temp.parent

        k = (1 - other_beta) / (1 / p)
        from numpy import arange
        for i in [j for j in arange(0, k * (1 / p) + 10e-10, (1 / p))]:
            node.add_child(Node(i, level + 1, node))
        for child in node.children:
            tree(child, n, p, level + 1)
    elif level == (n - 1):
        other_beta = 0
        # Traversing up the tree to get other values of beta
        temp = node
        while temp is not None:
            other_beta += temp.data
            temp = temp.parent
        node.add_child(Node(1 - other_beta, level + 1, node))

    else:
        return


class reference_point:
    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = coordinates

    def __str__(self):
        s = "id: " + str(self.id) + "\n"
        s += "coordinates: " + str(self.coordinates) + "\n"
        return s


def get_ref_points(root):
    ref_points = []
    assert (root.data == -1 and root.level == 0), "Supplied node is not root"
    visited, stack = set(), [root]
    count = 0
    while len(stack) != 0:
        vertex = stack.pop()
        if vertex not in visited:
            if len(vertex.children) == 0:
                temp = vertex
                points = []
                while temp is not None:
                    points = [temp.data] + points
                    temp = temp.parent
                ref_points.append(reference_point(count, points))
                count += 1
            stack.extend(vertex.children)
            visited.add(vertex)
    return ref_points


from math import factorial


def comb(n, r):
    return factorial(n) / factorial(r) / factorial(n - r)


def setDivs(number_of_objectives):
    """reference points have two level when number of objectives > 5 (to keep number of reference points under check"""
    if number_of_objectives == 3:
        number_of_reference_points = [12, 0]
    elif number_of_objectives == 5:
        number_of_reference_points = [6, 0]
    elif number_of_objectives == 8 or number_of_objectives == 10:
        number_of_reference_points = [3, 2]
    elif number_of_objectives == 15:
        number_of_reference_points = [2, 1]
    else:
        print "This case is not handled. Number of objectives: ", number_of_objectives
        exit()

    return number_of_reference_points


def generate_weight_vector(division, number_of_objectives):
    root = Node(-1)
    tree(root, number_of_objectives, division)
    return get_ref_points(root)


def two_level_weight_vector_generator(divisions, number_of_objectives):
    division1 = divisions[0]
    division2 = divisions[1]

    N1 = 0
    N2 = 0

    if division1 != 0: N1 = comb(number_of_objectives + division1 - 1, division1)
    if division2 != 0: N2 = comb(number_of_objectives + division2 - 1, division2)

    first_layer = []
    second_layer = []
    if N1 != 0:  first_layer = generate_weight_vector(division1, number_of_objectives)
    if N2 != 0:
        second_layer = generate_weight_vector(division2, number_of_objectives)
        mid = 1 / number_of_objectives
        for tsl_objectives in second_layer:
            tsl_objectives.id += int(N1)
            tsl_objectives.coordinates = [(t + mid) / 2 for t in tsl_objectives.coordinates]


    for l in first_layer + second_layer:
        l.coordinates = [ll.item() for ll in l.coordinates]
        for ll in l.coordinates:
            assert(type(ll) != numpy.float64), "Seomthing is wrong"
    return first_layer + second_layer



def get_betaq(rand, alpha, eta=30):
    betaq = 0.0
    if rand <= (1.0 / alpha):
        betaq = (rand * alpha) ** (1.0 / (eta + 1.0))
    else:
        betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1.0))
    return betaq

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
    mchild1.evaluate()  #checked| correct

    assert(mchild1.valid is True), "Something is wrong| Check if the evaluation is complete"
    return mchild1


def compute_ideal_points(problem, population):
    checking_ideal_point = []
    for obj_index in xrange(len(problem.objectives)):
        checking_ideal_point.append(min([pop.fitness.fitness[obj_index] for pop in population]))
    return checking_ideal_point


def compute_max_points(problem, population):
    max_points = [-1e32 for _ in xrange(len(problem.objectives))]
    for i in xrange(len(problem.objectives)):
        for individual in population:
            if individual.fitness.fitness[i] > max_points[i]:
                max_points[i] = individual.fitness.fitness[i]
    return max_points


def asf_function(individual, index, ideal_point):
    max_value = -1e32
    epsilon = 1e-6
    for i, obj in enumerate(individual.fitness.fitness):
        temp_value = abs(obj - ideal_point[i])
        if index != i: temp_value /= epsilon
        if temp_value > max_value: max_value = temp_value
    return max_value

def compute_extreme_points(problem, population, ideal_point):
    extreme_points = [[0 for _ in problem.objectives] for _ in problem.objectives]
    for j in xrange(len(problem.objectives)):
        index = -1
        min_value = 1e32

        for i in xrange(len(population)):
            asfValue = asf_function(population[i], j, ideal_point)
            if asfValue < min_value:
                min_value = asfValue
                index = i

        for k in xrange(len(problem.objectives)):
            extreme_points[j][k] = population[index].fitness.fitness[k]

    assert(len(extreme_points) == len(problem.objectives)), "Number of extreme points should be equal to number of objectives"
    return extreme_points


def compute_intercept_points(problem, extreme_points, ideal_point, max_point):
    import numpy
    assert(len(extreme_points) == len(problem.objectives)), "Length of extreme points should be equal to the number of objectives of the problem"
    assert(len(extreme_points[0]) == len(ideal_point)), "Length of extreme points and ideal points should be the same"
    temp_L = []
    for extreme_point in extreme_points:
        temp = []
        for i, j in zip(extreme_point, ideal_point): temp.append(i-j)
        temp_L.append(temp)

    EX = numpy.array(temp_L)
    intercepts = [-1 for _ in problem.objectives]

    if numpy.linalg.matrix_rank(EX) == len(EX):
        UM = numpy.matrix([[1] for _ in problem.objectives])
        AL0 = numpy.linalg.inv(EX)
        AL = AL0.dot(UM)
        AL = AL.tolist()
        outer_j = 0
        for j in xrange(len(problem.objectives)):
            outer_j = j
            try:
                aj = 1/AL[j][0] + ideal_point[j]
            except ZeroDivisionError:
                break
            if aj > ideal_point[j]:
                intercepts[j] = aj
            else:
                break
        if outer_j != len(problem.objectives)-1:
            for k, max_value in enumerate(max_point):
                intercepts[k] = max_value # zmax


    else:
        for k,max_value in enumerate(max_point):
            intercepts[k] = max_value # zmax

    return intercepts



def normalization(problem, population, intercept_point, ideal_point):
    for individual in population:
        temp_normalized = []
        for count, obj in enumerate(individual.fitness.fitness):
            temp_normalized.append((obj - ideal_point[count])/(intercept_point[count] - ideal_point[count] + 0.0000001))
        individual.normalized = temp_normalized

    return population


def convert_to_jmoo(problem, pareto_fronts):
    tpopulation = []
    for front_no, front in enumerate(pareto_fronts[:-1]):
        for i, dIndividual in enumerate(front):
            cells = []
            for j in xrange(len(dIndividual)):
                cells.append(dIndividual[j])
            tpopulation.append(jmoo_individual(problem, cells, list(dIndividual.fitness.values)))
    for pop in tpopulation: pop.front_no = 0  # all the front except the last front

    lpopulation = []
    for front_no, front in enumerate(pareto_fronts[-1:]):
        for i, dIndividual in enumerate(front):
            cells = []
            for j in xrange(len(dIndividual)):
                cells.append(dIndividual[j])
            lpopulation.append(jmoo_individual(problem, cells, list(dIndividual.fitness.values)))
    for pop in lpopulation: pop.front_no = -1  # last front

    from itertools import chain
    assert(len(list(chain(*pareto_fronts))) <= len(lpopulation) + len(tpopulation)), "Non Dominated Sorting is wrong!"
    return lpopulation + tpopulation

def perpendicular_distance(ref, sol):
    assert(len(ref) == len(sol)), "ref and sol should be of same length"
    ip =0
    refLenSQ = 0

    for j in xrange(len(ref)):
        ip += sol[j] * ref[j]
        refLenSQ += ref[j] * ref[j]
    refLenSQ **= 0.5
    d1 = abs(ip)/ refLenSQ

    d2 = 0
    for i in xrange(len(ref)):
        d2 += (sol[i] - d1 * (ref[i] / refLenSQ)) * (sol[i] - d1 * (ref[i] / refLenSQ))
    d2 **= 0.5
    return d2


def associate(problem, population, reference_points):
    for individual in population:
        temp_min_value = 1e32
        for rp in reference_points:
            temp_distance = perpendicular_distance(rp.coordinates, individual.normalized)
            assert(temp_distance >= 0), "Something is wrong"
            if temp_distance < temp_min_value:
                temp_min_value = temp_distance
                index = rp.id
        individual.cluster_id = index
        individual.perpendicular_distance = temp_min_value

    return population


def assignment(problem, fullpopulation0, reference_points, configuration):

    from copy import deepcopy
    fullpopulation = deepcopy(fullpopulation0)
    population = [pop for pop in fullpopulation if pop.front_no == 0]
    last_front = [pop for pop in fullpopulation if pop.front_no == -1]

    assert(len(population) + len(last_front) == len(fullpopulation)), "population + last_front == full_population"

    remain = configuration["Universal"]["Population_Size"] - len(population)
    assert(remain <= len(last_front)), "remain should be less that last_front"
    count_reference_points = [0 for _ in reference_points]  # ro
    for individual in population: count_reference_points[individual.cluster_id] += 1

    assert(sum(count_reference_points) == len(population)), "Sanity Check"
    from random import shuffle
    flags = [False for _ in xrange(len(reference_points))]  #flag
    num = 0

    while num < remain:
        perm = [i for i in xrange(len(reference_points))]
        shuffle(perm)
        min_no = 1e32  # min
        id_to_consider = -1  # id

        for perm_index in perm:  # perm[i]
            if not flags[perm_index] and count_reference_points[perm_index] < min_no:
                min_no = count_reference_points[perm_index]
                id_to_consider = perm_index

        possible_options = []  # list
        for k in xrange(len(last_front)):
            if last_front[k].cluster_id == id_to_consider:
                possible_options.append(k)

        if len(possible_options) != 0:
            index_number = 0  # index
            if count_reference_points[id_to_consider] == 0:  # population doesn't have point near reference point id
                min_distance = 1e32  # minDist
                for j in xrange(len(possible_options)):
                    if last_front[possible_options[j]].perpendicular_distance < min_distance:
                        min_distance = last_front[possible_options[j]].perpendicular_distance
                        index_number = j
            else:
                from random import randint
                index_number = randint(0, len(possible_options) - 1)

            population.append(deepcopy(last_front[possible_options[index_number]]))
            count_reference_points[id_to_consider] += 1

            last_front.pop(possible_options[index_number])
            num += 1

        else:
            flags[id_to_consider] = True

    assert(len(population) == configuration["Universal"]["Population_Size"]), "This function needs to generate remain number of population"
    return population

# ---------------------- Helper --------------------------------
def nsgaiii_selector2(problem, population, configuration, values_to_be_passed):
    assert (len(population) % 4 == 0), "The population size needs to be multiple if 4. Look at footnote page 584"
    return population, 0


def nsgaiii_regenerate2(problem, population, configuration):
    assert (len(population) == configuration["Universal"]["Population_Size"]), "The population should be equal to the population size as defined in jmoo_properties"
    assert (len(population) % 4 == 0), "The population size needs to be multiple if 4. Look at footnote page 584"

    mutants = []
    for count, individual in enumerate(population): mutants.append(variation(problem, count, population, configuration))
    assert (len(mutants) == len(population)), "The population after regeneration must be double"
    return mutants, len(mutants)


def nsgaiii_recombine2(problem, population, selectees, configuration):
    k = configuration["Universal"]["Population_Size"]
    assert (len(population) % 4 == 0), "The population size needs to be multiple if 4. Look at footnote page 584"
    assert (len(population + selectees) == 2 * len(population)), \
        "The recombination population should be 2 * len(population)"
    evaluate_no = 0
    for individual in population+selectees:
            if not individual.valid:
                individual.evaluate()
                evaluate_no += 1
    Individuals = jmoo_algorithms.deap_format(problem, population + selectees)
    assert(len(Individuals) == len(population) + len(selectees)), "Error in changing formal from JMOO to deap"
    pareto_fronts = sortNondominated(Individuals, k)
    from itertools import chain
    assert(len(list(chain(*pareto_fronts))) >= k), \
        "Non dominated sorting should return number greater than or equal to k (jmoo_properties.MU)"

    population = convert_to_jmoo(problem, pareto_fronts)
    assert(len(population) == len(list(chain(*pareto_fronts)))),\
        "Length of the population and mgpopulation should be equal to pareto_fronts"

    ideal_point = compute_ideal_points(problem, population)
    max_point = compute_max_points(problem, population)

    extreme_points = compute_extreme_points(problem, population, ideal_point)
    intercept_point = compute_intercept_points(problem, extreme_points, ideal_point, max_point)
    population = normalization(problem, population, intercept_point, ideal_point)

    divisions = division_dict[str(len(problem.objectives))]
    reference_points = two_level_weight_vector_generator(divisions, len(problem.objectives))  # is always constant | checked!


    population = associate(problem, population, reference_points)
    population = assignment(problem, population, reference_points, configuration)

    assert(len(population) == configuration["Universal"]["Population_Size"]), "This function needs to generate remain number of population"


    return population, evaluate_no


def clear_extra_fields(individual):
    individual.front_no = -10
    individual.normalized = []
    individual.perpendicular_distance = -1
    return individual