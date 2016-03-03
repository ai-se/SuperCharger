import csv
from sklearn import tree
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import sys, os, inspect
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem
parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../Techniques")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)
from SMOTE import smote



def avg(lst):
    return sum(lst)/float(len(lst))

class Abcd:
    def __init__(i,db="all",rx="all"):
        i.db = db; i.rx=rx;
        i.yes = i.no = 0
        i.known = {}; i.a= {}; i.b= {}; i.c= {}; i.d= {}
        global The
    def __call__(i,actual=None,predicted=None):
        return i.keep(actual,predicted)
    def tell(i,actual,predict):
        i.knowns(actual)
        i.knowns(predict)
        if actual == predict: i.yes += 1
        else                :  i.no += 1
        for x in  i.known:
            if actual == x:
                if  predict == actual: i.d[x] += 1
                else                 : i.b[x] += 1
            else:
                if  predict == x     : i.c[x] += 1
                else                 : i.a[x] += 1
    def knowns(i,x):
        if not x in i.known:
            i.known[x]= i.a[x]= i.b[x]= i.c[x]= i.d[x]= 0.0
        i.known[x] += 1
        if (i.known[x] == 1):
            i.a[x] = i.yes + i.no
    def header(i):

        if False:
            print "#",('{0:10s} {1:11s}  {2:4s}  {3:4s} {4:4s} '+ \
                       '{5:4s}{6:4s} {7:3s} {8:3s} {9:3s} '+ \
                       '{10:3s} {11:3s}{12:3s}{13:10s}').format(
                "db", "rx",
                "n", "a","b","c","d","acc","pd","pf","prec",
                "f","g","class")
            print '-'*100

    def ask(i):
        def p(y) : return int(100*y + 0.5)
        def n(y) : return int(y)
        def auto(x):
            try:
                return str(x)
            except ValueError:
                return x
        pd = pf = pn = prec = g = f = acc = 0
        scores = []
        for x in i.known:
            a= i.a[x]; b= i.b[x]; c= i.c[x]; d= i.d[x]
            if (b+d)    : pd   = d     / (b+d)
            if (a+c)    : pf   = c     / (a+c)
            if (a+c)    : pn   = (b+d) / (a+c)
            if (c+d)    : prec = d     / (c+d)
            if (1-pf+pd): g    = 2*(1-pf)*pd / (1-pf+pd)
            if (prec+pd): f    = 2*prec*pd/(prec+pd)
            if (a+b+c+d): acc=float(a+d)/(a+b+c+d)
            if False:
                print "#",('{0:10s} {1:10s} {2:4d} {3:4d} {4:4d} '+ \
                           '{5:4d} {6:4d} {7:4d} {8:3d} {9:3d} '+ \
                           '{10:3d} {11:3d} {12:3d} {13:10s}').format(i.db,
                                                                      i.rx,  n(b + d), n(a), n(b),n(c), n(d),
                                                                      p(acc), p(pd), p(pf), p(prec), p(f), p(g),auto(x))

            # Here the flag control the output that needs to be sent back

            if jmoo_preprocessor.PDPF or jmoo_preprocessor.PD or jmoo_preprocessor.PF or jmoo_preprocessor.PREC or jmoo_preprocessor.PFPREC or jmoo_preprocessor.PDPREC:
                scores += [[p(pd), p(pf), p(prec)]]  # e.g:[[100, 100, 74, 0], [0, 0, 74, 0]]
            elif jmoo_preprocessor.ABCD:
                scores += [[p(pd), p(pf), p(prec), a, b, c, d]]
            elif jmoo_preprocessor.GF:
                scores += [[p(pd), p(pf), p(prec), p(g), p(f)]]
            elif jmoo_preprocessor.ACC:
                scores += [[p(pd), p(pf), p(prec), p(acc)]]
        return scores

