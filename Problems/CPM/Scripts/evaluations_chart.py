
def list_files():
    log_directory = "../Logs/"
    import os
    files = [log_directory+file for file in os.listdir(log_directory) if file[-4:]==".txt"]
    return files

def get_data(filename):
    filter = [0.1, 0.2, 0.4, 0.8]
    data = {}
    lines = open(filename, "r").readlines()
    for i, line in enumerate(lines):
        if i == 0: continue
        temp = line[:-1].split(",")
        temp[-1] = temp[-1].replace("\n", "")
        if float(temp[0]) not in filter: continue
        # saved_percentage = float(temp[-2])/float(temp[-2]) * 100
        if temp[-1] in data.keys(): data[temp[-1]].append(float(temp[-2]))
        else:  data[temp[-1]] = [float(temp[-2])]

    return data

data = {}
left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height
files = list_files()
for file in files:
    name = file[:-4].split("_")[1]
    data[name] = get_data(file)

import numpy as np
import matplotlib.pyplot as plt

# Data = evaluation_data()

# print len(Data["apache"]["east_west_where"])

left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

index = np.array([10, 20, 30, 40])
bar_width = 2
#
opacity = 0.2
error_config = {'ecolor': '0.3'}
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'], 'size':9.5})
# rc('text', usetex=True)

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, sharex='col', sharey='row')

r1 = ax1.bar(index + bar_width, data["apache"]["base_line"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax1.bar(index + 2*bar_width, data["apache"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax1.bar(index + 3*bar_width, data["apache"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
ax1.yaxis.offsetText.set_visible(False)
ax1.set_yticks(np.arange(0, 160, 30))


ax1.text(right, 0.5*(bottom+top), 'Apache',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax1.transAxes)


# ax2.set_title('Berkeley DB C')
#r1 = ax1.bar(index + bar_width, Data["BDBC"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax2.bar(index + bar_width, data["BDBC"]["base_line"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax2.bar(index + 2*bar_width, data["BDBC"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax2.bar(index + 3*bar_width, data["BDBC"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
ax2.yaxis.offsetText.set_visible(False)
ax2.set_yticks(np.arange(0, 2100, 500))
ax2.text(right, 0.5*(bottom+top), 'BDBC',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax2.transAxes)


# ax3.set_title('Berkeley DB Java')
#r1 = ax1.bar(index + bar_width, Data["BDBJ"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax3.bar(index + bar_width, data["BDBJ"]["base_line"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax3.bar(index + 2*bar_width, data["BDBJ"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax3.bar(index + 3*bar_width, data["BDBJ"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
ax3.set_yticks(np.arange(0, 150, 30))
ax3.yaxis.offsetText.set_visible(False)
ax3.text(right, 0.5*(bottom+top), 'BDBJ',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax3.transAxes)


# ax4.set_title('LLVM')
#r1 = ax1.bar(index + bar_width, Data["LLVM"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax4.bar(index + bar_width, data["LLVM"]["base_line"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax4.bar(index + 2*bar_width, data["LLVM"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax4.bar(index + 3*bar_width, data["LLVM"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
ax4.set_yticks(np.arange(0, 900, 200))
ax4.yaxis.offsetText.set_visible(False)
ax4.text(right, 0.5*(bottom+top), 'LLVM',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax4.transAxes)



#r1 = ax1.bar(index + bar_width, Data["SQL"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax5.bar(index + bar_width, data["SQL"]["base_line"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax5.bar(index + 2*bar_width, data["SQL"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax5.bar(index + 3*bar_width, data["SQL"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
ax5.set_yticks(np.arange(0, 4000, 1000))
ax5.yaxis.offsetText.set_visible(False)
ax5.text(right, 0.5*(bottom+top), 'SQL',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax5.transAxes)

# ax6.set_title('X264')
#r1 = ax1.bar(index + bar_width, Data["X264"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax6.bar(index + bar_width, data["X264"]["base_line"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax6.bar(index + 2*bar_width, data["X264"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax6.bar(index + 3*bar_width, data["X264"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
ax6.set_yticks(np.arange(0, 1000, 200))
ax6.yaxis.offsetText.set_visible(False)
ax6.text(right, 0.5*(bottom+top), 'X264',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax6.transAxes)



plt.figlegend([ r1, r2, r3], [ "Where Exemplar", "Where Random",  "Where East West"], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.0145), fancybox=True, ncol=3)
f.text(0.04, 0.5, 'Number of Evaluations', va='center', rotation='vertical', fontsize=11)
plt.xticks([15, 25, 35, 45], ['10', '20', '40', '80'])
f.set_size_inches(6.0, 8.5)
f.subplots_adjust(wspace=0, hspace=0)
plt.xlabel("Percentage of Data(%)", fontsize=11)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.tight_layout()
# plt.show()
plt.savefig('evaluation_graph.eps', format='eps')