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
            objectives.append([float(c) for c in content.split(",")][-1 * number_of_objectives:])
    else:
        for content in contents[1:population_size+1]:
            objectives.append([float(c) for c in content.split(",")][-1 * number_of_objectives:])

    return objectives


def get_content_all(problem, file, population_size):
    objectives = []
    contents = open(file, "r").readlines()
    for content in contents[1:population_size+1]:
        temp = [float(c) for c in content.split(",")]
        objectives.append(temp)
    return objectives


need to fix the normalization part
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
    population = [jmoo_individual(problem[-1], i[number_of_objectives:], i[:number_of_objectives]) for i in content]

    from jmoo_algorithms import get_non_dominated_solutions
    actual_frontier = [sol.fitness.fitness for sol in
                       get_non_dominated_solutions(problem[-1], population, Configurations)]
    return actual_frontier


def get_initial_datapoints(problem, algorithm, gtechnique, Configurations):
    pop_size = Configurations["Universal"]["Population_Size"]
    folder_name = "./Data/"
    sep = "_"
    filename = folder_name + problem.name + "-p" + str(
        Configurations["Universal"]["Population_Size"]) + "-d" + str(len(problem.decisions)) + "-o" + str(
        len(problem.objectives)) + "-g" + gtechnique.__name__ + "-dataset.txt"
    return get_content(problem, filename, pop_size, initial_line=True)


def run2(problem, algorithms, gtechniques, Configurations, tag):
    import os
    from time import strftime
    date_folder_prefix = strftime("%m-%d-%Y")
    if not os.path.isdir('./Results/Charts/' + date_folder_prefix):
        os.makedirs('./Results/Charts/' + date_folder_prefix)

    actual_frontier = get_actual_frontier(problem, algorithms, gtechniques, Configurations, tag)
    results = {}
    number_of_repeats = Configurations["Universal"]["Repeats"]
    generations = Configurations["Universal"]["No_of_Generations"]
    pop_size = Configurations["Universal"]["Population_Size"]
    evaluations = [pop_size*i for i in xrange(generations+1)]

    f, axarr = plt.subplots(1)

    for algorithm in algorithms:
        results[algorithm.name] = {}
        for gtechnique in gtechniques:
            results[algorithm.name][gtechnique.__name__] = []
    for algorithm in algorithms:
        for gtechnique in gtechniques:
            points = get_initial_datapoints(problem[-1], algorithm, gtechnique, Configurations)
            from PerformanceMetrics.IGD.IGD_Calculation import IGD
            results[algorithm.name][gtechnique.__name__].append(IGD(actual_frontier, points))

            for generation in xrange(generations):
                temp_igd_list = []
                files = find_files_for_generations(problem[-1].name, algorithm.name, gtechnique.__name__, number_of_repeats, generation+1)
                for file in files:
                    temp_igd_list.append(IGD(actual_frontier, get_content(problem[-1], file, pop_size)))
                from numpy import median
                results[algorithm.name][gtechnique.__name__].append(median(temp_igd_list))

            if gtechnique.__name__ == "sway":
                lstyle = "--"
                mk = "v"
            else:
                lstyle = '-'
                mk = algorithm.type

            axarr.plot(evaluations, results[algorithm.name][gtechnique.__name__], linestyle=lstyle,
               label=algorithm.name + "_" + gtechnique.__name__, marker=mk,
               color=algorithm.color, markersize=8, markeredgecolor='none')
            axarr.set_autoscale_on(True)
            axarr.set_xlim([-10, 10000])
            axarr.set_xscale('log', nonposx='clip')
            axarr.set_yscale('log', nonposx='clip')
            axarr.set_ylabel("IGD")

            print problem[-1].name, algorithm.name, gtechnique.__name__, results[algorithm.name][gtechnique.__name__]

    f.suptitle(problem[-1].name)
    fignum = len([name for name in os.listdir('./Results/Charts/' + date_folder_prefix)]) + 1
    plt.legend(frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.025), fancybox=True, ncol=2)
    plt.savefig('./Results/Charts/' + date_folder_prefix + '/figure' + str(
    "%02d" % fignum) + "_" + problem[-1].name + "_" + tag + '.png', dpi=100)
    plt.cla()


    print "Processed: ", problem[-1].name