def _Abcd(predicted, actual, threshold):
    predicted_txt = []
    abcd = Abcd(db='Training', rx='Testing')

    # for i,j in zip(predicted,actual):
    #     print i,j

    def isDef(x):
        return "Defective" if x >= threshold else "Non-Defective"
    for data in predicted:
        predicted_txt +=[isDef(data)]
    for act, pre in zip(actual, predicted_txt):
        abcd.tell(act, pre)
    abcd.header()
    score = abcd.ask()
    return score[-1]


def weitransform(list, threshold):
    result = []
    for l in list:
        if l > threshold: result.append("Defective")
        else: result.append("Non-Defective")
    return result




tera_decisions= [jmoo_decision("min_samples_split", 2, 20),
                  jmoo_decision("min_samples_leaf", 1, 20),
                  jmoo_decision("max_features", 0.05, 1),
                  jmoo_decision("max_depth", 1, 50),
                  jmoo_decision("threshold", 0, 1)
                  ]

def get_tera_objectives():
    if jmoo_preprocessor.PDPFPREC is True:
        print "1"
        tera_objectives = [jmoo_objective("pd", False),
                           jmoo_objective("pf", True),
                           jmoo_objective("prec", False),]
    elif jmoo_preprocessor.ABCD is True:
        print "1"
        tera_objectives = [jmoo_objective("a", False),
                           jmoo_objective("b", True),
                           jmoo_objective("c", True),
                           jmoo_objective("d", False),]
    elif jmoo_preprocessor.GF is True:
        print "1"
        tera_objectives = [jmoo_objective("g", False),
                           jmoo_objective("f", False),]

    elif jmoo_preprocessor.ACC is True:
        print "1"
        tera_objectives = [jmoo_objective("acc", False)]

    elif jmoo_preprocessor.PD is True:
        print "Objective PD activated"
        tera_objectives = [jmoo_objective("pd", False)]


    elif jmoo_preprocessor.PF is True:
        print "Objective PF activated"
        tera_objectives = [jmoo_objective("pf", True)]
        import time
        time.sleep(3)

    elif jmoo_preprocessor.PREC is True:
        print "Objective PREC activated"
        tera_objectives = [jmoo_objective("prec", False)]

    elif jmoo_preprocessor.PDPF is True:
        print "Objective PDPF activated"
        tera_objectives = [jmoo_objective("pd", False),
                           jmoo_objective("pf", True)]

    elif jmoo_preprocessor.PDPREC is True:
        print "Objective PDPREC activated"
        tera_objectives = [jmoo_objective("pd", False),
                           jmoo_objective("prec", False)]

    elif jmoo_preprocessor.PFPREC is True:
        print "Objective PFPREC activated"
        tera_objectives = [jmoo_objective("pf", True),
                           jmoo_objective("prec", False)]

    return tera_objectives



def readSmoteDataset(file, properties):
    prefix = "Tera/"
    suffix = ".csv"
    finput = open(prefix + file + suffix, 'rb')
    reader = csv.reader(finput, delimiter=',')
    dataread = smote(reader)
    return np.array(dataread[0]), dataread[-1]  # keeping the same format as Joe's code


def readDataset(file, properties):
    prefix = "Tera/"
    suffix = ".csv"
    finput = open(prefix + file + suffix, 'rb')
    reader = csv.reader(finput, delimiter=',')

    dataread = []
    try:
        k = properties.unusual_range_end
    except:
        k = 3
    for i,row in enumerate(reader):
        if i > 0: #ignore header row
            line = []
            for item in row[k:]:
                try:
                    line.append(float(item))
                except:
                    pass
            dataread.append(np.array(line))
    properties = row[:k]
    # print properties
    return np.array(dataread), properties

