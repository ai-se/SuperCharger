data = {}

data["ground"] = {}
data["ground"]["GALE"]={"hv":100, "spread":100}
data["ground"]["NSGAII"]={"hv":157, "spread":124}
data["ground"]["SPEA2"]={"hv":158, "spread":116}
data["ground"]["GALE_NM"]={"hv":91, "spread":104}

data["POM3D"] = {}
data["POM3D"]["GALE"]={"hv":100, "spread":100}
data["POM3D"]["NSGAII"]={"hv":142, "spread":121}
data["POM3D"]["SPEA2"]={"hv":142, "spread":117}
data["POM3D"]["GALE_NM"]={"hv":88, "spread":103}

data["POM3A"] = {}
data["POM3A"]["GALE"]={"hv":100, "spread":100}
data["POM3A"]["NSGAII"]={"hv":210, "spread":101}
data["POM3A"]["SPEA2"]={"hv":213, "spread":108}
data["POM3A"]["GALE_NM"]={"hv":87, "spread":102}

data["POM3B"] = {}
data["POM3B"]["GALE"]={"hv":100, "spread":100}
data["POM3B"]["NSGAII"]={"hv":128, "spread":132}
data["POM3B"]["SPEA2"]={"hv":129, "spread":120}
data["POM3B"]["GALE_NM"]={"hv":93, "spread":102}

data["POM3C"] = {}
data["POM3C"]["GALE"]={"hv":100, "spread":100}
data["POM3C"]["NSGAII"]={"hv":145, "spread":100}
data["POM3C"]["SPEA2"]={"hv":143, "spread":99}
data["POM3C"]["GALE_NM"]={"hv":90, "spread":100}

data["XOMO_ALL"] = {}
data["XOMO_ALL"]["GALE"]={"hv":100, "spread":100}
data["XOMO_ALL"]["NSGAII"]={"hv":140, "spread":106}
data["XOMO_ALL"]["SPEA2"]={"hv":138, "spread":105}
data["XOMO_ALL"]["GALE_NM"]={"hv":105, "spread":105}

data["XOMO_OSP"] = {}
data["XOMO_OSP"]["GALE"]={"hv":100, "spread":100}
data["XOMO_OSP"]["NSGAII"]={"hv":141, "spread":99}
data["XOMO_OSP"]["SPEA2"]={"hv":142, "spread":100}
data["XOMO_OSP"]["GALE_NM"]={"hv":93, "spread":100}

data["XOMOO2"] = {}
data["XOMOO2"]["GALE"]={"hv":100, "spread":100}
data["XOMOO2"]["NSGAII"]={"hv":139, "spread":101}
data["XOMOO2"]["SPEA2"]={"hv":138, "spread":100}
data["XOMOO2"]["GALE_NM"]={"hv":94, "spread":98}

data["XOMO_Flight"] = {}
data["XOMO_Flight"]["GALE"]={"hv":100, "spread":100}
data["XOMO_Flight"]["NSGAII"]={"hv":93, "spread":114}
data["XOMO_Flight"]["SPEA2"]={"hv":93, "spread":168}
data["XOMO_Flight"]["GALE_NM"]={"hv":96, "spread":107}





import numpy as np
import matplotlib.pyplot as plt



def get_data(method, field):
    datasets = ["POM3A", "POM3B", "POM3C", "POM3D", "XOMO_ALL", "XOMO_OSP", "XOMOO2", "ground", "XOMO_Flight"]
    return_arr = []
    for dataset in datasets:
        return_arr.append(data[dataset][method][field])
    return return_arr

# index = np.array([10, 40, 70, 100, 130, 160])
index = np.array([25*(i+1) for i in xrange(9)])
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

f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

# plt.ylabel("Time saved(%)", fontsize=11)
# ax1.set_title('Apache')
r1 = ax1.bar(index, get_data("NSGAII", "hv"), bar_width,alpha=opacity,color='#660066',error_kw=error_config)
r2 = ax1.bar(index+bar_width, get_data("SPEA2", "hv"), bar_width,alpha=opacity,color='#CC0000',error_kw=error_config)
r3 = ax1.bar(index + 2*bar_width, get_data("GALE", "hv"), bar_width,alpha=opacity,color='y',error_kw=error_config)
r4 = ax1.bar(index + 3*bar_width, get_data("GALE_NM", "hv"), bar_width,alpha=opacity,color='g',error_kw=error_config)
# ax1.set_xlim(5, 190)
# ax1.set_ylim(0, 119)
# ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.yaxis.offsetText.set_visible(False)

# ax1.set_ylabel("Mean(%) Fault Rate")
ax1.text(0.5, 0.95*(bottom+top), 'Hypervolume',
        horizontalalignment='center',
        verticalalignment='top',
        rotation=0,
        fontsize=12,
        transform=ax1.transAxes)
# ax1.set_yticks([0, 10, 20, 48],)
# ax1.set_yticklabels([0, 10, 20, 98.2])
# ax1.set_yscale('log', basey=10)
ax1.set_xticks([34, 59, 84, 109, 134, 159, 184, 209, 234])
ax1.set_xticklabels(["POM3A", "POM3B", "POM3C", "POM3D", "X_ALL", "X_OSP", "X_O2", "X_G", "X_F"], rotation='vertical', fontsize='large')
ax1.tick_params(axis='y', labelsize=12)
ax1.set_xlim(10, 250)


# ax2.set_title('Berkeley DB C')
r1 = ax2.bar(index, get_data("NSGAII", "spread"), bar_width,alpha=opacity,color='#660066',error_kw=error_config)
r2 = ax2.bar(index+bar_width, get_data("SPEA2", "spread"), bar_width,alpha=opacity,color='#CC0000',error_kw=error_config)
r3 = ax2.bar(index + 2*bar_width, get_data("GALE", "spread"), bar_width,alpha=opacity,color='y',error_kw=error_config)
r4 = ax2.bar(index + 3*bar_width, get_data("GALE_NM", "spread"), bar_width,alpha=opacity,color='g',error_kw=error_config)
ax2.set_xlim(10, 250)
ax2.tick_params(axis='y', labelsize=12)
# ax2.set_ylim(0, 52)
# ax2.set_yscale("log")

ax2.yaxis.offsetText.set_visible(False)
ax2.text(0.5, 0.95*(bottom+top), 'Spread',
        horizontalalignment='center',
        verticalalignment='top',
        rotation=0,
        fontsize=12,
        transform=ax2.transAxes)

ax2.set_yticks([0, 50, 100, 150, 200, 250])
ax2.set_xticks([34, 59, 84, 109, 134, 159, 184, 209, 234])
ax2.set_xticklabels(["POM3A", "POM3B", "POM3C", "POM3D", "X_ALL", "X_OSP", "X_O2", "X_G", "X_F"], rotation='vertical', fontsize='large')
ax2.tick_params(axis='y', labelsize=12)



plt.figlegend([r1, r2, r3, r4], ["NSGAII", "SPEA2", "GALE",  "GALE-S-NM"], frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.023), fancybox=True, ncol=5)
# f.text(0.04, 0.5, 'Time Saved(%)', va='center', rotation='vertical', fontsize=11)
# plt.xlim(5, 125)
f.set_size_inches(12, 5)
# f.subplots_adjust(wspace=0, hspace=0)
# plt.ylabel("Time saved(%)", fontsize=11)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.tight_layout()
# plt.show()
plt.savefig('rq1.eps', format='eps')