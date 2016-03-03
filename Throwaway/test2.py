def distance_matrix_transformation(distance_matrix, cut):
    left_dm = [d[:cut] for d in distance_matrix[:cut]]
    right_dm = [d[cut:] for d in distance_matrix[cut:]]
    return left_dm, right_dm


from random import randint
distance_matrix = [[randint(1, 100) for _ in xrange(4)] for _ in xrange(4)]

for d in distance_matrix: print d

left, right = distance_matrix_transformation(distance_matrix, 1)

for l in left: print l

for r in right: print r
