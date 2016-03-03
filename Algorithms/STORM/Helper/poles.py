import os, inspect, sys, random

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../Techniques")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from Techniques.euclidean_distance import euclidean_distance
from ndimes import generate_direction
from perpendicular_distance import perpendicular_distance
from geometry import find_extreme_point, find_midpoint
from better import rearrange

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import jmoo_properties
from jmoo_individual import jmoo_individual


def find_extreme(one, population):
    temp = []
    for individual in population:
        temp_distance = euclidean_distance(one.decisionValues, individual.decisionValues), individual
        assert(temp_distance > 1), "Something's wrong"
        temp.append([temp_distance, individual])
    return sorted(temp, key=lambda x: x[0], reverse=True)[0][1]


def look_for_duplicates(element, lst, field=lambda x: x):
    for l in lst:
        if field(element) == field(l):
            return True
    return False

def find_poles(problem, population):
    poles = []
    #remove duplicates
    temp_poles = []
    for _ in xrange(jmoo_properties.ANYWHERE_POLES):
        while True:
            one = random.choice(population)
            east = find_extreme(one, population)
            west = find_extreme(east, population)
            if east != west and east != one and west != one and east not in list(temp_poles) and west not in list(temp_poles): break
        poles.append(east)
        poles.append(west)
        if look_for_duplicates(east, temp_poles) is False:
            temp_poles.append(east)
        else:
            assert(True),"Something'S wrong"
        if look_for_duplicates(west, temp_poles, lambda x: x.decisionValues) is False:
            temp_poles.append(west)
        else:
            assert(True),"Something'S wrong"

    min_point, max_point = find_extreme_point([pop.decisionValues for pop in poles])
    mid_point = find_midpoint(min_point, max_point)
    mid_point = jmoo_individual(problem, mid_point, None)
    stars = rearrange(problem, mid_point, poles)
    return stars


def find_poles2(problem, population):
    def midpoint(population):
        def median(lst):
            import numpy
            return numpy.median(numpy.array(lst))

        mdpnt = []
        for dec in xrange(len(population[0].decisionValues)):
            mdpnt.append(median([pop.decisionValues[dec] for pop in population]))
        assert(len(mdpnt) == len(population[0].decisionValues)), "Something's wrong"
        # print mdpnt
        return jmoo_individual(problem, mdpnt, None)

    def generate_directions(problem):
        def gen(point):
            r = sum([pp**2 for pp in point])**0.5
            return [round(p/r,3) for p in point]
        coordinates = [gen([random.uniform(0, 1) for _ in xrange(len(problem.decisions))]) for _ in xrange(jmoo_properties.ANYWHERE_POLES * 2)]
        for co in coordinates:
            assert(int(round(euclidean_distance(co, [0 for _ in xrange(len(problem.decisions))]))) == 1), "Something's wrong"
        return coordinates




    # find midpoint
    mid_point = midpoint(population)
    # find directions
    directions = generate_directions(problem)
    # draw a star
    poles =[]
    for direction in directions:
        mine = -1e32
        temp_pole = None
        for pop in population:
            transformed_dec = [(p-m) for p, m in zip(pop.decisionValues, mid_point.decisionValues)]
            y = perpendicular_distance(direction, transformed_dec)
            c = euclidean_distance(transformed_dec, [0 for _ in xrange(len(problem.decisions))])
            # print c, y
            if mine < (c-y):
                mine = c - y
                temp_pole = pop
        poles.append(temp_pole)

    stars = rearrange(problem, mid_point, poles)
    return stars


def find_poles3(problem, population, configurations):
    """This version of find_poles, randomly selects individuals from the population and considers
    assumes them to be the directions
    Intuition: Random directions are better than any
    """
    # min_point = minimum in all dimensions, max_point = maximum in all dimensions
    min_point, max_point = find_extreme_point([pop.decisionValues for pop in population])
    # find mid point between min_point and max_point (mean)
    temp_mid_point = find_midpoint(min_point, max_point)
    # Randomly Sample the population to generate directions. This is a simpler approach to find_poles2()
    directions = [population[i] for i in sorted(random.sample(xrange(len(population)),
                                                              configurations["STORM"]["STORM_POLES"] * 2))]
    # Encapsulate the mid_point into an jmoo_individual structure
    mid_point = jmoo_individual(problem, temp_mid_point, None)
    assert(problem.validate(temp_mid_point) is True), "Mid point is not a valid solution and this shouldn't happen"
    # stars now is a list of poles in the Poles format
    stars = rearrange(problem, mid_point, directions)
    return stars


