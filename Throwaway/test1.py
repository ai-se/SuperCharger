def avg(list): return (float)(sum(list)) / (float)(len(list))


def approach1(dataset):
    dim = len(dataset[0])

    d_ = []
    for i, fit_i in enumerate(dataset):
        fma = []
        for j, fit_j in enumerate(dataset):
            if not i == j:
                fma.append(sum([abs(fit_i[k] - fit_j[k]) for k in range(dim)]))
        d_.append(min(fma))
    d_bar = avg(d_)
    ssm = ((1 / float(len(dataset) - 1)) * sum([(d_bar - d_i) ** 2 for d_i in d_])) ** 0.5
    return ssm


def approach2(dataset):
    dim = len(dataset[0])
    d_ =[]
    d_ = [min([sum([abs(fit_i[k] - fit_j[k]) for k in range(dim)]) for j, fit_j in enumerate(dataset) if i != j]) for i, fit_i in enumerate(dataset)]
    d_bar = avg(d_)
    ssm = ((1 / float(len(dataset) - 1)) * sum([(d_bar - d_i) ** 2 for d_i in d_])) ** 0.5
    return ssm


def approch3(dataset):
    """Time required:  25.459327"""
    dim = len(dataset[0])
    dist = lambda x, y: sum([abs(x[k] - y[k]) for k in range(dim)])
    leng = len(dataset)
    distance_matrix = [[-1 for _ in xrange(leng)] for _ in xrange(leng)]
    for i in xrange(leng):
        for j in xrange(leng):
            if i == j: distance_matrix[i][j] = 1e5
            elif distance_matrix[i][j] == -1:
                distance_matrix[i][j] = dist(dataset[i], dataset[j])
                distance_matrix[j][i] = distance_matrix[i][j]

    d_= [min(distance_matrix[i]) for i in xrange(leng)]
    d_bar = avg(d_)
    ssm = ((1 / float(leng - 1)) * sum([(d_bar - d_i) ** 2 for d_i in d_])) ** 0.5
    return ssm

def approch4(X):
    """Time required:  35.484411"""
    dim = len(X[0])
    dist = lambda x, y: sum([abs(x[k] - y[k]) for k in range(dim)])
    from  scipy.spatial.distance import pdist
    distance_matrix = pdist(X, dist)

    return


import pickle
dataset = pickle.load( open( "data.p", "rb" ) )

import time
start = time.clock()
print approach1(dataset),
print "Time required: ", (time.clock() - start)
#
#
# start = time.clock()
# print approach2(dataset),
# print "Time required: ", (time.clock() - start)

start = time.clock()
print approch3(dataset)
print "Time required: ", (time.clock() - start)
#
import pdb
pdb.set_trace()