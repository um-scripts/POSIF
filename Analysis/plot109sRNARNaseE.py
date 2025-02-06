from io import BytesIO

import matplotlib.pyplot as plt
from PIL import Image
import matplotlib
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import rcParams
import json
import re

from matplotlib.ticker import StrMethodFormatter

# from plot_bedgraph import extract_bed


rcParams['font.family'] = 'Arial'
rcParams['font.size'] = 8
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 8
})

# RNaseWTfwd = extract_bed('WTfwd_seqdepNorm.bg')
# RNaseWTrev = extract_bed('WTrev_seqdepNorm.bg')
RNaseWTfwd= pd.read_csv('SRR8550304perbasefwd.bed', sep= '\t', names= ['chrom', 'position', 'ReadCount'])
RNaseWTrev= pd.read_csv('SRR8550304perbaserev.bed', sep= '\t', names= ['chrom', 'position', 'ReadCount'])


# RNaseTreatedfwd = extract_bed('fwd_seqdepNorm.bg')
# RNaseTreatedrev = extract_bed('rev_seqdepNorm.bg')
RNaseTreatedfwd= pd.read_csv('SRR8550316perbasefwd.bed', sep= '\t', names= ['chrom', 'position', 'ReadCount'])
RNaseTreatedrev= pd.read_csv('SRR8550316perbaserev.bed', sep= '\t', names= ['chrom', 'position', 'ReadCount'])

# --------------
# bedgraphfilesFromNCBI
# Treated = extract_bed('GSM3595717_1xn_RNE_Cas9_3.bedgraph')
# WildType = extract_bed('GSM3595705_1xn_WT3.bedgraph')
# Treated.to_csv('RNaseTreated.csv', index= False)
# WildType.to_csv('RNaseWildtype.csv', index= False)
# ------------------
# FWD/REV
m = pd.read_csv('206PadjControlCDS_significant.csv')
a = pd.read_csv('annotation.csv',header=None, names=['Name', 'Start', 'End', 'Strand', 'Position'])


m['anno_start']=None
m['anno_end']= None

m['Rv'] = m['Location'].apply(lambda x: x[9:])

for i, row in m.iterrows():
    idx = a[a['Position'] == row['Rv']].index.values[0]

    m.loc[i, 'anno_start'] = int(a.iloc[idx]['Start'])
    m.loc[i, 'anno_end'] = int(a.iloc[idx]['End'])

N = m.shape[0]

for i, row in m.iterrows():
    print(i)
    sRNA_start, sRNA_end = min(row['start'],row['end']),max(row['start'],row['end'])
    start, end = min(row['anno_start'],row['anno_end']),max(row['anno_start'],row['anno_end'])
    if row['strand'] == '+':
        RNaseWT = RNaseWTfwd
        RNaseTreated = RNaseTreatedfwd
    else:
        RNaseWT = RNaseWTrev
        RNaseTreated = RNaseTreatedrev

    fig, ax = plt.subplots(1, 1)
    ax.plot(RNaseWT.ReadCount[start:end + 1], color='pink', linewidth=1)
    ax.plot(RNaseWT.ReadCount[sRNA_start:sRNA_end+1], color='crimson', linewidth=2)
    ax.plot(RNaseTreated.ReadCount[start:end + 1], color='cyan', linewidth=1)
    ax.plot(RNaseTreated.ReadCount[sRNA_start:sRNA_end+1], color='blue', linewidth=2)

    ax.legend(['RNase_WT_CDS', 'RNase_WT_sRNA', 'RNase_Depleted_CDS', 'RNase_Depleted_sRNA'])
    ax.set_xlabel('Genomic Position')
    ax.set_ylabel('Read count')

    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
    ax.set_xticks(ticks=ax.get_xticks(), fontname='Arial', fontsize=2)
    ax.set_yticks(ticks=ax.get_yticks(), fontname='Arial', fontsize=2)

    ax.set_xlim([start-50, end+50])
    fig.suptitle(r'{locus}, \textit{{{rv}}}'.format(locus=row["Locus_tag"], rv=row["Rv"].split("-")[1]))

    plt.tight_layout()
    png1 = BytesIO()
    plt.savefig(png1, format='jpeg', dpi=300)
    plt.close()

    png2 = Image.open(png1)
    png2.save(f'FiguresFinalSS_new/{row["Locus_tag"]}.jpeg')
    png1.close()
    png2.close()
    plt.close(fig)

# =======================================================
#
# RNaseWT = pd.read_csv('RNaseWildtype.csv')
# RNaseTreated= pd.read_csv('RNaseTreated.csv')
#
#
# m = pd.read_csv('206PadjControlCDS_significant.csv')
# a = pd.read_csv('annotation.csv',header=None, names=['Name', 'Start', 'End', 'Strand', 'Position'])
#
# m['anno_start']=None
# m['anno_end']= None
#
# m['Rv'] = m['Location'].apply(lambda x: x[9:])
# for i, row in m.iterrows():
#     idx = a[a['Position'] == row['Rv']].index.values[0]
#
#     m.loc[i, 'anno_start'] = a.iloc[idx]['Start']
#     m.loc[i, 'anno_end'] = a.iloc[idx]['End']
#
#
# for i, row in m.iterrows():
#     print(i)
#     sRNA_start, sRNA_end = min(row['start'],row['end']),max(row['start'],row['end'])
#     start, end = min(row['anno_start'],row['anno_end']),max(row['anno_start'],row['anno_end'])
#     if row['strand'] == '+':
#         RNaseWT = RNaseWTfwd
#         RNaseTreated = RNaseTreatedfwd
#     else:
#         RNaseWT = RNaseWTrev
#         RNaseTreated = RNaseTreatedrev

    # plt.plot(RNaseWT.normalizedRC[start:end + 1], color='pink', linewidth=1)
    #
    # plt.plot(RNaseWT.normalizedRC[sRNA_start:sRNA_end+1], color='crimson', linewidth=2)
    #
    # plt.plot(RNaseTreated.normalizedRC[start:end + 1], color='cyan', linewidth=1)
    #
    # plt.plot(RNaseTreated.normalizedRC[sRNA_start:sRNA_end+1], color='blue', linewidth=2)
    #
    # plt.legend(['RNaseWT_CDS','RNaseWT_sRNA', 'RNaseTREAT_CDS','RNaseTREAT_sRNA'])
    #
    #
    # plt.xlim([start-50, end+50])
    # plt.title(f'{row["Locus_tag"]}({row["strand"]}), {row["Rv"]}, " (WT)"')
    #
    #
    # plt.tight_layout()
    # plt.savefig(f'figureNCBI/{row["Locus_tag"]}.png', dpi=150)
    # plt.close()