def evaluator(input, properties):

    # print input
    # print "Length: ", len(input)


    if properties.type != "default":
        mss = int(round(input[0]))
        msl = int(round(input[1]))
        mxf = float(input[2])
        md = int(input[3])
        threshold = float(input[4])
    else:
        threshold = 0.5

    assert(len(properties.training_dataset) == 1), "didn't assume"

    # Check whether SMOTE need to be used or not. Note that this has only been
    # applied to the training dataset
    if jmoo_preprocessor.SMOTE is True and properties.type != "default":
        data_train = readSmoteDataset(properties.training_dataset[0], properties)
        # print data_train
    else:
        data_train = readDataset(properties.training_dataset[0], properties)

    data_test = readDataset(properties.test_dataset, properties)


    #train the learner
    indep = np.array(map(lambda x: np.array(x[:-1]), data_train[0]))
    dep   = np.array(map(lambda x: np.array(x[-1:]), data_train[0]))


    from sklearn.tree import DecisionTreeRegressor
    if properties.type == "default":
        clf = DecisionTreeRegressor()
    else:  # random_state has been set so that we can always reproduce the experiments
        clf = DecisionTreeRegressor(max_features=mxf, min_samples_split=mss, min_samples_leaf=msl, random_state= 1, max_depth= md)
    clf.fit(indep, dep)

    #test the learner
    test_indep = np.array(map(lambda x: np.array(x[:-1]), data_test[0]))
    test_dep   = np.array(map(lambda x: np.array(x[-1:]), data_test[0]))
    t = clf.predict(test_indep)

    result = [i for i in t]
    result = [float(x) for x in result]

    output = _Abcd(result, weitransform(test_dep, 0), threshold)

    if jmoo_preprocessor.PDPFPREC:
        print [o for o in output]
        return output[:3]
    elif jmoo_preprocessor.ABCD:
        print [o for o in output[-4:]]
        return output[:3]
    elif jmoo_preprocessor.GF:
        print [o for o in output[-3:]]
        return output[:3]
    elif jmoo_preprocessor.ACC:
        print [o for o in output[-1:]]
        return output[:3]
    elif jmoo_preprocessor.PD:
        return [output[0]]
    elif jmoo_preprocessor.PF:
        return [output[1]]
    elif jmoo_preprocessor.PREC:
        return [output[2]]
    elif jmoo_preprocessor.PDPF:
        return [output[0], output[1]]
    elif jmoo_preprocessor.PFPREC:
        return [output[1], output[2]]
    elif jmoo_preprocessor.PDPREC:
        return [output[0], output[2]]
    elif jmoo_preprocessor.PDPFPREC:
        return [output[0], output[1], output[2]]


class Properties:
    def __init__(self, name, test_file, train_file, type="Test"):
        self.dataset_name = name
        self.training_dataset = train_file
        self.test_dataset = test_file
        self.type = type

    def __str__(self):
        return self.dataset_name + str(self.training_dataset)


class xalan(jmoo_problem):
    def __init__(prob):
        prob.name = "Xalan"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, "xalan-2.5", ["xalan-2.4"])
        prob.training = "xalan-2.4"
        prob.tuning = "xalan-2.5"
        prob.testing = "xalan-2.6"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "xalan-2.6", ["xalan-2.4"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "xalan-2.6", ["xalan-2.4"], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints
    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name
#ant

class xerces(jmoo_problem):
    def __init__(prob):
        prob.name = "xerces"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "xerces-1.3", ["xerces-1.2"])
        prob.training = "xerces-1.2"
        prob.tuning = "xerces-1.3"
        prob.testing = "xerces-1.4"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints


    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "xerces-1.4", ["xerces-1.2"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "xerces-1.4", ["xerces-1.2"], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name

class velocity(jmoo_problem):
    def __init__(prob):
        prob.name = "Velocity"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "velocity-1.5", ["velocity-1.4"])
        prob.training = "velocity-1.4"
        prob.tuning = "velocity-1.5"
        prob.testing = "velocity-1.6"

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "velocity-1.6", ["velocity-1.4"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "velocity-1.6", ["velocity-1.4"], type="default"))
        return output[:3]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name


class synapse(jmoo_problem):
    def __init__(prob):
        prob.name = "synapse"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "synapse-1.1", ["synapse-1.0"])
        prob.training = "synapse-1.0"
        prob.tuning = "synapse-1.1"
        prob.testing = "synapse-1.2"

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "synapse-1.2", ["synapse-1.0"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "synapse-1.2", ["synapse-1.0"], type="default"))
        return output[:3]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name


