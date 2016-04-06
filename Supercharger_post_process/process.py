from __future__ import division

import matplotlib.pyplot as plt

algorithms = ["NSGAII", "SPEA2", "GALE"]
problems = ["POM3A", "POM3B", "POM3C", "POM3D", "xomo_ground", "xomo_flight", "xomo_all", "xomoo2", "xomo_osp"]

from os import listdir
import pandas as pd

files = ["./Data/" + file for file in listdir("./Data/")]
for problem in problems:
    scores = {}
    dfs = []
    temp_files = []
    for algorithm in algorithms:
        scores[algorithm] = {}
        temp_files.extend([file for file in files if (problem in file and algorithm in file and "raw_table" in file)])
        dfs.append(pd.read_csv(temp_files[-1]))
    for pname in ["s_igd_median", "s_hv_median", "s_spread_median"]:
        _temp_df = pd.concat([dfs[0][pname], dfs[1][pname], dfs[2][pname]], axis=1, keys=['NSGAII', 'SPEA2', "GALE"])
        temp_df = pd.DataFrame()
        temp_df["NSGAII_R"] = (_temp_df["NSGAII"] * 100)/_temp_df["GALE"]
        temp_df["SPEA2_R"] = (_temp_df["SPEA2"] *100)/_temp_df["GALE"]
        filename = problem + "_" + pname
        temp_df.to_csv("./Results/" + filename + ".csv")
        temp_df.plot()
        plt.xlabel("Generation")
        plt.ylabel("Score")
        plt.title(pname)
        plt.savefig("./RGraphs/" + filename +".png")



