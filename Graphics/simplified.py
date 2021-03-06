from __future__ import division
import matplotlib.pyplot as plt


normalization = []


def find_files(problem, algorithm, ipg, rep, gen):
    sep = "_"
    main_file_path = "./RawData/PopulationArchives/"
    problem_algorithm_path = main_file_path + algorithm + sep + problem + sep + ipg + "/"
    rep_path = problem_algorithm_path + str(rep) + "/"
    gen_path = rep_path + str(gen) + ".txt"
    return gen_path


def find_files_for_generations(problem, algorithm, ipg, number_of_repeats, gen):
    return [find_files(problem, algorithm, ipg, rep_no, gen) for rep_no in xrange(number_of_repeats)]


def get_actual_frontier_files(problem, algorithms, ipgs, max_repeats, max_gens):
    files = []
    for algorithm in algorithms:
        for ipg in ipgs:
            files.extend(find_files_for_generations(problem.name, algorithm.name, ipg.__name__, max_repeats, max_gens))
    return files


def get_content(problem, file, population_size, initial_line=False):
    number_of_objectives = len(problem.objectives)
    objectives = []
    contents = open(file, "r").readlines()
    if initial_line is False:
        for content in contents[:population_size]:
            objectives.append([float(c) for count,c in enumerate(content.split(","))][-1 * number_of_objectives:])
        return objectives
    else:
        for content in contents[1:population_size+1]:
            objectives.append([float(c) for count,c in enumerate(content.split(","))][-1 * number_of_objectives:])
        return objectives


def get_content_for_table(problem, file, population_size, initial_line=False):
    number_of_objectives = len(problem.objectives)
    objectives = []
    contents = open(file, "r").readlines()
    if initial_line is False:
        for content in contents[:population_size]:
            objectives.append([float(c) for count,c in enumerate(content.split(","))])
        return objectives
    else:
        for content in contents[1:population_size+1]:
            decisions = map(float, content.strip().split(","))
            objectives.append(decisions + problem.evaluate(decisions))
        return objectives


def get_content_all(problem, file, population_size, initial_line=True):
    objectives = []
    contents = open(file, "r").readlines()
    if initial_line is True:
        for content in contents[1:population_size+1]:
            temp = [float(c) for c in content.split(",")]
            objectives.append(temp)
    else:
        for content in contents[:population_size]:
            temp = [float(c) for c in content.split(",")]
            objectives.append(temp)
    return objectives


def remove_duplicates(objectives):
    # remove duplicates
    import itertools
    objectives.sort()
    removed = list(objectives for objectives, _ in itertools.groupby(objectives))
    return removed


def get_actual_frontier(problem, algorithms, gtechniques, Configurations, tag):
    number_of_objectives = len(problem[-1].objectives)
    pop_size = Configurations["Universal"]["Population_Size"]
    max_repeats = Configurations["Universal"]["Repeats"]
    max_gens = Configurations["Universal"]["No_of_Generations"]
    files = get_actual_frontier_files(problem[-1], algorithms, gtechniques, max_repeats, max_gens)
    content = []
    for file in files:
        content.extend(remove_duplicates(get_content_all(problem[-1], file, pop_size)))

    # change into jmoo_individual
    from jmoo_individual import jmoo_individual
    population = [jmoo_individual(problem[-1], i[:-1*number_of_objectives:], i[-1*number_of_objectives:]) for i in content]

    from jmoo_algorithms import get_non_dominated_solutions
    actual_frontier = [sol.fitness.fitness for sol in
                       get_non_dominated_solutions(problem[-1], population, Configurations)]
    print "Size of the Actual Frontier : ", len(actual_frontier)
    return actual_frontier


def get_normalization_values(problem,  gtechnique, Configurations):
    folder_name = "./Data/"
    filename = folder_name + problem.name + "-p" + str(
        Configurations["Universal"]["Population_Size"]) + "-d" + str(len(problem.decisions)) + "-o" + str(
        len(problem.objectives)) + "-g" + gtechnique.__name__ + "-dataset.txt"

    global normalization
    number_of_objectives = len(problem.objectives)
    contents = open(filename, "r").readlines()
    normalization = [map(float, c.split(',')) for c in contents[-1*number_of_objectives:]]


def get_initial_datapoints(problem, algorithm, gtechnique, Configurations):
    number_of_objectives = len(problem.objectives)
    pop_size = Configurations["Universal"]["Population_Size"]
    folder_name = "./Data/"
    sep = "_"
    filename = folder_name + problem.name + "-p" + str(
        Configurations["Universal"]["Population_Size"]) + "-d" + str(len(problem.decisions)) + "-o" + str(
        len(problem.objectives)) + "-g" + gtechnique.__name__ + "-dataset.txt"

    print "Initial Points are read from file: ", filename, " Algorithm: ", algorithm.name, " GTechnique: ", gtechnique.__name__

    content = get_content(problem, filename, pop_size, initial_line=True)
    from jmoo_individual import jmoo_individual
    population = [jmoo_individual(problem, i[:-1*number_of_objectives], i[-1*number_of_objectives:]) for i in content]
    from jmoo_algorithms import get_non_dominated_solutions
    temp_value = [sol.fitness.fitness for sol in
                   get_non_dominated_solutions(problem, population, Configurations)]
    if len(temp_value) <= 2:
        temp_value = [sol.fitness.fitness for sol in population]
    return temp_value


def apply_normalization(problem, points):
    norm_points = [[0 for _ in xrange(len(problem.objectives))] for _ in xrange(len(points))]
    for i, point in enumerate(points):
        for objective in xrange(len(problem.objectives)):
            norm_points[i][objective] = (point[objective] - normalization[objective][0])/(normalization[objective][2] - normalization[objective][0])
    return norm_points


