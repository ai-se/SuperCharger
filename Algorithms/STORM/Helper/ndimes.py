"""
Algorithm for the Isotropic method for producing random points on a unit N-hypersphere
A Note on a Uniformly Method for Generating Points on N-Dimensional Spheres
"""
from __future__ import division
from random import normalvariate
import numpy

def ndes_generate_direction(points, midpoint):
    r = sum([point**2 for point in points])**0.5
    temp = [(point/r) for i, point in enumerate(points)]
    return temp

def generate_direction(dimension, no_points, midpoint):
        return [ndes_generate_direction([normalvariate(0, 1) for _ in xrange(dimension)], midpoint)
                for _ in xrange(no_points)]


# ------------------------ Testing ------------------------- #

def euclidean_distance(pointa, pointb):
    def dist(x,y):
        return numpy.sqrt(numpy.sum((x-y)**2))

    return dist(numpy.array(pointa), numpy.array(pointb))

if __name__ == "__main__":
    dimension = 3
    no_points = 40
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    points = generate_direction(dimension, no_points, [0, 0, 0])
    # print points

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([point[0] for point in points],[point[1] for point in points], [point[2] for point in points] )
    plt.show()