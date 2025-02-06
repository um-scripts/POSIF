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

# from matplotlib import rc
# rc('font', **{'family': 'serif', 'serif': ['Arial']})
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    "font.size": 8
})


class ScalarFormatterClass(ScalarFormatter):
    def _set_format(self):
        self.format = "%.4f"


def read_files():
    acidicF = pd.read_csv('acidicIF_Fwd_score.bed', sep='\t')
    controlF = pd.read_csv('ControlIF_Fwd_score.bed', sep='\t')
    lowironF = pd.read_csv('LowironIF_Fwd_score.bed', sep='\t')
    membraneF = pd.read_csv('MembraneIF_Fwd_score.bed', sep='\t')
    nutrientF = pd.read_csv('NutrientIF_Fwd_score.bed', sep='\t')
    oxidativeF = pd.read_csv('OxidativeIF_Fwd_score.bed', sep='\t')

    acidicR = pd.read_csv('acidicIF_Rev_score.bed', sep='\t')
    controlR = pd.read_csv('ControlIF_Rev_score.bed', sep='\t')
    lowironR = pd.read_csv('LowironIF_Rev_score.bed', sep='\t')
    membraneR = pd.read_csv('MembraneIF_Rev_score.bed', sep='\t')
    nutrientR = pd.read_csv('NutrientIF_Rev_score.bed', sep='\t')
    oxidativeR = pd.read_csv('OxidativeIF_Rev_score.bed', sep='\t')

    dataF = {
        'Acidic pH_Fwd': ((0, 0), acidicF),
        'Iron limitation_Fwd': ((0, 1), lowironF),
        'Membrane stress_Fwd': ((0, 2), membraneF),
        'Nutrient starvation_Fwd': ((1, 0), nutrientF),
        'Oxidative stress_Fwd': ((1, 1), oxidativeF),
        'Rich medium_Fwd': ((1, 2), controlF)
    }

    dataR = {
        'Acidic pH_Rev': ((0, 0), acidicR),
        'Iron limitation_Rev': ((0, 1), lowironR),
        'Membrane stress_Rev': ((0, 2), membraneR),
        'Nutrient starvation_Rev': ((1, 0), nutrientR),
        'Oxidative stress_Rev': ((1, 1), oxidativeR),
        'Rich medium_Rev': ((1, 2), controlR)
    }

    return dataF, dataR


def plot(srna_name: str, data: dict, region: tuple, back: list[tuple], tss: list[tuple] = None, path=None):
    fig = plt.figure(figsize=(8, 4))
    figure_gs = GridSpec(2, 1, figure=fig, height_ratios=[8, 1], hspace=0.3)
    master_gs = GridSpecFromSubplotSpec(2, 3, subplot_spec=figure_gs[0], wspace=0.4, hspace=0.4)

    file = open('offset_scores.json', 'r')
    threshold = json.load(file)
    file.close()

    wrapper = TextWrapper(width=40, break_long_words=False, break_on_hyphens=False)

    path = os.getcwd() if not path else path
    leg_entries = {}
    yScalarFormatter = ScalarFormatterClass(useMathText=True)
    yScalarFormatter.set_powerlimits((0, 0))

    for name, v in data.items():
        gs_idx, d = v
        gss = GridSpecFromSubplotSpec(2, 1, hspace=0, subplot_spec=master_gs[gs_idx])
        ax0 = fig.add_subplot(gss[0])
        ax1 = fig.add_subplot(gss[1])

        for start, end, color, label in back:
            leg_entries[label] = ax0.axvspan(start, end, color=color, alpha=0.15)

        ax0.plot(d.readcount[region[0] - 100:region[-1] + 100], color='black', linewidth=1.5)
        leg_entries[srna_name] = ax0.plot(d.readcount[region[0]:region[-1]], color='firebrick', linewidth=1.5)[0]

        if tss is not None:
            for value, color, label in tss:
                leg_entries[label] = ax0.axvline(value, color=color, linewidth=0.5, ls='--')

        axis_start = min(map(lambda x: x[0], back))
        axis_end = max(map(lambda x: x[1], back))
        ax0.set_xlim([axis_start, axis_end])
        ax1.set_xlim([axis_start, axis_end])

        ax0.set_title(name.split('_')[0])
        ax0.set_xticks([])
        ax1.plot(d.score[axis_start: axis_end], color='black')
        ax1.plot(d.score[region[0]:region[-1]], color='firebrick', linewidth=1.5)
        leg_entries['Score Threshold'] = ax1.axhline(threshold[name], color='gold', ls='--', linewidth=0.8)
        # ax1.ticklabel_format(axis='x', style='sci', scilimits=(0, 0), useLocale=True)
        # ax1.xaxis.set_major_formatter(yScalarFormatter)
        min_score = min(np.min(d.score[axis_start: axis_end]), threshold[name])
        max_score = max(np.max(d.score[axis_start: axis_end]), threshold[name])
        min_rc = np.min(d.readcount[axis_start: axis_end])
        max_rc = np.max(d.readcount[axis_start: axis_end])
        rc_int = (max_rc - min_rc) * 0.1
        score_int = (max_score - min_score) * 0.1
        ax0.set_ylim([min_rc-rc_int, max_rc+rc_int])
        ax1.set_ylim([min_score-score_int, max_score+score_int])
        ax0.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
        ax1.xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
        ax1.yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
        ax1.set_xticks(ticks=np.round(np.linspace(axis_start, axis_end, 3)), fontname='Arial', fontsize=2)
        ax0.set_yticks(ticks=[(min_rc + max_rc) / 2, max_rc], fontname='Arial', fontsize=2)
        ax1.set_yticks(ticks=[(min_score + max_score)/2, min_score], fontname='Arial', fontsize=2)
        # ax1.ticklabel_format(axis='x', style='plain', useOffset=False)
    legend_ax = fig.add_subplot(figure_gs[1])
    legend_ax.axis('off')
    handles = []
    labels = []
    for label, handle in leg_entries.items():
        handles.append(handle)
        labels.append('\n'.join(wrapper.wrap(label)))
    legend_ax.legend(handles, labels, loc='center', borderaxespad=0., ncol=6)

    fig.text(0.5, 0.13, 'Genomic Position', ha='center', fontsize='medium', fontweight='bold')
    fig.text(0.03, 0.55, 'Anomaly Score (Bottom), Read Count (Top)', va='center',
             rotation='vertical', fontsize='medium', fontweight='bold')

    # plt.tight_layout()
    plt.subplots_adjust(left=0.11, bottom=0.02, top=0.9, right=0.95)

    png1 = BytesIO()
    plt.savefig(png1, format='png', dpi=500)
    plt.close(fig)

    png2 = Image.open(png1)
    png2.save(f'{path}/{srna_name}.tiff')
    png1.close()
    png2.close()
