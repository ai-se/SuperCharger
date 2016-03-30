from Problems.POM3.POM3A import POM3A
from jmoo_properties import Configurations

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
            decisions = map(float, content.strip().split(","))
            objectives.append(decisions + problem.evaluate(decisions))
        import pdb
        pdb.set_trace()
        return ["".join(contents[0])]+[",".join(map(str, o))+"\n" for o in objectives]+["".join(c) for c in contents[population_size+1:]]


def get_initial_datapoints(problem, algorithm, gtechnique, Configurations):
    number_of_objectives = len(problem.objectives)
    pop_size = Configurations["Universal"]["Population_Size"]
    folder_name = "./Data/"
    sep = "_"
    filename = folder_name + problem.name + "-p" + str(
        Configurations["Universal"]["Population_Size"]) + "-d" + str(len(problem.decisions)) + "-o" + str(
        len(problem.objectives)) + "-g" + gtechnique.__name__ + "-dataset.txt"

    print "Initial Points are read from file: ", filename, " Algorithm: ", algorithm.name, " GTechnique: ", gtechnique.__name__

    contents= get_content(problem, filename, pop_size, initial_line=True)
    f = open(filename, "w")
    for content in contents: f.write(content)
    f.close()


def func_modinitpop(problems, Configurations):
    for problem in problems:
        get_initial_datapoints(problem, "ASdsa", "c", Configurations)