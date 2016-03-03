from jmoo_stats_box import *
import os, inspect, sys


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import jmoo_properties
from STORM.Helper.mutator import extrapolate
from STORM.Helper.geometry import find_central_point
from STORM.Helper.poles import find_poles, look_for_duplicates, find_poles3, find_poles2
from STORM.Helper.better import rearrange
from STORM.Helper.scores import scores
from STORM.Helper.nudge import nudge

from STORM.Helper.scores import scores2


def anywhere_mutate(problem, population, configurations):
    return population, 0


def anywhere_recombine(problem, popuplation, mutants, configurations):
    return mutants, 0


# def anywhere3_selector(problem, individuals):
#     new_population = []
#     mutated_population = []
#     new_population.extend(individuals)
#     for count in xrange(jmoo_properties.ANYWHERE_EXPLOSION):
#         new_population.extend([extrapolate(problem, individuals, individual, jmoo_properties.F, jmoo_properties.CF)
#                                for individual in individuals])
#     poles = find_poles(new_population)
#
#
#     stars = []
#     for p1, p2 in poles:
#         stars.append(p1)
#         stars.append(p2)
#     midpoint = jmoo_individual(problem, find_central_point(poles), None)
#     stars = rearrange(problem, midpoint, stars)
#     #stars = find_poles2(problem, new_population)
#
#     print ">> ", len([x for x in individuals if x.fitness.fitness is not None]), jmoo_properties.ANYWHERE_POLES
#
#
#     # remove population from new population TODO: Clean up
#     raw_poles = []
#     for s in stars:
#         for star in [s.east, s.west]:
#             if look_for_duplicates(star, raw_poles) is False:
#                 star.correct_pole = s.id  # added to keep in sync with the mutated_population
#                 star.anyscore = 1e32  # added to keep in sync with the mutated_population
#                 raw_poles.append(star)
#             else: continue
#
#             for pop in new_population:
#                 if star. decisionValues == pop.decisionValues:
#                     new_population.remove(pop)
#
#
#     distribution_list = []
#     for individual in new_population:
#         correct_poles, individual = scores2(individual, stars)
#         distribution_list.extend(correct_poles)
#         for poles in correct_poles:
#             temp_individual = nudge(problem, individual, stars[poles].east, individual.anyscore)
#             temp_individual.anyscore = individual.anyscore
#             temp_individual.correct_pole = poles
#             mutated_population.append(temp_individual)
#
#     mutated_population.extend(raw_poles) # adding the poles to the population
#
#     distribution_list = list(set(distribution_list))
#     return_population = []
#     # print "Length of the new_population: ", len(new_population)
#     # print "Length of the mutated population: ", len(mutated_population)
#     # print len([x for x in mutated_population if x.fitness.fitness is not None])
#     for point in distribution_list:
#         temp_list = [individual for individual in mutated_population if individual.correct_pole == point]
#         return_population += sorted(temp_list, key=lambda x:x.anyscore, reverse=True)[:(len(temp_list) * 100)/len(mutated_population)]
#     howmany = jmoo_properties.MU - len(return_population)
#     for _ in xrange(howmany):
#         return_population.append(jmoo_individual(problem, problem.generateInput(), None))
#     # print "Length of return population: ", len(return_population)
#     return return_population, len(stars)

