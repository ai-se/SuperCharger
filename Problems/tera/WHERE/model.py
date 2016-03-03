import os
class Model:
    def __init__(self,name):
        self.name = name
        if name == 'XOMO':
            self.model = Xomo(model = 'flight')
        elif name == 'xomoflight':
            self.model = Xomo(model='flight')
        elif name == 'xomoground':
            self.model = Xomo(model='ground')
        elif name == 'xomoosp':
            self.model = Xomo(model='osp')
        elif name == 'xomoosp2':
            self.model = Xomo(model='osp2')
        elif name == 'xomoall':
            self.model = Xomo(model='all')
        else:
            sys.stderr.write("Enter valid model name _POM3 or xomoflight --> XOMO[flight/ground/osp/osp2/all]\n")
            sys.exit()
    
    def trials(self,N,verbose=True):
        #returns headers and rows
        return self.model.trials(N,verbose)

    def oo(self, verbose=False):
        #pdb.set_trace()
        return self.model.c

    def update(self,fea,cond,thresh):
        #cond is true when <=
        self.model.update(fea,cond,thresh)

    def __repr__(self):
        return self.name

# class Xomo:
#     def __init__(self,
#                  out=os.environ["HOME"]+"/GIT/Courses/Misc/Seive/XOMO/data",
#                  data = "data",
#                  model=None):
#         def theModel(model):
#             #default model is flight
#             if not model:
#                 model = "flight"
#             return model
#         self.collection = {}
#         self.model = theModel(model)
#         self.c = Cocomo("XOMO/"+data+"/"+self.model)
#         self.out = out + "/" + self.model + ".csv"
#         self.data = data
#         self.names = ["aa", "sced", "cplx", "site", "resl", "acap",
#                       "etat", "rely","data", "prec", "pmat", "aexp",
#                       "flex", "pcon", "tool", "time","stor", "docu",
#                       "b", "plex", "pcap", "kloc", "ltex", "pr",
#                       "ruse", "team", "pvol"]
#         #LOWs and UPs are defined in data/* files according to models
#
#         for _n,n in enumerate(self.names):
#             self.collection[n] = Attr(n)
#             k = filter(lambda x: x.txt == n,self.c.about())[0]
#             self.collection[n].update(k.min,k.max)
#
#     def update(self,fea,cond,thresh):
#         def applydiffs(c,col,m,thresh,verbose):
#             k = filter(lambda x: x.txt == col,c.about())[0]
#             if verbose: print k.txt,k.min,k.max,">before"
#             if m == "max":
#                 max = thresh
#                 k.update(k.min,max,m=c)
#             elif m == "min":
#                 min = thresh
#                 k.update(min,k.max,m=c)
#             if verbose: print k.txt, k.min, k.max,">after"
#         if cond:
#             self.collection[fea].up = thresh
#             applydiffs(self.c,fea,'max',thresh)
#         else:
#             self.collection[fea].low = thresh
#             applydiffs(self.c,fea,'min',thresh)
#
#     def trials(self,N,verbose=True):
#         print len(self.names)
#         for _n,n in enumerate(self.names):
#             k = filter(lambda x: x.txt == n,self.c.about())[0]
#             print k
#             if verbose: print k.txt,k.min,k.max,">before"
#             k.update(self.collection[n].low,
#                      self.collection[n].up,
#                      m=self.c)
#             if verbose: print k.txt, k.min, k.max,">after"
#             if verbose:
#                 print "Sample of 5"
#                 for _ in range(5):
#                     print n, self.c.xys()[0][n]
#         self.c.xys(verbose=False)
#         header,rows = self.c.trials(n=N,out=self.out,verbose=False,write=False)
#         return header,rows

#Generic Attribute class to implement in all models
class Attr:
    def __init__(self,name):
        self.name = name
        self.up = 0
        self.low = 0
    
    def update(self,low,up):
        self.low = low
        self.up = up
    
    def __repr__(self):
        s = str(self.low)+' < '+self.name +' < '+str(self.up)+'\n'
        return s
