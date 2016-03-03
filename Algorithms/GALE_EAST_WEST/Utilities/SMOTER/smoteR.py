from __future__ import division
class Candidate():
    def __init__(self, independent, dependent, class_name=None):
        self.independent = independent
        self.dependent = dependent
        self.class_name = class_name

    def set_class_name(self, name):
        self.class_name = name


def class_names(dependent, min_value, max_value, bins=5):
    bin_size = (max_value - min_value)/bins
    return int((dependent - min_value)/bin_size)


def euclidean_distance(list1, list2):
    assert(len(list1) == len(list2)), "The points don't have the same dimension"
    distance = sum([(i - j) ** 2 for i, j in zip(list1, list2)]) ** 0.5
    assert(distance >= 0), "Distance can't be less than 0"
    return distance


def apply_over_sampling(candidates, number_of_points):
    ng = int(len(candidates)/2)
    new_samples = candidates[:]

    if len(candidates) == 1: return candidates * number_of_points

    for np in xrange(number_of_points):
        case = candidates[np % len(candidates)]
        neighbors = sorted(candidates, key=lambda x: euclidean_distance(case.independent, x.independent))[1:1+ng]
        from random import choice
        x = choice(neighbors)

        new_indep = [0 for _ in xrange(len(x.independent))]

        # For independent Variables
        for index in xrange(len(x.independent)):
            diff = case.independent[index] - x.independent[index]
            from random import random
            new_indep[index] = case.independent[index] + random() * diff

        # For dependent Variables
        # d1 = euclidean_distance(new_indep, case.independent)
        # d2 = euclidean_distance(new_indep, x.independent)
        # new_dep = (d2 * case.dependent + d1 * x.dependent) / (d1 + d2)

        from random import random
        new_dep = case.dependent + random() * (x.dependent - case.dependent)

        new_samples.append(Candidate(new_indep, new_dep, case.class_name))

    return new_samples


def apply_smote(list_of_indep, list_of_dep):

    new_samples = []

    assert(len(list_of_dep) == len(list_of_indep)), "Something is wrong"
    Candidates = [Candidate(indep, dep) for indep, dep in zip(list_of_indep, list_of_dep)]

    # Assigning class names
    min_value = min(list_of_dep)
    max_value = max(list_of_dep)


    candidate_dict = {}
    for C in Candidates:
        class_name = class_names(C.dependent, min_value, max_value)
        if class_name in candidate_dict.keys(): candidate_dict[class_name].append(C)
        else: candidate_dict[class_name] = [C]
        candidate_dict[class_name][-1].set_class_name(class_name)

    # Finding Rare classes and Frequent classes
    rare_classes = []  # SMOTE
    frequent_classes = []  # under sampled

    from numpy import median
    y_median = int(median([len(candidate_dict[key]) for key in candidate_dict.keys()]))

    for key in candidate_dict.keys():
        if len(candidate_dict[key]) < y_median: rare_classes.append(key)
        elif len(candidate_dict[key]) > y_median:  frequent_classes.append(key)

    for rare_class in rare_classes:
        new_samples.extend(apply_over_sampling(candidate_dict[rare_class], y_median))

    for key in list(set(candidate_dict.keys()) - set(rare_classes)):
        new_samples.extend(candidate_dict[key])


    return [x.independent for x in new_samples], [x.dependent for x in new_samples]






