import pandas as pd
from sklearn.ensemble import IsolationForest
import re


def get_annotated(annotations, srna, strand=None):
    overlapping_annotations = annotations[
        annotations['start'].between(srna['start'], srna['end'], inclusive='neither') |
        annotations['end'].between(srna['start'], srna['end'], inclusive='neither') |
        ((annotations['start'] < srna['start']) & (srna['end'] < annotations['end']))
    ]
    if len(overlapping_annotations.index) == 0:
        return 'Intergenic'

    overlapped_rows = {}
    srna_length = srna['end'] - srna['start']
    for i, annotation in overlapping_annotations.iterrows():
        overlap = min(annotation['end'], srna['end']) - max(annotation['start'], srna['start'])
        overlapped_rows[i] = overlap * 100 / srna_length

    max_overlap = max(overlapped_rows.values())
    Is = [k for k, v in overlapped_rows.items() if v == max_overlap]

    if len(Is) == 1 or strand is None: I = Is[0]
    elif annotations.loc[Is[0], 'strand'] == strand: I = Is[0]
    elif annotations.loc[Is[1], 'strand'] == strand: I = Is[1]
    else: I = Is[0]

    if overlapped_rows[I] < 50 and len(Is) == 1:
        return 'Intergenic'

    match = re.fullmatch('^ID=([^;]*);.*$', annotations.loc[I, 'gene_id'])
    if match is None:
        return None
    elif strand is None:
        return match.group(1)
    elif annotations.loc[I, 'strand'] == strand:
        return 'Sense to ' + match.group(1)
    else:
        return 'Antisense to ' + match.group(1)


def annotate(regions, annotations, strand=None):
    d_out = pd.DataFrame(columns=['name', 'start', 'end', 'location'])
    for i, srna in regions.iterrows():
        an = get_annotated(annotations, srna, strand)
        name = 'sRNA-{0}'.format(i) if strand is None \
            else 'Fwd-sRNA-{0}'.format(i) if strand == '+' \
            else 'Rev-sRNA-{0}'.format(i)
        d_out.loc[i] = [name, srna['start'], srna['end'], an]
    return d_out


def group_consecutive(vals, step=1):
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result


def detectSRNA(data, cf):
    readcount = data['readcount'].values.reshape(-1, 1)
    clf = IsolationForest(contamination=cf, n_jobs=1, n_estimators=100, max_samples=5000, random_state=0)
    clf.fit(readcount)

    pred = clf.predict(readcount)
    scores = clf.decision_function(readcount)

    # add the anomaly score and decision(-1/1) to the data frame
    data['anomaly decision'] = pred
    data['score'] = scores

    # Get the regions
    a = data[data['anomaly decision'] == -1]
    Regions = []
    for group in group_consecutive(a['position']):
        if len(group) > 1:
            Regions.append([group[0], group[-1]])

    Merged = [Regions[0]]
    for region in Regions[1:]:
        if region[0] - Merged[-1][-1] <= 5:
            Merged[-1][-1] = region[-1]
        else:
            Merged.append(region)

    reg = pd.DataFrame(Merged, columns=['start', 'end'])
    regions = reg[reg['end'] - reg['start'] >= 20].copy()
    return regions