def anywhere_selector(problem, individuals, configurations):
    print "=" * 10
    new_population = []
    mutated_population = []
    new_population.extend(individuals)
    for count in xrange(jmoo_properties.ANYWHERE_EXPLOSION):
        new_population.extend([extrapolate(problem, individuals, individual, jmoo_properties.F, jmoo_properties.CF)
                               for individual in individuals])

    import pdb
    pdb.set_trace()

    stars = find_poles2(problem, new_population)


    # print ">> ", len([x.fitness.fitness for x in new_population if x.fitness.fitness is not None]), len(new_population), jmoo_properties.ANYWHERE_POLES
    # exit()

    # remove population from new population TODO: Clean up
    raw_poles = []
    for s in stars:
        for star in [s.east, s.west]:
            if look_for_duplicates(star, raw_poles) is False:
                star.correct_pole = s.id  # added to keep in sync with the mutated_population
                star.anyscore = 1e32  # added to keep in sync with the mutated_population
                raw_poles.append(star)
            else: continue

            for pop in new_population:
                if star. decisionValues == pop.decisionValues:
                    new_population.remove(pop)


    distribution_list = []
    for individual in new_population:
        correct_poles, individual = scores2(individual, stars)
        distribution_list.extend(correct_poles)
        for poles in correct_poles:
            temp_individual = nudge(problem, individual, stars[poles].east, individual.anyscore)
            temp_individual.anyscore = individual.anyscore
            temp_individual.correct_pole = poles
            mutated_population.append(temp_individual)

    mutated_population.extend(raw_poles) # adding the poles to the population

    distribution_list = list(set(distribution_list))
    return_population = []
    # print "Length of the new_population: ", len(new_population)
    # print "Length of the mutated population: ", len(mutated_population)
    # print len([x for x in mutated_population if x.fitness.fitness is not None])
    for point in distribution_list:
        temp_list = [individual for individual in mutated_population if individual.correct_pole == point]
        return_population += sorted(temp_list, key=lambda x:x.anyscore, reverse=True)[:(len(temp_list) * 100)/len(mutated_population)]
    howmany = jmoo_properties.MU - len(return_population)
    for _ in xrange(howmany):
        return_population.append(jmoo_individual(problem, problem.generateInput(), None))
    # print "Length of return population: ", len(return_population)
    # print "length of stars: ", len(stars)
    return return_population, sum([1 if x.fitness.fitness != None else 0 for x in return_population])


def anywhere3_selector(problem, individuals, Configurations, values_to_be_passed):
    new_population = []
    mutated_population = []
    new_population.extend(individuals)

    # The population explodes by Configurations["STORM"]["STORM_EXPLOSION"] times
    for count in xrange(Configurations["STORM"]["STORM_EXPLOSION"]):
        new_population.extend([extrapolate(problem, individuals, individual, Configurations["STORM"]["F"],
                                           Configurations["STORM"]["CF"]) for individual in individuals])

    stars = find_poles3(problem, new_population, Configurations)

    # remove population from new population TODO: Clean up
    raw_poles = []
    for s in stars:
        for star in [s.east, s.west]:
            if look_for_duplicates(star, raw_poles) is False:
                star.correct_pole = s.id  # added to keep in sync with the mutated_population
                star.anyscore = 1e32  # added to keep in sync with the mutated_population
                raw_poles.append(star)
            else: continue

            # Remove the star from the new_population
            new_population = [pop for pop in new_population if pop != star]

    poles_distribution_list = []
    for individual in new_population:
        # correct_poles, individual = scores(individual, stars, Configurations)
        correct_poles_scores, individual = scores2(individual, stars, Configurations)
        correct_poles = [x[0] for x in correct_poles_scores]
        increments = [x[-1] for x in correct_poles_scores]

        # distribution_list would be used to help in the culling process
        poles_distribution_list.extend(correct_poles)
        for poles, increment in zip(correct_poles, increments):
            temp_individual = nudge(problem, individual, stars[poles].east, increment, Configurations)
            temp_individual.anyscore = increment
            temp_individual.correct_pole = poles
            mutated_population.append(temp_individual)

    mutated_population.extend(raw_poles) # adding the poles to the population
    # from Helper.culling import culling
    # after_culling_population = culling(poles_distribution_list, mutated_population, Configurations)
    # return after_culling_population, sum([1 if x.fitness.fitness is not None else 0 for x in after_culling_population])


    distribution_list = list(set(poles_distribution_list))
    return_population = []
    # print "Length of the new_population: ", len(new_population)
    # print "Length of the mutated population: ", len(mutated_population)
    # print len([x for x in mutated_population if x.fitness.fitness is not None])
    for point in distribution_list:
        temp_list = [individual for individual in mutated_population if individual.correct_pole == point]
        return_population += sorted(temp_list, key=lambda x:x.anyscore, reverse=True)[:(len(temp_list) * 100)/len(mutated_population)]
    howmany = Configurations["Universal"]["Population_Size"] - len(return_population)
    for _ in xrange(howmany):
        return_population.append(jmoo_individual(problem, problem.generateInput(), None))
    # print "Length of return population: ", len(return_population)
    # print "length of stars: ", len(stars)
    return return_population, sum([1 if x.fitness.fitness != None else 0 for x in return_population])
