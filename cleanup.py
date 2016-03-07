folders = ["Charts/", "Final_Frontier/", "Tables/", "Approx_HyperVolume"]
parent = "Results/"
for folder in folders:
    filepath = parent + folder
    from os import system
    system("rm -rf " + filepath + "*")


# folders = ["ExperimentalRecords/", "PopulationArchives/"]
# parent = "RawData/"
# for folder in folders:
#     filepath = parent + folder
#     from os import system
#     system("rm -rf " + filepath + "*")
#
#
# parent = "Data/"
# filepath = parent
# from os import system
# system("rm -rf " + filepath + "*")