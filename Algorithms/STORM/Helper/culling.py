
class CullingHelperObject:
    def __init__(self, pole_id, count):
        self.pole_id = pole_id
        self.count = count

    def decrement(self, count=1):
        self.count -= count

    def increment(self, count=1):
        self.count += count

    def __str__(self):
        return "id: " + str(self.pole_id) + " count: " + str(self.count)


def culling(poles_distribution_list, population, Configurations):

    after_culling = []

    # find the distribution
    distribution_list = [0 for _ in xrange(Configurations["STORM"]["STORM_POLES"] * 2)]

    # place individuals in the population into bins
    population_bins = []
    for pole_id in xrange(Configurations["STORM"]["STORM_POLES"] * 2):
        population_bins.append(sorted([individual for individual in population if individual.correct_pole == pole_id],
                                      key=lambda x:x.anyscore, reverse=True))
    assert(sum([len(element) for element in population_bins]) == len(population)), "The binning didn't work!"
    obj_distribution_list = [CullingHelperObject(id, count) for id, count in enumerate(distribution_list)]

    while len(after_culling) < Configurations["Universal"]["Population_Size"]:
        obj_distribution_list = sorted(obj_distribution_list, key=lambda x: x.count)
        if len(population_bins[obj_distribution_list[0].pole_id]) == 0:
            # Since the number of individuals in the bin is 0, we assign a high score so that this bin is not selected
            obj_distribution_list[0].increment(1e32)
            pass
        else:
            # Since the bin elements are sorted in the decreasing order of scores, we use the first element
            after_culling.append(population_bins[obj_distribution_list[0].pole_id][0])
            # remove the element (added to after_culling) from the selection pool
            del population_bins[obj_distribution_list[0].pole_id][0]
            obj_distribution_list[0].increment()

    return after_culling

