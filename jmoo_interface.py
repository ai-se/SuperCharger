
"""
##########################################################
### @Author Joe Krall      ###############################
### @copyright see below   ###############################

    This file is part of JMOO,
    Copyright Joe Krall, 2014.

    JMOO is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JMOO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with JMOO.  If not, see <http://www.gnu.org/licenses/>.
    
###                        ###############################
##########################################################
"""

"Brief notes"
"Command line interface."

from jmoo_properties import *
from jmoo_core import *
from temp_modify_initial_population import func_modinitpop
from eval_numbers import func_eval_numbers
   
"""
------------
Quick Notes
------------

The Main Interface of JMOO.  Run this python script from the commmand line with or without command line arguments.

- The Core behind JMOO is to perform 'tests' and then prepare 'reports' about those tests.
- - A 'test' is a collection of problems and algorithms.  Each algorithm is tested against each problem.

- To define tests (and many other properties), please see jmoo_properties.py
- To define reports, see below in this python script.
"""
   

db = open('what.txt', 'w')
                                

# Process command line arguments.  These modify properties of JMOO.
tag = ""
reportOnly = False
chartOnly = False
binsOnly = False
noReports = True
modinitpop = False
evalnumbers = False
for i,arg in enumerate(sys.argv):
    if arg == "-n" or arg == "-N":
        repeats = sys.argv[i+1]
    if arg == "-NEW" or arg == "-new" or arg == "-New":
        build_new_pop = True
    if arg == "-MU" or arg == "-mu" or arg == "-Mu":
        MU = sys.argv[i+1]
    if arg == "-tag" or arg == "-Tag" or arg == "-TAG":
        tag = sys.argv[i+1]
    if arg == "-reportOnly":
        reportOnly = True
    if arg == "-chartOnly":
        reportOnly = True
        chartOnly = True
    if arg == "-binsOnly":
        binsOnly = True
        reportOnly = True
    if arg == "-modinitpop":
        modinitpop = True
    if arg == "-evalnumbers":
        evalnumbers = True
        
        
# Build new initial populations if suggested.  Before tests can be performed, a problem requires an initial dataset.
if build_new_pop:
    for problem in problems:
        for gtech in GTechniques:
            initialPopulation(problem, gtech, Configurations["Universal"]["Population_Size"])


# Wrap the tests in the jmoo core framework
tests = jmoo_test(problems, algorithms, GTechniques)

if modinitpop is True:func_modinitpop(problems, GTechniques,
                                      Configurations)

if evalnumbers is True: func_eval_numbers(problems, algorithms, GTechniques, Configurations)

# Define the reports
elif chartOnly == True: reports = [jmoo_chart_report(tests, Configurations)]
elif binsOnly: reports = [jmoo_decision_report(tests)]

elif reportOnly: reports = [jmoo_stats_report(tests, Configurations)]
elif noReports: reports = []
else: reports = [jmoo_stats_report(tests), jmoo_decision_report(tests), jmoo_chart_report(tests)]

if modinitpop is False or evalnumbers is False:
    # Associate core with tests and reports
    core = JMOO(tests, reports, Configurations)

    # Perform the tests
    if not reportOnly: core.doTests()

    # Prepare the reports
    core.doReports(tag)