import os
import json
from io import BytesIO
from textwrap import TextWrapper

from matplotlib.ticker import StrMethodFormatter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.ticker import ScalarFormatter

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 12
})


SRR21026187R = pd.read_csv('SRR21026187perbaseREV.bed', sep='\t', usecols=[1, 2], names=['position', 'rc'])
SRR18455932R = pd.read_csv('SRR18455932perbaseREV.bed', sep='\t', usecols=[1, 2], names=['position', 'rc'])
SRR18455928R = pd.read_csv('SRR18455928perbaseREV.bed', sep='\t', usecols=[1, 2], names=['position', 'rc'])
SRR18455925R = pd.read_csv('SRR18455925perbaseREV.bed', sep='\t', usecols=[1, 2], names=['position', 'rc'])
SRR214196865R = pd.read_csv('SRR214196865perbaseREV.bed', sep='\t', usecols=[1, 2], names=['position', 'rc'])



fig = plt.figure(figsize=(12, 6))
figure_gs = GridSpec(2, 1, figure=fig, height_ratios=[10, 1], hspace=0.2)
ax = fig.add_subplot(figure_gs[0])
leg_entries = {}

start, end = 3359585, 3363155
x = SRR21026187R['position'].to_numpy()
y = SRR21026187R['rc'].to_numpy()

mask1 = (x >= start-50) & (x <= end+50)
mask2 = (x >= 3363018) & (x <= 3363153)
ax.plot(x[mask1], y[mask1], c='black', lw=1, zorder=2)
ax.plot(x[mask2], y[mask2], c= 'red', lw= 2, zorder=3)
wrapper = TextWrapper(width=40, break_long_words=False, break_on_hyphens=False)

leg_entries['TSS'] = ax.axvline(3363155, color='navy', linewidth=0.8, ls='--')
leg_entries[r'5\' UTR of \textit{Rv3001c}'] = ax.axvspan(3362986, 3363155, alpha=0.5, color='lemonchiffon', zorder=1)
leg_entries[r'\textit{Rv3003c}'] = ax.axvspan(3361130, 3362986, alpha=0.5, color='paleturquoise', zorder=1)
leg_entries[r'\textit{Rv3002c}'] = ax.axvspan(3360624, 3361130, alpha=0.8, color='palevioletred', zorder=1)
leg_entries['IGR'] = ax.axvspan(3360586, 3360624, alpha=0.5, color='darkseagreen', zorder=1)
leg_entries[r'\textit{Rv3001c}'] = ax.axvspan(3359585, 3360586, alpha=0.5, color='mistyrose', zorder=1)


ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
ax.xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))

legend_ax = fig.add_subplot(figure_gs[1])
legend_ax.axis('off')
handles = []
labels = []
for label, handle in leg_entries.items():
    handles.append(handle)
    labels.append('\n'.join(wrapper.wrap(label)))
legend_ax.legend(handles, labels, loc='center', borderaxespad=0., ncol=6)

fig.text(0.5, 0.1, 'Genomic Position', ha='center', fontsize='medium', fontweight='bold')
fig.text(0.03, 0.55, 'Read Count', va='center',
         rotation='vertical', fontsize='medium', fontweight='bold')

plt.subplots_adjust(left=0.11, bottom=0.02, top=0.9, right=0.95)
print(y[mask1])
ax.set_xlim([start - 50, end + 50])
ax.invert_xaxis()
# plt.show()
png1 = BytesIO()
plt.savefig(png1, format='png', dpi=500)
plt.close(fig)

png2 = Image.open(png1)
png2.save('SRR21026187R.png')
png1.close()
png2.close()

