folders = ["Charts/", "Final_Frontier/", "Tables/", "Approx_HyperVolume"]
parent = "Results/"
for folder in folders:
    filepath = parent + folder
    from os import system
    system("rm -rf " + filepath + "*")