def draw_igd(problem, algorithms, gtechniques, Configurations, tag):
    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Charts/' + date_folder_prefix):
        os.makedirs('./Results/Charts/' + date_folder_prefix)

    actual_frontier = get_actual_frontier(problem, algorithms, gtechniques, Configurations, tag)
    # actual_frontier = apply_normalization(problem[-1], actual_frontier)
    results = {}
    number_of_repeats = Configurations["Universal"]["Repeats"]
    number_of_objectives = len(problem[-1].objectives)
    generations = Configurations["Universal"]["No_of_Generations"]
    pop_size = Configurations["Universal"]["Population_Size"]
    evaluations = [pop_size*i for i in xrange(generations+1)]

    f, axarr = plt.subplots(1)

    for algorithm in algorithms:
        results[algorithm.name] = {}
        for gtechnique in gtechniques:
            results[algorithm.name][gtechnique.__name__] = {}
            results[algorithm.name][gtechnique.__name__]["mean"] = []
            results[algorithm.name][gtechnique.__name__]["std"] = []
    for algorithm in algorithms:
        for gtechnique in gtechniques:

            points = get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations)
            from PerformanceMetrics.IGD.IGD_Calculation import IGD
            results[algorithm.name][gtechnique.__name__]["mean"].append(IGD(actual_frontier, points))
            results[algorithm.name][gtechnique.__name__]["std"].append(0)

            for generation in xrange(generations):
                print ".",
                import sys
                sys.stdout.flush()
                temp_igd_list = []
                files = find_files_for_generations(problem[-1].name, algorithm.name, gtechnique.__name__, number_of_repeats, generation+1)
                for file in files:
                    temp_value = get_content_all(problem[-1], file, pop_size, initial_line=False)
                    # change into jmoo_individual
                    from jmoo_individual import jmoo_individual
                    population = [jmoo_individual(problem[-1], i[:-1*number_of_objectives], i[-1*number_of_objectives:]) for i in temp_value]

                    from jmoo_algorithms import get_non_dominated_solutions
                    temp_value = [sol.fitness.fitness for sol in
                                   get_non_dominated_solutions(problem[-1], population, Configurations)]
                    temp_igd_list.append(IGD(actual_frontier, temp_value))
                from numpy import mean, std
                results[algorithm.name][gtechnique.__name__]["mean"].append(mean(temp_igd_list))
                results[algorithm.name][gtechnique.__name__]["std"].append(std(temp_igd_list))


            if gtechnique.__name__ == "sway":
                lstyle = "--"
                mk = "v"
                ms = 4
            elif gtechnique.__name__ == "wierd":
                lstyle = "-"
                mk = "o"
                ms = 4
            else:
                lstyle = '-'
                mk = algorithm.type
                ms = 8

    means = []
    stds = []
    labels = []

    for algorithm in algorithms:
        for gtechnique in gtechniques:
            means.append(results[algorithm.name][gtechnique.__name__]["mean"])
            stds.append(results[algorithm.name][gtechnique.__name__]["std"])
            labels.append(algorithm.name+gtechnique.__name__)

    graph_build(problem, means, stds, labels,['Blue', 'CornflowerBlue', 'DarkMagenta', 'DarkOrchid'], evaluations, tag)

    #         axarr.plot(evaluations, results[algorithm.name][gtechnique.__name__], linestyle=lstyle,
    #            label=algorithm.name + "_" + gtechnique.__name__, marker=mk,
    #            color=algorithm.color, markersize=ms, markeredgecolor='none')
    #         axarr.set_autoscale_on(True)
    #         axarr.set_xlim([0, 10000])
    #         # axarr.set_xscale('log', nonposx='clip')
    #         axarr.set_yscale('log', nonposx='clip')
    #         axarr.set_ylabel("IGD")
    #
    #         print
    #         print problem[-1].name, algorithm.name, gtechnique.__name__ , #results[algorithm.name][gtechnique.__name__]
    #
    # f.suptitle(problem[-1].name)
    # fignum = len([name for name in os.listdir('./Results/Charts/' + date_folder_prefix)]) + 1
    # plt.legend(frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.025), fancybox=True, ncol=2)
    # plt.savefig('./Results/Charts/' + date_folder_prefix + '/figure' + str(
    # "%02d" % fignum) + "_" + problem[-1].name + "_" + tag + '.png', dpi=100,bbox_inches='tight')
    # plt.cla()
    # print "Processed: ", problem[-1].name



