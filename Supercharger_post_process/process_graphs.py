from __future__ import division
from os import listdir
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def transform(compare, gale):
    retu = []
    for c, g in zip(compare, gale): retu.append(c*100/g)
    return retu




foldername = "./Data_evals/"
problems = ["POM3C"]
algorithms = ["NSGAII", "SPEA2", "GALE"]

left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

for problem in problems:
    f, (ax1, ax2, ax3) = plt.subplots(1, 3)
    scores = {}
    for pscore in ["s_hv_median", "s_spread_median", "s_igd_median"]:
        scores[pscore] = {}
        for algorithm in algorithms:
            scores[pscore][algorithm] = {}
            scores[pscore][algorithm]["values"] = []
            scores[pscore][algorithm]["evals"] = []

            files = listdir(foldername)
            filename = [file for file in files if (problem in file and algorithm in file and "raw_table" in file)][-1]

            df = pd.read_csv(foldername + filename)

            scores[pscore][algorithm]["values"]= df[pscore].tolist()
            scores[pscore][algorithm]["evals"]= df["evals_standard_random"].tolist()



    import matplotlib.ticker as mtick
    ax1.plot(scores["s_hv_median"]["NSGAII"]["evals"], scores["s_hv_median"]["NSGAII"]["values"], "ko-", color='r')
    ax1.plot(scores["s_hv_median"]["SPEA2"]["evals"], scores["s_hv_median"]["SPEA2"]["values"], "kv-", color='g')
    ax1.plot(scores["s_hv_median"]["GALE"]["evals"], scores["s_hv_median"]["GALE"]["values"], "kx-", color='y')
    ax1.set_xscale("log")
    ax1.set_title("HyperVolume")
    ax1.set_xlabel("Evaluations")
    ax1.set_xlim(0, 13000)
    ax1.set_yticks([82000, 86000, 90000, 94000])
    # ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    # ax1.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))

    ax2.plot(scores["s_spread_median"]["NSGAII"]["evals"], scores["s_spread_median"]["NSGAII"]["values"], "ko-", color='r')
    ax2.plot(scores["s_spread_median"]["SPEA2"]["evals"], scores["s_spread_median"]["SPEA2"]["values"], "kv-", color='g')
    ax2.plot(scores["s_spread_median"]["GALE"]["evals"], scores["s_spread_median"]["GALE"]["values"], "kx-", color='y')
    ax2.set_xscale("log")
    ax2.set_title("Spread")
    ax2.set_xlabel("Evaluations")
    ax2.set_xlim(0, 13000)
    ax2.set_yticks([0.4, 0.6, 0.8, 1.0])
    # ax2.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))

    ax3.plot(scores["s_igd_median"]["NSGAII"]["evals"], scores["s_igd_median"]["NSGAII"]["values"], "ko-", color='r')
    ax3.plot(scores["s_igd_median"]["SPEA2"]["evals"], scores["s_igd_median"]["SPEA2"]["values"], "kv-", color='g')
    ax3.plot(scores["s_igd_median"]["GALE"]["evals"], scores["s_igd_median"]["GALE"]["values"], "kx-", color='y')
    ax3.set_xscale("log")
    ax3.set_title("IGD")
    ax3.set_xlabel("Evaluations")
    ax3.set_xlim(0, 13000)
    ax3.set_yticks([0,60,120,180])
    # ax3.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))


    # plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
    plt.figlegend([ax1.lines[0], ax1.lines[1], ax1.lines[2]], [ "NSGA-II", "SPEA-2","GALE"],
                  frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.035), fancybox=True, ncol=3)

    f.set_size_inches(9, 4)
    f.tight_layout()

    filename_graph = "./Figures/" + problem + ".png"
    plt.savefig(filename_graph)