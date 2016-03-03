import unittest
from os.path import realpath, abspath, split, join
from inspect import currentframe, getfile
from sys import path

from nsgaiii_components import two_level_weight_vector_generator, nsgaiii_regenerate, nsgaiii_recombine

cmd_subfolder = realpath(abspath(join(split(getfile(currentframe()))[0], "../..")))
if cmd_subfolder not in path: path.insert(0, cmd_subfolder)
from jmoo_problems import initialPopulation, dtlz1
from jmoo_properties import MU

problem = dtlz1(6, 2)
initialPopulation(problem, MU, "unittesting")
population = problem.loadInitialPopulation(MU, "unittesting")


class two_level_weight_vector_generator_TestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test1(self):
        self.assertTrue(len(two_level_weight_vector_generator([3, 2], 8)) == 156)

    def test2(self):
        self.assertTrue(len(two_level_weight_vector_generator([3, 2], 10)) == 275)

    def test3(self):
        self.assertTrue(len(two_level_weight_vector_generator([2, 1], 15)) == 135)


class nsgaiii_regenerate_TestCase(unittest.TestCase):
    def test1(self):
        global population
        population, evaluation = nsgaiii_regenerate(problem, population)
        self.assertTrue(len(population) == MU)

    def test2(self):
        global population
        population, evaluation = nsgaiii_regenerate(problem, population)
        test_population = [True if pop.valid is not None else False for pop in population]
        test_population = reduce(lambda x, y: x and y, test_population)
        self.assertTrue(test_population is True)

    def test3(self):
        global population
        population, evaluation = nsgaiii_regenerate(problem, population)
        self.assertTrue(evaluation == len(population))


class two_level_weight_vector_generator_TestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test1(self):
        self.assertTrue(len(two_level_weight_vector_generator([3, 2], 8)) == 156)

    def test2(self):
        self.assertTrue(len(two_level_weight_vector_generator([3, 2], 10)) == 275)

    def test3(self):
        self.assertTrue(len(two_level_weight_vector_generator([2, 1], 15)) == 135)


class nsgaiii_recombine_TestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test1(self):
        nsgaiii_recombine(problem, population, population, MU)



if __name__ == '__main__':
    unittest.main()