def draw_hv(problem, algorithms, gtechniques, Configurations, tag):
    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Charts/' + date_folder_prefix):
        os.makedirs('./Results/Charts/' + date_folder_prefix)

    reference_point = [5000 for _ in xrange(len(problem[-1].objectives))]
    results = {}
    number_of_repeats = Configurations["Universal"]["Repeats"]
    generations = Configurations["Universal"]["No_of_Generations"]
    pop_size = Configurations["Universal"]["Population_Size"]
    evaluations = [pop_size*i for i in xrange(generations+1)]

    f, axarr = plt.subplots(1)

    for algorithm in algorithms:
        results[algorithm.name] = {}
        for gtechnique in gtechniques:
            results[algorithm.name][gtechnique.__name__] = {}
            results[algorithm.name][gtechnique.__name__]["mean"] = []
            results[algorithm.name][gtechnique.__name__]["std"] = []
    for algorithm in algorithms:
        for gtechnique in gtechniques:

            points = get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations)
            from PerformanceMetrics.HyperVolume.hv import get_hyper_volume
            results[algorithm.name][gtechnique.__name__]["mean"].append(get_hyper_volume(reference_point, points))
            results[algorithm.name][gtechnique.__name__]["std"].append(0)

            for generation in xrange(generations):
                print ".",
                temp_igd_list = []
                files = find_files_for_generations(problem[-1].name, algorithm.name, gtechnique.__name__, number_of_repeats, generation+1)
                for file in files:
                    temp_value = get_content(problem[-1], file, pop_size)
                    # print [[round(tt, 2) for tt in t] for t in temp_value]
                    temp_igd_list.append(get_hyper_volume(reference_point, temp_value))
                from numpy import mean
                from numpy import mean, std
                results[algorithm.name][gtechnique.__name__]["mean"].append(mean(temp_igd_list))
                results[algorithm.name][gtechnique.__name__]["std"].append(std(temp_igd_list))

            if gtechnique.__name__ == "sway":
                lstyle = "--"
                mk = "v"
            elif gtechnique.__name__ == "wierd":
                lstyle = "-"
                mk = "o"
            else:
                lstyle = '-'
                mk = algorithm.type

    means = []
    stds = []
    labels = []

    for algorithm in algorithms:
        for gtechnique in gtechniques:
            means.append(results[algorithm.name][gtechnique.__name__]["mean"])
            stds.append(results[algorithm.name][gtechnique.__name__]["std"])
            labels.append(algorithm.name+gtechnique.__name__)

    graph_build(problem, means, stds, labels,['Blue', 'CornflowerBlue', 'DarkMagenta', 'DarkOrchid'], evaluations, tag)


    # f.suptitle(problem[-1].name)
    # fignum = len([name for name in os.listdir('./Results/Charts/' + date_folder_prefix)]) + 1
    # plt.legend(frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.025), fancybox=True, ncol=2)
    # plt.savefig('./Results/Charts/' + date_folder_prefix + '/figure' + str(
    # "%02d" % fignum) + "_" + problem[-1].name + "_" + tag + '.png', dpi=100, bbox_inches='tight')
    # plt.cla()
    #
    # print "Processed: ", problem[-1].name


def find_extreme_points(problem, points):
    from Techniques.euclidean_distance import euclidean_distance
    distance_matrix = [[-1 for _ in xrange(len(points))] for _ in xrange(len(points))]
    for i in xrange(len(points)):
        for j in xrange(len(points)):
            if distance_matrix[i][j] == -1:
                temp_dist = euclidean_distance(points[i], points[j])
                distance_matrix[i][j] = temp_dist
                distance_matrix[j][i] = temp_dist
    max_distance = max([max(maps_objective) for maps_objective in distance_matrix])
    indexes = [[(i, j) for j, distance in enumerate(distances) if distance == max_distance] for i, distances in
               enumerate(distance_matrix)]
    index = [index for index in indexes if len(index) > 0][-1][-1]
    return points[index[0]], points[index[1]]


def draw_spread(problem, algorithms, gtechniques, Configurations, tag):
    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Charts/' + date_folder_prefix):
        os.makedirs('./Results/Charts/' + date_folder_prefix)

    actual_frontier = get_actual_frontier(problem, algorithms, gtechniques, Configurations, tag)
    extreme_point1, extreme_point2 = find_extreme_points(problem[-1], actual_frontier)

    results = {}
    number_of_repeats = Configurations["Universal"]["Repeats"]
    generations = Configurations["Universal"]["No_of_Generations"]
    pop_size = Configurations["Universal"]["Population_Size"]
    evaluations = [pop_size*i for i in xrange(generations+1)]

    f, axarr = plt.subplots(1)

    for algorithm in algorithms:
        results[algorithm.name] = {}
        for gtechnique in gtechniques:
            results[algorithm.name][gtechnique.__name__] = {}
            results[algorithm.name][gtechnique.__name__]["mean"] = []
            results[algorithm.name][gtechnique.__name__]["std"] = []
    for algorithm in algorithms:
        for gtechnique in gtechniques:

            points = get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations)

            from PerformanceMetrics.Spread.Spread import spread_calculator
            print algorithm.name, extreme_point1,extreme_point2
            results[algorithm.name][gtechnique.__name__]["mean"].append(spread_calculator(points, extreme_point1,extreme_point2))
            results[algorithm.name][gtechnique.__name__]["std"].append(0)

            for generation in xrange(generations):
                print ".",
                temp_igd_list = []
                files = find_files_for_generations(problem[-1].name, algorithm.name, gtechnique.__name__, number_of_repeats, generation+1)
                for file in files:
                    temp_value = get_content(problem[-1], file, pop_size)
                    # print [[round(tt, 2) for tt in t] for t in temp_value]
                    temp_igd_list.append(spread_calculator(temp_value, extreme_point1,extreme_point2))
                from numpy import mean, std
                results[algorithm.name][gtechnique.__name__]["mean"].append(mean(temp_igd_list))
                results[algorithm.name][gtechnique.__name__]["std"].append(std(temp_igd_list))

            if gtechnique.__name__ == "sway":
                lstyle = "--"
                mk = "v"
            elif gtechnique.__name__ == "wierd":
                lstyle = "-"
                mk = "o"
            else:
                lstyle = '-'
                mk = algorithm.type

    means = []
    stds = []
    labels = []

    for algorithm in algorithms:
        for gtechnique in gtechniques:
            means.append(results[algorithm.name][gtechnique.__name__]["mean"])
            stds.append(results[algorithm.name][gtechnique.__name__]["std"])
            labels.append(algorithm.name+gtechnique.__name__)

    graph_build(problem, means, stds, labels,['Blue', 'CornflowerBlue', 'DarkMagenta', 'DarkOrchid'], evaluations, tag)


            # axarr.plot(evaluations, results[algorithm.name][gtechnique.__name__], linestyle=lstyle,
            #    label=algorithm.name + "_" + gtechnique.__name__, marker=mk,
            #    color=algorithm.color, markersize=8, markeredgecolor='none')
            # axarr.set_autoscale_on(True)
            # axarr.set_xlim([-100, 10000])
            # axarr.set_xscale('log', nonposx='clip')
            # # axarr.set_yscale('log', nonposx='clip')
            # axarr.set_ylabel("Spread")
            #
            # print problem[-1].name, algorithm.name, gtechnique.__name__ , #results[algorithm.name][gtechnique.__name__]
    #
    # f.suptitle(problem[-1].name)
    # fignum = len([name for name in os.listdir('./Results/Charts/' + date_folder_prefix)]) + 1
    # plt.legend(frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.025), fancybox=True, ncol=2)
    # plt.savefig('./Results/Charts/' + date_folder_prefix + '/figure' + str(
    # "%02d" % fignum) + "_" + problem[-1].name + "_" + tag + '.png', dpi=100,bbox_inches='tight')
    # plt.cla()
    #
    # print "Processed: ", problem[-1].name


