
import random, os, inspect, sys


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from jmoo_individual import jmoo_individual


def three_others(individuals, one):
    seen = [one]

    def other():
        while True:
            random_selection = random.randint(0, len(individuals) - 1)
            if individuals[random_selection] not in seen:
                seen.append(individuals[random_selection])
                break
        return individuals[random_selection]

    return other(), other(), other()

def trim(mutated, low, up):
    return max(low, min(mutated, up))

def extrapolate(problem, individuals, one, f, cf):
    two, three, four = three_others(individuals, one)
    solution = []
    for d, decision in enumerate(problem.decisions):
        x, y, z = two.decisionValues[d], three.decisionValues[d], four.decisionValues[d]
        if random.random() < cf:
            mutated = x + f * (y - z)
            solution.append(trim(mutated, decision.low, decision.up))
        else:
            solution.append(one.decisionValues[d])

    return jmoo_individual(problem, [float(d) for d in solution], None)