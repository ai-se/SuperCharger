def func_eval_numbers(problems, algorithms, gtechniques, Configurations):
    raw_folder_name = "Results/Tables/03-30-2016/"
    from os import listdir
    files = listdir(raw_folder_name)
    for problem in problems:
        for algorithm in algorithms:
            for gtechnique in gtechniques:
                foldername = "./RawData/PopulationArchives/" + algorithm.name + "_" + problem.name + "_" + gtechnique.__name__ + "/"
                possible_files =  [file for file in files if (problem.name in file and algorithm.name in file and "raw_table" in file)]
                assert(len(possible_files) == 1), "something is wrong. you can't have more than 1 matching file"
                raw_file_name =  [file for file in files if (problem.name in file and algorithm.name in file and "raw_table" in file)][-1]
                evals = {}
                average_number = [0]
                for repeat in xrange(Configurations["Universal"]["Repeats"]): evals[str(repeat)] = [0]
                for gen in xrange(Configurations["Universal"]["No_of_Generations"]):
                    for repeat in xrange(Configurations["Universal"]["Repeats"]):
                        final_name = foldername + str(repeat) + "/"
                        filename = final_name + str(gen+1) + ".txt"
                        num_lines = sum(1 for _ in open(filename))
                        # making it cumulative
                        evals[str(repeat)].append(evals[str(repeat)][-1] + num_lines)

                    from numpy import mean
                    average_number.append(mean([evals[key][-1] for key in evals.keys()]))
                # print average_number, len(average_number)
                import pandas as pd
                import numpy as np
                output_folder = "Supercharger_post_process/Results_evals/"
                csv_input = pd.read_csv(output_folder + raw_file_name)
                # print csv_input.shape[0]
                csv_input["evals_"+gtechnique.__name__] = average_number
                csv_input.to_csv(output_folder + raw_file_name, index=False)
                print problem.name, algorithm.name, gtechnique.__name__#, [round(a, 3) for a in average_number]