def graph_build(problem, means, stds, labels, colors, evals, title):
    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Charts/' + date_folder_prefix):
        os.makedirs('./Results/Charts/' + date_folder_prefix)
    import matplotlib.pyplot as plt
    t = evals

    mu1 = means[0]
    mu2 = means[1]
    mu3 = means[2]
    mu4 = means[3]

    sigma1 = stds[0]
    sigma2 = stds[1]
    sigma3 = stds[2]
    sigma4 = stds[3]


    # plot it!
    fig, ax = plt.subplots(1)
    ax.plot(t, mu1, lw=2, label=labels[0], color=colors[0])
    ax.plot(t, mu2, lw=2, label=labels[1], color=colors[1])
    ax.fill_between(t, [m+s for m,s in zip(mu1,sigma1)], [m-s for m,s in zip(mu1,sigma1)], facecolor=colors[0], alpha=0.5)
    ax.fill_between(t, [m+s for m,s in zip(mu2,sigma2)], [m-s for m,s in zip(mu2,sigma2)], facecolor=colors[1], alpha=0.5)
    ax.set_title(title)
    ax.legend(loc='upper left')
    ax.set_xlabel('Evaluations')
    ax.set_ylabel(title)
    ax.grid()
    fignum = len([name for name in os.listdir('./Results/Charts/' + date_folder_prefix)]) + 1
    plt.savefig('./Results/Charts/' + date_folder_prefix + '/figure' + str( "%02d" % fignum) + "_" + problem[-1].name + "_" + title + '_NSGA3.png', dpi=100,bbox_inches='tight')

    plt.cla()

    ax.plot(t, mu3, lw=2, label=labels[2], color=colors[2])
    ax.plot(t, mu4, lw=2, label=labels[3], color=colors[3])
    # ax.fill_between(t, [m+s for m,s in zip(mu3,sigma3)], [m-s for m,s in zip(mu3,sigma3)], facecolor=colors[2], alpha=0.5)
    # ax.fill_between(t, [m+s for m,s in zip(mu4,sigma4)], [m-s for m,s in zip(mu4,sigma4)], facecolor=colors[3], alpha=0.5)
    ax.set_title(title)
    ax.legend(loc='upper left')
    ax.set_xlabel('Evaluations')
    ax.set_ylabel(title)
    # ax.set_yscale('log')
    ax.grid()
    fignum = len([name for name in os.listdir('./Results/Charts/' + date_folder_prefix)]) + 1
    plt.savefig('./Results/Charts/' + date_folder_prefix + '/figure' + str( "%02d" % fignum) + "_" + problem[-1].name + "_" + title + '_MOEAD.png', dpi=100,bbox_inches='tight')