class poi(jmoo_problem):
    def __init__(prob):
        prob.name = "poi"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "poi-2.0", ["poi-1.5"])
        prob.training = "poi-1.5"
        prob.tuning = "poi-2.0"
        prob.testing = "poi-2.5"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob,input = None):
        return False #no constraints

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "poi-2.5", ["poi-1.5"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "poi-2.5", ["poi-1.5"], type="default"))
        return output[:3]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name

class lucene(jmoo_problem):
    def __init__(prob):
        prob.name = "lucene"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "lucene-2.2", ["lucene-2.0"])
        prob.training = "lucene-2.0"
        prob.tuning = "lucene-2.2"
        prob.testing = "lucene-2.4"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "lucene-2.4", ["lucene-2.0"]))
        print "# Evaluator: -------------> SCORES", output
        return output

    def default(prob):
        output = evaluator(input, Properties(prob.name, "lucene-2.4", ["lucene-2.0"], type="default"))
        return output[:3]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name

class jedit(jmoo_problem):
    def __init__(prob):
        prob.name = "jedit"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "jedit-4.0", ["jedit-3.2"])
        prob.training = "jedit-3.2"
        prob.tuning = "jedit-4.0"
        prob.testing = "jedit-4.1"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "jedit-4.1", ["jedit-3.2"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "jedit-4.1", ["jedit-3.2"], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints
    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name

class ivy(jmoo_problem):
    def __init__(prob):
        prob.name = "ivy"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "ivy-1.4", ["ivy-1.1"])
        prob.training = "ivy-1.1"
        prob.tuning = "ivy-1.4"
        prob.testing = "ivy-2.0"
    # Just returns what is required. Not extra stuff
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "ivy-2.0", ["ivy-1.1"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "ivy-2.0", ["ivy-1.1"], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name



class forrest(jmoo_problem):
    def __init__(prob):
        prob.name = "forrest"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "forrest-0.7", [ "forrest-0.6"])
        prob.training = "forrest-0.6"
        prob.tuning = "forrest-0.7"
        prob.testing = "forrest-0.8"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "forrest-0.8", ["forrest-0.6"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "forrest-0.8", ["forrest-0.6"], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name


class ant(jmoo_problem):
    def __init__(prob):
        prob.name = "ant"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "ant-1.4", ["ant-1.3"])
        prob.training = "ant-1.3"
        prob.tuning = "ant-1.4"
        prob.testing = "ant-1.5"

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "ant-1.5", ["ant-1.3"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "ant-1.5", ["ant-1.3"], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints

    def change_objective(prob):
        # print "."*100
        # # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name



class camel(jmoo_problem):
    def __init__(prob):
        prob.name = "camel"
        prob.decisions = tera_decisions
        prob.objectives = get_tera_objectives()
        prob.properties = Properties(prob.name, "camel-1.2", ["camel-1.0"])
        prob.training = "camel-1.0"
        prob.tuning = "camel-1.2"
        prob.testing = "camel-1.4"

    # Just returns what is required. Not extra stuff
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        assert(len(output) == len(prob.objectives)), "Output and Objectives are not same"
        for i,j in zip(prob.objectives, output):
            i.value = j

        return [objective.value for objective in prob.objectives]

    # Returns the PDPF
    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, "camel-1.4", ["camel-1.0"]))
        print "# Evaluator: -------------> SCORES", output
        return output


    def default(prob):
        output = evaluator(input, Properties(prob.name, "camel-1.4", ["camel-1.0"], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints
    def change_objective(prob):
        print "."*100
        # print "CHNAGE CALLED", jmoo_preprocessor.PF, jmoo_preprocessor.PD
        prob.objectives = get_tera_objectives()
#        for o in prob.objectives:
#            print "Objective name: ", o.name

