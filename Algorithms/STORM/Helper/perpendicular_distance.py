def perpendicular_distance(pointa, pointb):
    """

    :param pointa:  the line from the origin passes through point a
    :param pointb:
    :return:
    """
    def dotproduct(pointa, pointb):
        ret = 0
        for i, j in zip(pointa, pointb):
            ret += (i*j)
        return ret

    def magnitude(pointa):
        sum = 0
        for i in pointa:
            sum += i ** 2
        return sum ** 0.5
    mag = dotproduct(pointa, pointb)/(magnitude(pointa))
    lengthb = magnitude(pointb) # hypotenuse
    base = mag
    return (lengthb ** 2 - base ** 2) ** 0.5