def build_table_for_epsilon(problem, algorithms, gtechniques, Configurations, tag):
    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Tables/' + date_folder_prefix):
        os.makedirs('./Results/Tables/' + date_folder_prefix)

    results = {}
    number_of_repeats = Configurations["Universal"]["Repeats"]
    generations = Configurations["Universal"]["No_of_Generations"]
    pop_size = Configurations["Universal"]["Population_Size"]
    evaluations = [pop_size*i for i in xrange(generations+1)]


    print "==="*20
    print "Problem Name: ", problem[-1].name
    print "Algorithms: ", [a.name for a in algorithms]


    number_of_objectives = len(problem[-1].objectives)
    print "Number of Objectives: ", number_of_objectives
    actual_frontier = get_actual_frontier(problem, algorithms, gtechniques, Configurations, tag)
    print "Length of the Actual Frontier is : ", len(actual_frontier)

    extreme_point1, extreme_point2 = find_extreme_points(problem[-1], actual_frontier)

    f, axarr = plt.subplots(1)

    for algorithm in algorithms:
        results[algorithm.name] = {}
        for gtechnique in gtechniques:
            results[algorithm.name][gtechnique.__name__] = {}
            results[algorithm.name][gtechnique.__name__]["IGD"] = {}
            results[algorithm.name][gtechnique.__name__]["IGD"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"] = []

            results[algorithm.name][gtechnique.__name__]["HV"] = {}
            results[algorithm.name][gtechnique.__name__]["HV"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["HV"]["iqr"] = []

            results[algorithm.name][gtechnique.__name__]["Spread"] = {}
            results[algorithm.name][gtechnique.__name__]["Spread"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"] = []

            for objective in xrange(len(problem[-1].objectives)):
                results[algorithm.name][gtechnique.__name__][str(objective)]={}
                results[algorithm.name][gtechnique.__name__][str(objective)]["median"] = []
                results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"] = []

    for algorithm in algorithms:
        print
        ref_point_list = []
        for gtechnique in gtechniques:ref_point_list.extend(get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations))

        print "Length of ref_point_list : ", len(ref_point_list)

        # this would only be used on wrt to the algorithms
        reference_point = [max([r[o] for r in ref_point_list]) * 5 for o in xrange(number_of_objectives)]
        print "Reference Point used for HyperVolume is : ", reference_point

        fignum = len([name for name in os.listdir('./Results/Tables/' + date_folder_prefix)]) + 1
        filename = './Results/Tables/' + date_folder_prefix+ '/table' + str( "%02d" % fignum) + "_" + problem[-1].name + "_" + algorithm.name + ".csv"
        raw_filename = './Results/Tables/' + date_folder_prefix+ '/raw_table_' + str( "%02d" % fignum) + "_" + problem[-1].name + "_" + algorithm.name + ".csv"
        for gtechnique in gtechniques:

            # since the initial dataset doesn't have evaluated points

            points = get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations)
            print "Length of initial data points is: ", len(points), "Algorithm Name: ", algorithm.name, " Gtechnique: ", gtechnique.__name__
            from PerformanceMetrics.IGD.IGD_Calculation import IGD
            results[algorithm.name][gtechnique.__name__]["IGD"]["median"].append(IGD(actual_frontier, points))
            results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"].append(0)

            from PerformanceMetrics.HyperVolume.hv import get_hyper_volume
            results[algorithm.name][gtechnique.__name__]["HV"]["median"].append(get_hyper_volume(reference_point, points))
            results[algorithm.name][gtechnique.__name__]["HV"]["iqr"].append(0)

            from PerformanceMetrics.Spread.Spread import spread_calculator
            results[algorithm.name][gtechnique.__name__]["Spread"]["median"].append(spread_calculator(points, extreme_point1,extreme_point2))
            results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"].append(0)


            for objective in xrange(len(problem[-1].objectives)):
                temp_list = [p[objective] for p in points]
                from numpy import median
                results[algorithm.name][gtechnique.__name__][str(objective)]["median"].append(median(temp_list))
                results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"].append(0)

            for generation in xrange(generations):
                print ".",
                import sys
                sys.stdout.flush()

                files = find_files_for_generations(problem[-1].name, algorithm.name, gtechnique.__name__, number_of_repeats, generation+1)

                temp_median = [[] for _ in xrange(number_of_objectives)]
                temp_igd = []
                temp_hv = []
                temp_spread = []
                # change into jmoo_individual
                from jmoo_individual import jmoo_individual
                for file in files:
                    temp_values = get_content_for_table(problem[-1], file, pop_size)
                    population = []
                    for temp_value in temp_values:
                        population.append(jmoo_individual(problem[-1], temp_value[:len(problem[-1].decisions)], temp_value[len(problem[-1].decisions):]))

                    from jmoo_algorithms import get_non_dominated_solutions
                    population_fitness = [sol.fitness.fitness for sol in
                                   get_non_dominated_solutions(problem[-1], population, Configurations)]
                    # print "Length of the non-dominated-solutions are: ", len(population_fitness)
                    # The spread calculator would throw error if number of non-dominated solution is less than 1
                    # to circumvent this: I choose to use all the points if such case arise

                    if len(population_fitness) <= 2:
                        population_fitness = [sol.fitness.fitness for sol in population]


                    for objective in xrange(len(problem[-1].objectives)):
                        from numpy import median
                        from numpy import percentile
                        point_list = [p[objective] for p in population_fitness]
                        temp_median[objective].append(median(point_list))

                    # IGD values
                    temp_igd.append(IGD(actual_frontier, population_fitness))
                    temp_hv.append(get_hyper_volume(reference_point, population_fitness))
                    temp_spread.append(spread_calculator(population_fitness, extreme_point1,extreme_point2))

                for objective in xrange(number_of_objectives):
                    results[algorithm.name][gtechnique.__name__][str(objective)]["median"].append(median(temp_median[objective]))
                    iqr = percentile(temp_median[objective], 75) - percentile(temp_median[objective], 25)
                    results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["IGD"]["median"].append(median(temp_igd))
                iqr = percentile(temp_igd, 75) - percentile(temp_igd, 25)
                results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["HV"]["median"].append(median(temp_hv))
                iqr = percentile(temp_hv, 75) - percentile(temp_hv, 25)
                results[algorithm.name][gtechnique.__name__]["HV"]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["Spread"]["median"].append(median(temp_spread))
                iqr = percentile(temp_spread, 75) - percentile(temp_spread, 25)
                results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"].append(iqr)
            print

        print "==="*20

        table = []
        raw_table = []
        table.append(["Generation", "s_o1_median", "s_o1_iqr", "s_o2_median", "s_o2_iqr", "s_o3_median", "s_o3_iqr", "s_igd_median", "s_igd_iqr", "s_hv_median", "s_hv_iqr", "s_spread_median", "s_spread_iqr", "sw_o1_median", "sw_o1_iqr", "sw_o2_median", "sw_o2_iqr", "sw_o3_median", "sw_o3_iqr", "sw_igd_median", "sw_igd_iqr", "sw_hv_median", "sw_hv_iqr", "sw_spread_median", "sw_spread_iqr"])
        raw_table.append(["Generation", "s_o1_median", "s_o1_iqr", "s_o2_median", "s_o2_iqr", "s_o3_median", "s_o3_iqr", "s_igd_median", "s_igd_iqr", "s_hv_median", "s_hv_iqr", "s_spread_median", "s_spread_iqr", "sw_o1_median", "sw_o1_iqr", "sw_o2_median", "sw_o2_iqr", "sw_o3_median", "sw_o3_iqr", "sw_igd_median", "sw_igd_iqr", "sw_hv_median", "sw_hv_iqr", "sw_spread_median", "sw_spread_iqr"])

        # Normalizing
        normalize = [[1e20, -1e20] for _ in xrange(len(problem[-1].objectives)+3)]
        for gtechnique in gtechniques:
            for objective in xrange(len(problem[-1].objectives)):
                normalize[objective][0] = min(normalize[objective][0], min(results[algorithm.name][gtechnique.__name__][str(objective)]["median"]))
                normalize[objective][1] = max(normalize[objective][1], max(results[algorithm.name][gtechnique.__name__][str(objective)]["median"]))
            normalize[-3][0] = min(normalize[-3][0], min(results[algorithm.name][gtechnique.__name__]["IGD"]["median"]))
            normalize[-3][1] = max(normalize[-3][1], max(results[algorithm.name][gtechnique.__name__]["IGD"]["median"]))
            normalize[-2][0] = min(normalize[-2][0], min(results[algorithm.name][gtechnique.__name__]["HV"]["median"]))
            normalize[-2][1] = max(normalize[-2][1], max(results[algorithm.name][gtechnique.__name__]["HV"]["median"]))
            normalize[-1][0] = min(normalize[-1][0], min(results[algorithm.name][gtechnique.__name__]["Spread"]["median"]))
            normalize[-1][1] = max(normalize[-1][1], max(results[algorithm.name][gtechnique.__name__]["Spread"]["median"]))

        for generation in xrange(generations+1):
            line = [generation]
            for gtechnique in gtechniques:
                for objective in xrange(len(problem[-1].objectives)):
                    line.append(round(results[algorithm.name][gtechnique.__name__][str(objective)]["median"][generation], 3))
                    line.append(round(results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"][generation], 3))
                line.append(round(results[algorithm.name][gtechnique.__name__]["IGD"]["median"][generation], 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"][generation], 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["HV"]["median"][generation], 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["HV"]["iqr"][generation], 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["Spread"]["median"][generation], 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"][generation], 8))
            raw_table.append(line)

        for generation in xrange(generations+1):
            line = [generation]
            for gtechnique in gtechniques:
                for objective in xrange(len(problem[-1].objectives)):
                    line.append(round((results[algorithm.name][gtechnique.__name__][str(objective)]["median"][generation] - normalize[objective][0])/(normalize[objective][1] - normalize[objective][0]), 3))
                    line.append(round(results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"][generation] * 100/(normalize[objective][1] - normalize[objective][0]), 3))
                line.append(round((results[algorithm.name][gtechnique.__name__]["IGD"]["median"][generation] - normalize[-3][0])/(normalize[-3][1] - normalize[-3][0]), 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"][generation] * 100/(normalize[-3][1] - normalize[-3][0]), 8))
                line.append(round((results[algorithm.name][gtechnique.__name__]["HV"]["median"][generation] - normalize[-2][0])/(normalize[-2][1] - normalize[-2][0]), 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["HV"]["iqr"][generation] * 100/(normalize[-2][1] - normalize[-2][0]), 8))
                line.append(round((results[algorithm.name][gtechnique.__name__]["Spread"]["median"][generation] - normalize[-1][0])/(normalize[-1][1] - normalize[-1][0]), 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"][generation] * 100/(normalize[-1][1] - normalize[-1][0]), 8))
            table.append(line)


        import csv
        with open(filename, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(table)

        with open(raw_filename, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(raw_table)
        print "done"


def build_for_gale(problem, algorithms, gtechniques, Configurations, tag):

    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Tables/' + date_folder_prefix):
        os.makedirs('./Results/Tables/' + date_folder_prefix)

    results = {}
    number_of_repeats = Configurations["Universal"]["Repeats"]
    generations = Configurations["Universal"]["No_of_Generations"]
    pop_size = Configurations["Universal"]["Population_Size"]
    number_of_objectives = len(problem[-1].objectives)

    actual_frontier = get_actual_frontier(problem, algorithms, gtechniques, Configurations, tag)
    extreme_point1, extreme_point2 = find_extreme_points(problem[-1], actual_frontier)

    f, axarr = plt.subplots(1)

    # Preping the Data Dict
    for algorithm in algorithms:
        results[algorithm.name] = {}
        for gtechnique in gtechniques:
            results[algorithm.name][gtechnique.__name__] = {}
            results[algorithm.name][gtechnique.__name__]["IGD"] = {}
            results[algorithm.name][gtechnique.__name__]["IGD"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"] = []

            results[algorithm.name][gtechnique.__name__]["HV"] = {}
            results[algorithm.name][gtechnique.__name__]["HV"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["HV"]["iqr"] = []

            results[algorithm.name][gtechnique.__name__]["Spread"] = {}
            results[algorithm.name][gtechnique.__name__]["Spread"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"] = []

            for objective in xrange(len(problem[-1].objectives)):
                results[algorithm.name][gtechnique.__name__][str(objective)]={}
                results[algorithm.name][gtechnique.__name__][str(objective)]["median"] = []
                results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"] = []

    for algorithm in algorithms:
        ref_point_list = []
        for gtechnique in gtechniques:ref_point_list.extend(get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations))

        # this would only be used on wrt to the algorithms
        reference_point = [max([r[o] for r in ref_point_list]) * 5 for o in xrange(number_of_objectives)]
        print reference_point

        fignum = len([name for name in os.listdir('./Results/Tables/' + date_folder_prefix)]) + 1
        filename = './Results/Tables/' + date_folder_prefix+ '/table' + str( "%02d" % fignum) + "_" + problem[-1].name + "_" + algorithm.name + ".csv"
        raw_filename = './Results/Tables/' + date_folder_prefix+ '/raw_table_' + str( "%02d" % fignum) + "_" + problem[-1].name + "_" + algorithm.name + ".csv"
        for gtechnique in gtechniques:

            # since the initial dataset doesn't have evaluated points
            points = get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations)
            from PerformanceMetrics.IGD.IGD_Calculation import IGD
            results[algorithm.name][gtechnique.__name__]["IGD"]["median"].append(IGD(actual_frontier, points))
            results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"].append(0)

            from PerformanceMetrics.HyperVolume.hv import get_hyper_volume
            results[algorithm.name][gtechnique.__name__]["HV"]["median"].append(get_hyper_volume(reference_point, points))
            results[algorithm.name][gtechnique.__name__]["HV"]["iqr"].append(0)

            from PerformanceMetrics.Spread.Spread import spread_calculator
            results[algorithm.name][gtechnique.__name__]["Spread"]["median"].append(spread_calculator(points, extreme_point1,extreme_point2))
            results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"].append(0)


            for objective in xrange(len(problem[-1].objectives)):
                temp_list = [p[objective] for p in points]
                from numpy import median
                results[algorithm.name][gtechnique.__name__][str(objective)]["median"].append(median(temp_list))
                results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"].append(0)

            for generation in xrange(generations):
                print ".",
                import sys
                sys.stdout.flush()

                files = find_files_for_generations(problem[-1].name, algorithm.name, gtechnique.__name__, number_of_repeats, generation+1)

                temp_median = [[] for _ in xrange(number_of_objectives)]
                temp_igd = []
                temp_hv = []
                temp_spread = []
                # change into jmoo_individual
                from jmoo_individual import jmoo_individual
                for file in files:
                    temp_values = get_content_for_table(problem[-1], file, pop_size)
                    population = []
                    for temp_value in temp_values:
                        population.append(jmoo_individual(problem[-1], temp_value[:len(problem[-1].decisions)], temp_value[len(problem[-1].decisions):]))

                    from jmoo_algorithms import get_non_dominated_solutions
                    population_fitness = [sol.fitness.fitness for sol in
                                   get_non_dominated_solutions(problem[-1], population, Configurations)]

                    for objective in xrange(len(problem[-1].objectives)):
                        from numpy import median
                        from numpy import percentile
                        point_list = [p[objective] for p in population_fitness]
                        temp_median[objective].append(median(point_list))

                    # IGD values
                    temp_igd.append(IGD(actual_frontier, population_fitness))
                    temp_hv.append(get_hyper_volume(reference_point, population_fitness))
                    temp_spread.append(spread_calculator(population_fitness, extreme_point1,extreme_point2))

                for objective in xrange(number_of_objectives):
                    results[algorithm.name][gtechnique.__name__][str(objective)]["median"].append(median(temp_median[objective]))
                    iqr = percentile(temp_median[objective], 75) - percentile(temp_median[objective], 25)
                    results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["IGD"]["median"].append(median(temp_igd))
                iqr = percentile(temp_igd, 75) - percentile(temp_igd, 25)
                results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["HV"]["median"].append(median(temp_hv))
                iqr = percentile(temp_hv, 75) - percentile(temp_hv, 25)
                results[algorithm.name][gtechnique.__name__]["HV"]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["Spread"]["median"].append(median(temp_spread))
                iqr = percentile(temp_spread, 75) - percentile(temp_spread, 25)
                results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"].append(iqr)

    import pdb
    pdb.set_trace()

def scottknott(problem, algorithms, gtechniques, Configurations, tag):
    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Tables/' + date_folder_prefix):
        os.makedirs('./Results/Tables/' + date_folder_prefix)

    results = {}
    number_of_repeats = Configurations["Universal"]["Repeats"]
    generations = Configurations["Universal"]["No_of_Generations"]
    pop_size = Configurations["Universal"]["Population_Size"]
    evaluations = [pop_size*i for i in xrange(generations+1)]

    number_of_objectives = len(problem[-1].objectives)
    actual_frontier = get_actual_frontier(problem, algorithms, gtechniques, Configurations, tag)

    extreme_point1, extreme_point2 = find_extreme_points(problem[-1], actual_frontier)

    f, axarr = plt.subplots(1)

    for algorithm in algorithms:
        results[algorithm.name] = {}
        for gtechnique in gtechniques:
            results[algorithm.name][gtechnique.__name__] = {}
            results[algorithm.name][gtechnique.__name__]["IGD"] = {}
            results[algorithm.name][gtechnique.__name__]["IGD"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"] = []

            results[algorithm.name][gtechnique.__name__]["HV"] = {}
            results[algorithm.name][gtechnique.__name__]["HV"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["HV"]["iqr"] = []

            results[algorithm.name][gtechnique.__name__]["Spread"] = {}
            results[algorithm.name][gtechnique.__name__]["Spread"]["median"] = []
            results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"] = []

            for objective in xrange(len(problem[-1].objectives)):
                results[algorithm.name][gtechnique.__name__][str(objective)]={}
                results[algorithm.name][gtechnique.__name__][str(objective)]["median"] = []
                results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"] = []

    for algorithm in algorithms:
        ref_point_list = []
        for gtechnique in gtechniques:ref_point_list.extend(get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations))

        # this would only be used on wrt to the algorithms
        reference_point = [max([r[o] for r in ref_point_list]) * 5 for o in xrange(number_of_objectives)]
        print reference_point

        fignum = len([name for name in os.listdir('./Results/Tables/' + date_folder_prefix)]) + 1
        filename = './Results/Tables/' + date_folder_prefix+ '/table' + str( "%02d" % fignum) + "_" + problem[-1].name + "_" + algorithm.name + ".csv"
        for gtechnique in gtechniques:

            # since the initial dataset doesn't have evaluated points
            points = get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations)
            from PerformanceMetrics.IGD.IGD_Calculation import IGD
            results[algorithm.name][gtechnique.__name__]["IGD"]["median"].append(IGD(actual_frontier, points))
            results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"].append(0)

            from PerformanceMetrics.HyperVolume.hv import get_hyper_volume
            results[algorithm.name][gtechnique.__name__]["HV"]["median"].append(get_hyper_volume(reference_point, points))
            results[algorithm.name][gtechnique.__name__]["HV"]["iqr"].append(0)

            from PerformanceMetrics.Spread.Spread import spread_calculator
            results[algorithm.name][gtechnique.__name__]["Spread"]["median"].append(spread_calculator(points, extreme_point1,extreme_point2))
            results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"].append(0)


            for objective in xrange(len(problem[-1].objectives)):
                temp_list = [p[objective] for p in points]
                from numpy import median
                results[algorithm.name][gtechnique.__name__][str(objective)]["median"].append(median(temp_list))
                results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"].append(0)

            for generation in xrange(generations):
                print ".",
                import sys
                sys.stdout.flush()

                files = find_files_for_generations(problem[-1].name, algorithm.name, gtechnique.__name__, number_of_repeats, generation+1)

                temp_median = [[] for _ in xrange(number_of_objectives)]
                temp_igd = []
                temp_hv = []
                temp_spread = []
                for file in files:
                    temp_value = get_content(problem[-1], file, pop_size)
                    # temp_point_list.append(temp_value)

                    for objective in xrange(len(problem[-1].objectives)):
                        from numpy import median
                        from numpy import percentile
                        point_list = [p[objective] for p in temp_value]
                        temp_median[objective].append(median(point_list))



                    temp_value = get_content_all(problem[-1], file, pop_size, initial_line=False)
                    # change into jmoo_individual
                    from jmoo_individual import jmoo_individual
                    population = [jmoo_individual(problem[-1], i[:-1*number_of_objectives:], i[-1*number_of_objectives:]) for i in temp_value]

                    from jmoo_algorithms import get_non_dominated_solutions
                    temp_value = [sol.fitness.fitness for sol in
                                   get_non_dominated_solutions(problem[-1], population, Configurations)]

                    # IGD values
                    temp_igd.append(IGD(actual_frontier, temp_value))
                    temp_hv.append(get_hyper_volume(reference_point, temp_value))
                    temp_spread.append(spread_calculator(temp_value, extreme_point1,extreme_point2))


                for objective in xrange(number_of_objectives):
                    results[algorithm.name][gtechnique.__name__][str(objective)]["median"].append(median(temp_median[objective]))
                    iqr = percentile(temp_median[objective], 75) - percentile(temp_median[objective], 25)
                    results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["IGD"]["median"].append(median(temp_igd))
                iqr = percentile(temp_igd, 75) - percentile(temp_igd, 25)
                results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["HV"]["median"].append(median(temp_hv))
                iqr = percentile(temp_hv, 75) - percentile(temp_hv, 25)
                results[algorithm.name][gtechnique.__name__]["HV"]["iqr"].append(iqr)

                results[algorithm.name][gtechnique.__name__]["Spread"]["median"].append(median(temp_spread))
                iqr = percentile(temp_spread, 75) - percentile(temp_spread, 25)
                results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"].append(iqr)



        table = []
        table.append(["Generation", "s_o1_median", "s_o1_iqr", "s_o2_median", "s_o2_iqr", "s_o3_median", "s_o3_iqr", "s_igd_median", "s_igd_iqr", "s_hv_median", "s_hv_iqr", "s_spread_median", "s_spread_iqr", "sw_o1_median", "sw_o1_iqr", "sw_o2_median", "sw_o2_iqr", "sw_o3_median", "sw_o3_iqr", "sw_igd_median", "sw_igd_iqr", "sw_hv_median", "sw_hv_iqr", "sw_spread_median", "sw_spread_iqr"])

        # Normalizing
        normalize = [[1e10, -1e10] for _ in xrange(len(problem[-1].objectives)+3)]
        for gtechnique in gtechniques:
            for objective in xrange(len(problem[-1].objectives)):
                normalize[objective][0] = min(normalize[objective][0], min(results[algorithm.name][gtechnique.__name__][str(objective)]["median"]))
                normalize[objective][1] = max(normalize[objective][1], max(results[algorithm.name][gtechnique.__name__][str(objective)]["median"]))
            normalize[-3][0] = min(normalize[-3][0], min(results[algorithm.name][gtechnique.__name__]["IGD"]["median"]))
            normalize[-3][1] = max(normalize[-3][1], max(results[algorithm.name][gtechnique.__name__]["IGD"]["median"]))
            normalize[-2][0] = min(normalize[-2][0], min(results[algorithm.name][gtechnique.__name__]["HV"]["median"]))
            normalize[-2][1] = max(normalize[-2][1], max(results[algorithm.name][gtechnique.__name__]["HV"]["median"]))
            normalize[-1][0] = min(normalize[-1][0], min(results[algorithm.name][gtechnique.__name__]["Spread"]["median"]))
            normalize[-1][1] = max(normalize[-1][1], max(results[algorithm.name][gtechnique.__name__]["Spread"]["median"]))
        print normalize[-2][0], normalize[-2][1]

        for generation in xrange(generations+1):
            line = [generation]
            for gtechnique in gtechniques:
                for objective in xrange(len(problem[-1].objectives)):
                    line.append(round((results[algorithm.name][gtechnique.__name__][str(objective)]["median"][generation] - normalize[objective][0])/(normalize[objective][1] - normalize[objective][0]), 3))
                    line.append(round(results[algorithm.name][gtechnique.__name__][str(objective)]["iqr"][generation] * 100/(normalize[objective][1] - normalize[objective][0]), 3))
                line.append(round((results[algorithm.name][gtechnique.__name__]["IGD"]["median"][generation] - normalize[-3][0])/(normalize[-3][1] - normalize[-3][0]), 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["IGD"]["iqr"][generation] * 100/(normalize[-3][1] - normalize[-3][0]), 8))
                line.append(round((results[algorithm.name][gtechnique.__name__]["HV"]["median"][generation] - normalize[-2][0])/(normalize[-2][1] - normalize[-2][0]), 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["HV"]["iqr"][generation] * 100/(normalize[-2][1] - normalize[-2][0]), 8))
                line.append(round((results[algorithm.name][gtechnique.__name__]["Spread"]["median"][generation] - normalize[-3][0])/(normalize[-3][1] - normalize[-3][0]), 8))
                line.append(round(results[algorithm.name][gtechnique.__name__]["Spread"]["iqr"][generation] * 100/(normalize[-3][1] - normalize[-3][0]), 8))
            table.append(line)


        import csv
        with open(filename, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(table)
        print "done"
