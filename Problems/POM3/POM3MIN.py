from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem
from Helper.pom3 import pom3


class POM3MIN(jmoo_problem):
    "POM3D"

    def __init__(prob):
        prob.name = "POM3MIN"
        names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", "Inter-Dependency", "Dynamism",
                 "Size", "Plan", "Team Size"]
        LOWS = [0.80, 1.22, 2, 0.60, 0, 1, 0, 0, 1]
        UPS = [0.90, 1.62, 6, 0.62, 2, 3, 1, 1, 3]
        prob.decisions = [jmoo_decision(names[i], LOWS[i], UPS[i]) for i in range(len(names))]
        prob.objectives = [jmoo_objective("Cost", True), jmoo_objective("Score", False),
                           jmoo_objective("Completion", False), jmoo_objective("Idle", True)]

    def evaluate(prob, input=None):
        if input:
            for i, decision in enumerate(prob.decisions):
                decision.value = input[i]
        else:
            input = [decision.value for decision in prob.decisions]
        p3 = pom3()
        output = p3.simulate(input)
        for i, objective in enumerate(prob.objectives):
            objective.value = output[i]
        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob):
        return False  # no constraints
