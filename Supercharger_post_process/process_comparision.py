from __future__ import division

import matplotlib.pyplot as plt

algorithms = ["NSGAII", "SPEA2", "GALE"]
problems = ["POM3A", "POM3B", "POM3C", "POM3D", "xomo_ground", "xomo_flight", "xomo_all",
            "xomoo2", "xomo_osp"]

from os import listdir
import pandas as pd

files = ["./Data_evals/" + file for file in listdir("./Data_evals/")]
for problem in problems:
    print problem,
    scores = {}
    dfs = []
    temp_files = []
    for algorithm in algorithms:
        scores[algorithm] = {}
        temp_files.extend([file for file in files if (problem in file and algorithm in file and "raw_table" in file)])
        dfs.append(pd.read_csv(temp_files[-1]))
    for pname in ["s_hv_median", "s_spread_median", "s_igd_median"]:
    # for pname in ["s_igd_median"]:
        print pname,
        _temp_df = pd.concat([dfs[0][pname], dfs[1][pname], dfs[2][pname]], axis=1, keys=['NSGAII', 'SPEA2', "GALE"])
        epname = "evals_standard_random"
        _eval_temp_df = pd.concat([dfs[0][epname], dfs[1][epname], dfs[2][epname]], axis=1, keys=['eNSGAII', 'eSPEA2', "eGALE"])

        for algorithm in ['NSGAII', 'SPEA2']:
            compare_values = _temp_df[algorithm].tolist()
            gale_values = _temp_df['GALE'].tolist()

            compare_evals = _eval_temp_df["e" + algorithm].tolist()
            gale_evals = _eval_temp_df["eGALE"].tolist()
            budget = 0

            for i, aval in enumerate(compare_values):
                max_val = 0
                for j, gval in enumerate(gale_values):
                    if pname != "s_hv_median":
                        if aval > gval:
                            max_val=j
                    else:
                        if aval < gval:
                            max_val=j



                if max_val != 0:
                    budget = compare_evals[i]
                    # print i, compare_evals[i], max_val, gale_evals[max_val], compare_values[i], gale_values[j]
                else:
                    break

            print  budget,
    print


        # temp_df = pd.DataFrame()
        # temp_df["NSGAII_R"] = (_temp_df["NSGAII"] * 100)/_temp_df["GALE"]
        # temp_df["SPEA2_R"] = (_temp_df["SPEA2"] *100)/_temp_df["GALE"]
        # filename = problem + "_" + pname
        # temp_df.to_csv("./Results/" + filename + ".csv")
        # temp_df.plot()
        # plt.xlabel("Generation")
        # plt.ylabel("Score")
        # plt.title(pname)
        # plt.savefig("./RGraphs/" + filename +".png")
        #


