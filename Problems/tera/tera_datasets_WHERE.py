import csv
import sys
import os
import inspect

from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem

parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../..")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)

from WHERE.main import *

prefix = "Tera/"
suffix = ".csv"

def avg(lst):
    return sum(lst)/float(len(lst))

class Abcd:
    def __init__(i,db="all"+ suffix,rx="all"):
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
                "db",prefix +"rx",
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

            if PDPF:
                scores += [[p(pd), p(pf), p(prec)]]  # e.g:[[100, 100, 74, 0], [0, 0, 74, 0]]
            elif ABCD:
                scores += [[p(pd), p(pf), p(prec), a, b, c, d]]
            elif GF:
                scores += [[p(pd), p(pf), p(prec), p(g), p(f)]]
            elif ACC:
                scores += [[p(pd), p(pf), p(prec), p(acc)]]


        return scores

        #print x,p(pd),p(prec)

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
    #abcd.header()
    score = abcd.ask()
    # pdb.set_trace()
    return score[-1]


def weitransform(list, threshold):
    result = []
    for l in list:
        if l > threshold: result.append("Defective")
        else: result.append("Non-Defective")
    return result

tera_decisions = [jmoo_decision("infoPrune", 0, 1),
                  jmoo_decision("min", 0, 10),
                  jmoo_decision("threshold", 0, 1),
                  jmoo_decision("wriggle", 0,1),
                  jmoo_decision("depthMax", 0, 20),
                  jmoo_decision("depthMin", 0, 6),
                  jmoo_decision("optionminsize", 0, 1),
                  jmoo_decision("treeprune", 0, 1),
                  jmoo_decision("whereprune", 0, 1)]



if PDPF:
    tera_objectives = [jmoo_objective("pd", False),
                   jmoo_objective("pf", True),
                   jmoo_objective("prec", False),]
elif ABCD:
    tera_objectives = [jmoo_objective("a", False),
                       jmoo_objective("b", True),
                       jmoo_objective("c", True),
                       jmoo_objective("d", False),]
elif GF:
    tera_objectives = [jmoo_objective("g", False),
                       jmoo_objective("f", False),]

elif ACC:
    tera_objectives = [jmoo_objective("acc", False)]


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
    #print properties
    return np.array(dataread), properties

def evaluator(input, properties):

    if properties.type != "default":
        assert(len(properties.training_dataset) == 1), "didn't assume"
        return Where(input, properties.training_dataset[0], properties.test_dataset)
    else:
        return NaiveWhere(properties.training_dataset[0], properties.test_dataset)


class Properties:
    def __init__(self, name, test_file, train_file, type="Test"):
        self.dataset_name = name
        self.training_dataset = train_file
        self.test_dataset = test_file
        self.type = type

    def __str__(self):
        return self.dataset_name + str(self.training_dataset) + str(self.test_dataset)


class xalanW(jmoo_problem):
    def __init__(prob):
        prob.name = "XalanW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"xalan-2.5"+ suffix, [prefix+"xalan-2.4"+ suffix])
        prob.training = "xalan-2.4"
        prob.tuning = "xalan-2.5"
        prob.testing = "xalan-2.6"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"xalan-2.6"+ suffix, [prefix+"xalan-2.4"+ suffix]))
        return output[:3]

    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"xalan-2.6"+ suffix, [prefix+"xalan-2.4"+ suffix], type="default"))
        return output[:3]
#ant

class xercesW(jmoo_problem):
    def __init__(prob):
        prob.name = "xercesW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"xerces-1.3"+ suffix, [prefix+"xerces-1.2"+ suffix])
        prob.training = "xerces-1.2"
        prob.tuning = "xerces-1.3"
        prob.testing = "xerces-1.4"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob,input = None):
        return False #no constraints


    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"xerces-1.4"+ suffix, [prefix+"xerces-1.2"+ suffix]))
        return output[:3]

    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"xerces-1.4"+ suffix, [prefix+"xerces-1.2"+ suffix], type="default"))
        return output[:3]

class velocityW(jmoo_problem):
    def __init__(prob):
        prob.name = "VelocityW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"velocity-1.5"+ suffix, [prefix+"velocity-1.4"+ suffix])
        prob.training = "velocity-1.4"
        prob.tuning = "velocity-1.5"
        prob.testing = "velocity-1.6"

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"velocity-1.6"+ suffix, [prefix+"velocity-1.4"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]
    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"velocity-1.6"+ suffix, [prefix+"velocity-1.4"+ suffix], type="default"))
        return output[:3]


class synapseW(jmoo_problem):
    def __init__(prob):
        prob.name = "synapseW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"synapse-1.1"+ suffix, [prefix+"synapse-1.0"+ suffix])
        prob.training = "synapse-1.0"
        prob.tuning = "synapse-1.1"
        prob.testing = "synapse-1.2"

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"synapse-1.2"+ suffix, [prefix+"synapse-1.0"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]
    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"synapse-1.2"+ suffix, [prefix+"synapse-1.0"+ suffix], type="default"))
        return output[:3]


class poiW(jmoo_problem):
    def __init__(prob):
        prob.name = "poiW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"poi-2.0"+ suffix, [prefix+"poi-1.5"+ suffix])
        prob.training = "poi-1.5"
        prob.tuning = "poi-2.0"
        prob.testing = "poi-2.5"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]

    def evalConstraints(prob,input = None):
        return False #no constraints

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"poi-2.5"+ suffix, [prefix+"poi-1.5"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]

    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"poi-2.5"+ suffix, [prefix+"poi-1.5"+ suffix], type="default"))
        return output[:3]

