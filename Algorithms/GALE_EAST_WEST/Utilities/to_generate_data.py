def generate_data(problem, number_of_points):
    dataset = []
    while len(dataset) < number_of_points:
        print "# ", len(dataset),
        import sys
        sys.stdout.flush()
        temp_dataset = []
        for run in xrange(number_of_points):
            temp_dataset.append(problem.generateInput())

        import itertools
        dataset.sort()
        dataset.extend(list(temp_dataset for temp_dataset,_ in itertools.groupby(temp_dataset)))

    from random import shuffle
    shuffle(dataset)
    return dataset[:number_of_points]

