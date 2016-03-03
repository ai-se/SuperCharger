from __future__ import division


def find_k_neighbors(points, neighbor_number=5):
    from sklearn.neighbors import NearestNeighbors
    import numpy as np
    X = np.array(points)
    neighbors = NearestNeighbors(n_neighbors=neighbor_number + 1, algorithm='ball_tree').fit(X)
    distances, indices = neighbors.kneighbors(X)
    return [[str(point), list([str(x) for x in indices[point][1:]])] for point in xrange(len(points))]


def generate_distance_matrix(points):
    from Techniques.euclidean_distance import euclidean_distance
    return [[euclidean_distance(points[i], points[j]) for j in xrange(len(points))] for i in xrange(len(points))]


def generate_weight_matrix(points):
    """closer the point higher the weight"""
    def gamma_kernel(x, y, sigma=1):
        from Techniques.euclidean_distance import euclidean_distance
        from math import exp
        return exp(-1 * (euclidean_distance(x, y)** 2)/ (2 * (sigma ** 2)))
    return [[gamma_kernel(points[i], points[j]) if i!=j else -1 for j in xrange(len(points))] for i in xrange(len(points))]


def find_distance_neighbors(points, distance_percentage=35):

    distance_matrix = generate_distance_matrix(points)
    neighbor_distance = max([max([distance_matrix[i][j] for i in xrange(len(points))]) for j in xrange(len(points))]) * distance_percentage/100

    neighbor_matrix = [[str(j) for j in xrange(len(points)) if distance_matrix[i][j] <= neighbor_distance and i!=j] for i in xrange(len(points))]
    return [[str(count), neigh] for count, neigh in enumerate(neighbor_matrix) ]


def draw_graphs(graph_dict):
    points = [[key, graph_dict[key]] for key in graph_dict.keys()]

    import pydot
    graph = pydot.Dot(graph_type='digraph')
    for point in points:
        for neighbor in point[-1]:
            edge = pydot.Edge(point[0], neighbor)
            graph.add_edge(edge)
    graph.write_png('example1_graph.png')


def generate_nodes_and_edges(population):
    decisions = [individual.decisionValues for individual in population]
    objectives = [individual.fitness.fitness for individual in population if individual.fitness.fitness]

    # find connections
    connections = find_distance_neighbors(decisions)

    # generate graphs
    from Graph import Graph
    input = dict((connect[0], connect[-1]) for connect in connections)

    # draw graphs
    # draw_graphs(input)

    return Graph(input), generate_weight_matrix(decisions)


