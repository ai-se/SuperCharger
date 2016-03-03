data = {}
data["ground"] = {}
data["ground"]["GALE"]={"evals":100}
data["ground"]["NSGAII"]={"evals":2817}
data["ground"]["SPEA2"]={"evals":2725}
data["ground"]["GALE_NM"]={"evals":14}
data["ground"]["GALE_LP"]={"evals":49}
data["ground"]["GALE_LPI"]={"evals":49}
data["POM3D"] = {}
data["POM3D"]["GALE"]={"evals":100}
data["POM3D"]["NSGAII"]={"evals":2105}
data["POM3D"]["SPEA2"]={"evals":2105}
data["POM3D"]["GALE_NM"]={"evals":11}
data["POM3D"]["GALE_LP"]={"evals":36}
data["POM3D"]["GALE_LPI"]={"evals":36}
data["POM3A"] = {}
data["POM3A"]["GALE"]={"evals":100}
data["POM3A"]["NSGAII"]={"evals":1786}
data["POM3A"]["SPEA2"]={"evals":1786}
data["POM3A"]["GALE_NM"]={"evals":9}
data["POM3A"]["GALE_LP"]={"evals":30}
data["POM3A"]["GALE_LPI"]={"evals":30}
data["POM3B"] = {}
data["POM3B"]["GALE"]={"evals":100}
data["POM3B"]["NSGAII"]={"evals":2041}
data["POM3B"]["SPEA2"]={"evals":2041}
data["POM3B"]["GALE_NM"]={"evals":9}
data["POM3B"]["GALE_LP"]={"evals":36}
data["POM3B"]["GALE_LPI"]={"evals":36}
data["POM3C"] = {}
data["POM3C"]["GALE"]={"evals":100}
data["POM3C"]["NSGAII"]={"evals":2522}
data["POM3C"]["SPEA2"]={"evals":2761}
data["POM3C"]["GALE_NM"]={"evals":14}
data["POM3C"]["GALE_LP"]={"evals":52}
data["POM3C"]["GALE_LPI"]={"evals":52}
data["XOMO_ALL"] = {}
data["XOMO_ALL"]["GALE"]={"evals":100}
data["XOMO_ALL"]["NSGAII"]={"evals":3704}
data["XOMO_ALL"]["SPEA2"]={"evals":3704}
data["XOMO_ALL"]["GALE_NM"]={"evals":19}
data["XOMO_ALL"]["GALE_LP"]={"evals":63}
data["XOMO_ALL"]["GALE_LPI"]={"evals":63}
data["XOMO_OSP"] = {}
data["XOMO_OSP"]["GALE"]={"evals":100}
data["XOMO_OSP"]["NSGAII"]={"evals":2771}
data["XOMO_OSP"]["SPEA2"]={"evals":2736}
data["XOMO_OSP"]["GALE_NM"]={"evals":14}
data["XOMO_OSP"]["GALE_LP"]={"evals":49}
data["XOMO_OSP"]["GALE_LPI"]={"evals":49}
data["XOMOO2"] = {}
data["XOMOO2"]["GALE"]={"evals":100}
data["XOMOO2"]["NSGAII"]={"evals":3509}
data["XOMOO2"]["SPEA2"]={"evals":3509}
data["XOMOO2"]["GALE_NM"]={"evals":18}
data["XOMOO2"]["GALE_LP"]={"evals":61}
data["XOMOO2"]["GALE_LPI"]={"evals":61}
data["XOMO_Flight"] = {}
data["XOMO_Flight"]["GALE"]={"evals":100}
data["XOMO_Flight"]["NSGAII"]={"evals":3636}
data["XOMO_Flight"]["SPEA2"]={"evals":3636}
data["XOMO_Flight"]["GALE_NM"]={"evals":16}
data["XOMO_Flight"]["GALE_LP"]={"evals":64}
data["XOMO_Flight"]["GALE_LPI"]={"evals":64}

import numpy as np
import matplotlib.pyplot as plt



def get_data(method, field):
    datasets = ["POM3A", "POM3B", "POM3C", "POM3D", "XOMO_ALL", "XOMO_OSP", "XOMOO2", "ground", "XOMO_Flight"]
    return_arr = []
    for dataset in datasets:
        return_arr.append(data[dataset][method][field])
    return return_arr

# index = np.array([10, 40, 70, 100, 130, 160])
index = np.array([30*(i+1) for i in xrange(9)])
print index



left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

bar_width = 4
#
opacity = 0.2
error_config = {'ecolor': '0.3'}
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'], 'size':9.5})
# rc('text', usetex=True)

f, (ax1) = plt.subplots(nrows=1, ncols=1)

# plt.ylabel("Time saved(%)", fontsize=11)
# ax1.set_title('Apache')
r1 = ax1.bar(index, get_data("NSGAII", "evals"), bar_width,alpha=opacity,color='#660066',error_kw=error_config)
r2 = ax1.bar(index+bar_width, get_data("SPEA2", "evals"), bar_width,alpha=opacity,color='#CC0000',error_kw=error_config)
r3 = ax1.bar(index + 2*bar_width, get_data("GALE", "evals"), bar_width,alpha=opacity,color='y',error_kw=error_config)
r4 = ax1.bar(index + 3*bar_width, get_data("GALE_NM", "evals"), bar_width,alpha=opacity,color='g',error_kw=error_config)
r5 = ax1.bar(index + 4*bar_width, get_data("GALE_LP", "evals"), bar_width,alpha=opacity,color='#FA5705',error_kw=error_config)
r6 = ax1.bar(index + 5*bar_width, get_data("GALE_LPI", "evals"), bar_width,alpha=opacity,color='#00D9FA',error_kw=error_config)
ax1.set_yscale('log')
# ax1.set_ylim(0, 119)
# ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.yaxis.offsetText.set_visible(False)

# ax1.set_ylabel("Mean(%) Fault Rate")
ax1.text(0.5, 0.95*(bottom+top), 'Evaluations',
        horizontalalignment='center',
        verticalalignment='top',
        rotation=0,
        fontsize=15,
        transform=ax1.transAxes)
# ax1.set_yticks([0, 10, 20, 48],)
# ax1.set_yticklabels([0, 10, 20, 98.2])
# ax1.set_yscale('log', basey=10)
ax1.set_xticks([41, 71, 101, 131, 161, 191, 221, 251, 281])
ax1.set_xticklabels(["POM3A", "POM3B", "POM3C", "POM3D", "X_ALL", "X_OSP", "X_O2", "X_G", "X_F"], rotation='vertical', fontsize='x-large')
ax1.tick_params(axis='y', labelsize=15)
ax1.set_xlim(22, 300)



plt.figlegend([r1, r2, r3, r4, r5, r6], ["NSGAII", "SPEA2", "GALE", "GALE-S-NM", "GALE-S-LP", "GALE-S-LP-I"], frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.013), fancybox=True, ncol=6, prop={'size':15})
# f.text(0.04, 0.5, 'Time Saved(%)', va='center', rotation='vertical', fontsize=11)
# plt.xlim(5, 125)
f.set_size_inches(12,7)
# f.subplots_adjust(wspace=0, hspace=0)
# plt.ylabel("Time saved(%)", fontsize=11)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.tight_layout()
# plt.show()
plt.savefig('rq4.eps', format='eps')