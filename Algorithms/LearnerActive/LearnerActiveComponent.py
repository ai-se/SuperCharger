from jmoo_individual import *
from Helper import generate_nodes_and_edges

def la_find(problem, population, configuration, values_to_be_passed):
    print "working1"
    graph, weight_matrix = generate_nodes_and_edges(population)
    # weight_matrix: shows the similarities of the matrix


    import pdb
    pdb.set_trace()
    return population, 0

def la_mutate(problem, population, configuration):
    print "working2"
    return population, 0

def la_regenerate(problem, unusedslot, mutants, configuration):
    print "working3"
    exit()
    return population, 0