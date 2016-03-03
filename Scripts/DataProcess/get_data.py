# import xml.etree.ElementTree
# e = xml.etree.ElementTree.parse('data.xml').getroot()
# for p in e.findall('Problem'):
#     for atype in p.findall('Algorithm'):
#         for run in atype.findall('Run'):
#             for summ in run.findall('Summary'):
#                 print summ.get('NumEvals')
#         raw_input()


# from xml.dom import minidom
# xmldoc = minidom.parse('data.xml')
# itemlist = xmldoc.getElementsByTagName('Problem')
# print(len(itemlist))
# print(itemlist[0].attributes['Algorithm'].value)
# for s in itemlist:
#     print(s.attributes['name'].value)


data = {}
import bs4 as bs
content = open("data.xml").read()
x = bs.BeautifulSoup(content)
problems = x.findAll('problem')
for problem in problems:
    data[problem["name"]] = {}
    algorithms = problem.findAll('algorithm')
    for algorithm in algorithms:
        runs = [run.summary for run in algorithm.findAll('run')]
        numevals = []

        for run in runs:
            numevals.append(str(run.numevals).replace("<numevals>", "").replace("</numevals>", ""))
        from numpy import mean
        data[problem["name"]][algorithm["name"]] = mean(map(int, numevals))

problems = data.keys()
for problem in problems:
    print problem, ", ",
    algorithms = ["GALE", "NSGAII", "SPEA2"]
    for algorithm in algorithms:
        print round(data[problem][algorithm], 0), ", " ,
    print