class luceneW(jmoo_problem):
    def __init__(prob):
        prob.name = "luceneW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"lucene-2.2"+ suffix, [prefix+"lucene-2.0"+ suffix])
        prob.training = "lucene-2.0"
        prob.tuning = "lucene-2.2"
        prob.testing = "lucene-2.4"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"lucene-2.4"+ suffix, [prefix+"lucene-2.0"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]

    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"lucene-2.4"+ suffix, [prefix+"lucene-2.0"+ suffix], type="default"))
        return output[:3]

class jeditW(jmoo_problem):
    def __init__(prob):
        prob.name = "jeditW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"jedit-4.0"+ suffix, [prefix+"jedit-3.2"+ suffix])
        prob.training = "jedit-3.2"
        prob.tuning = "jedit-4.0"
        prob.testing = "jedit-4.1"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"jedit-4.1"+ suffix, [prefix+"jedit-3.2"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]

    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"jedit-4.1"+ suffix, [prefix+"jedit-3.2"+ suffix], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints

class ivyW(jmoo_problem):
    def __init__(prob):
        prob.name = "ivyW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name,prefix +"ivy-1.4"+ suffix, [prefix+"ivy-1.1"+ suffix])
        prob.training = "ivy-1.1"
        prob.tuning = "ivy-1.4"
        prob.testing = "ivy-2.0"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]
    def evalConstraints(prob,input = None):
        return False #no constraints

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name,prefix +"ivy-2.0"+ suffix, [prefix+"ivy-1.1"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]

    def default(prob):
        output = evaluator(input, Properties(prob.name,prefix +"ivy-2.0"+ suffix, [prefix+"ivy-1.1"+ suffix], type="default"))
        return output[:3]


class forrestW(jmoo_problem):
    def __init__(prob):
        prob.name = "forrestW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, prefix + "forrest-0.7"+ suffix, [ prefix + "forrest-0.6"+ suffix])
        prob.training = "forrest-0.6"
        prob.tuning = "forrest-0.7"
        prob.testing = "forrest-0.8"
    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, prefix + "forrest-0.8"+ suffix, [prefix + "forrest-0.6"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]

    def default(prob):
        output = evaluator(input, Properties(prob.name, prefix + "forrest-0.8"+ suffix, [prefix + "forrest-0.6"+ suffix], type="default"))
        return output[:3]

    def evalConstraints(prob,input = None):
        return False #no constraints

class camelW(jmoo_problem):
    def __init__(prob):
        prob.name = "camelW"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives
        prob.properties = Properties(prob.name, prefix + "camel-1.2"+ suffix, [prefix + "camel-1.0"+ suffix])
        prob.training = "camel-1.0"
        prob.tuning = "camel-1.2"
        prob.testing = "camel-1.4"

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input  = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        return [objective.value for objective in prob.objectives]

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, prefix + "camel-1.4"+ suffix, [prefix +"camel-1.0"+ suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        return output[:3]
    def default(prob):
        output = evaluator(input, Properties(prob.name, prefix + "camel-1.4"+ suffix, [prefix +"camel-1.0"+ suffix], type="default"))
        return output[:3]


    def evalConstraints(prob,input = None):
        return False #no constraints

class antW(jmoo_problem):  # ant 15 is the latest, it can't see anything other than 1.5
    def __init__(prob):
        prob.name = "antW"
        prob.properties = Properties(prob.name, prefix + "ant-1.5" + suffix, [prefix + "ant-1.3" + suffix])
        prob.training = "ant-1.3"
        prob.tuning = "ant-1.4"
        prob.testing = "ant-1.5"
        prob.decisions = tera_decisions
        prob.objectives = tera_objectives

    def evaluate(prob, input = None):
        if input:
            for i,decision in enumerate(prob.decisions):
                decision.value = input[i]
        input = [decision.value for decision in prob.decisions]
        output = evaluator(input, prob.properties)
        print output
        if PDPF:
            prob.objectives[0].value = output[0]
            prob.objectives[1].value = output[1]
            prob.objectives[2].value = output[2]
        elif ABCD:
            prob.objectives[0].value = output[-4]
            prob.objectives[1].value = output[-3]
            prob.objectives[2].value = output[-2]
            prob.objectives[3].value = output[-1]
        elif GF:
            prob.objectives[0].value = output[-2]
            prob.objectives[1].value = output[-1]
        elif ACC:
            prob.objectives[0].value = output[-1]

        return [objective.value for objective in prob.objectives]

    def test(prob, input=None):
        if input is None:
            print "input parameter required"
            exit()
        output = evaluator(input, Properties(prob.name, prefix + "ant-1.5" + suffix, [prefix + "ant-1.3" + suffix]))
        if PDPF:
            print [o for o in output]
        elif ABCD:
            print [o for o in output[-4:]]
        elif GF:
            print [o for o in output[-3:]]
        elif ACC:
            print [o for o in output[-1:]]
        return output[:3]
    def default(prob):
        output = evaluator(input, Properties(prob.name, prefix + "ant-1.5" + suffix, [prefix + "ant-1.3" + suffix], type="default"))
        return output[:3]



    def evalConstraints(prob,input = None):
        return False  # no constraints