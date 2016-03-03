from mutator import trim
from jmoo_individual import jmoo_individual


def nudge(problem, individual, east, increment, configuration):
    if individual.anyscore == 1e32: return individual
    temp = []
    for i, decision in enumerate(problem.decisions):
        up = decision.up
        low = decision.low
        if east.decisionValues[i] > individual.decisionValues[i] >= 0: weight = + 1
        else: weight = - 1
        mutation = increment % configuration["STORM"]["GAMMA"] * (east.decisionValues[i] - individual.decisionValues[i])
        temp.append(trim(individual.decisionValues[i] + weight * mutation, low, up))
    return jmoo_individual(problem, temp, None)
