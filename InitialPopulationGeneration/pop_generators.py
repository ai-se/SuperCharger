
def standard_random(problem, n):
    dataset = []
    for run in range(n): dataset.append(problem.generateInput(center=False))
    return dataset