from __future__ import division
from os import listdir
import pandas as pd

foldername = "./Data_evals/"
problems = ["POM3C"]
algorithms = ["NSGAII", "SPEA2", "GALE"]

for problem in problems:
    for algorithm in algorithms:
        files = listdir(foldername)
        filename = [file for file in files if (problem in file and algorithm in file and "raw_table" in file)][-1]

        df = pd.read_csv(filename)


        import pdb
        pdb.set_trace()