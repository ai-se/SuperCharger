

def find_midpoint(pointa, pointb):
    temp = []
    for decisiona, decisionb in zip(pointa, pointb):
        temp.append((decisiona + decisionb)/2)
    return temp

def find_extreme_point(points):
    maxp = []
    minp = []
    for i in xrange(len(points[0])):
        one_dim_points = [point[i] for point in points]
        maxp.append(max(one_dim_points))
        minp.append(min(one_dim_points))
    assert(len(maxp) == len(minp)), "Something's wrong"
    return maxp, minp

def find_central_point(poles):
    assert(len(poles[0]) == 2), "There has to be 2 points in each pole"
    midpoints = [find_midpoint(pole[0].decisionValues, pole[-1].decisionValues) for pole in poles]
    min_point, max_point = find_extreme_point(midpoints)
    return find_midpoint(min_point, max_point)


