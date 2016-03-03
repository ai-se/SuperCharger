# since gale0 has only one generation, repeat the same file 20 times
def repeat_20_times(filename):
    filename += "/1.txt"
    foldername = "/".join(filename.strip().split("/")[:-1])
    extenstion = filename.strip().split("/")[-1].split(".")[-1]
    new_filenames = [str(i+1) for i in xrange(1, 20)]

    for new_filename in new_filenames:
        nfn = foldername + "/" + new_filename + "." + extenstion
        cmd = "cp " + filename + " " + nfn
        from os import system
        system(cmd)
    print "Finished for ", foldername


def driver_repeat_20_times():
    path = "/Users/viveknair/GIT/why_GALE_-really-_works/RawData/PopulationArchives"
    from os import listdir

    filter1 = lambda x: "GALE0" in x
    map1 = lambda x: path + "/" + x
    filter2 = lambda x: len(listdir(x)) == 1
    list_of_dirs = filter(filter1, listdir(path))
    list_of_dirs = map(map1, list_of_dirs)
    print len(list_of_dirs)
    list_of_dirs = [list_of_dirs[i] + "/" + f for i, folder in enumerate(list_of_dirs) for f in listdir(folder)]
    print len(list_of_dirs)
    list_of_dirs = filter(filter2, list_of_dirs)

    map(lambda x: repeat_20_times(x), list_of_dirs)



if __name__ == "__main__":
    driver_repeat_20_times()