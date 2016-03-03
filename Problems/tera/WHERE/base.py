from __future__ import division
import sys
import random
import math
import datetime
import time
import re
import pdb

sys.dont_write_bytecode = True


class Options:

  def __init__(i, **d):
    i.__dict__.update(d)

# Settings = Options(de=Options(np=20,
#                               repeats=1000,
#                               f=0.75,
#                               cr=0.85,
#                               threshold=0.0001,
#                               limit=Options(infoPrune = 1, 
#                                             dTreeMin = 1,
#                                             threshold = 1,
#                                             whereMinSize  = 1,    # min leaf size, percentage
#                                             whereDepthMin= 2,      # no pruning till this depth
#                                             wehreDepthMax= 20,     # max tree depth
#                                             whereWriggle = 0.2,    # min difference of 'better'
#                                             wherePrune   = True,   # pruning enabled?
#                                            ),
#                               life=5,
#                               k = 0,
#                               run = 20
#                               ))


Settings = Options(de=Options(np=10,
                              repeats=1000,
                              f=0.75,
                              cr=0.3,
                              threshold=0.0001,
                              limit=[1,10,1,1,20,6,1],
                              #infoPrune, minSize, threshold, wriggle, depthMax, depthMin, treeMin, treeprune, whereprune
                              cartLimit_Max = [1, 50, 20, 20, 1000, 100],
                              cartLimit_Min = [0.01, 1, 2, 1, 2,0],
                              # max_features, max_depth, min_samples_split, min_samples_leaf, max_leaf_nodes
                              life=5,
                              k = 0,
                              run = 20
                              ))
