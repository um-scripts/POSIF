import pandas as pd
import re

D = pd.read_csv('46smallProt.csv')
D['Name'] = pd.NA
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
repetitions = {}

for index, row in D.iterrows():
    pos = str(row['Position'])

    name = 'ncRv'
    matches = re.findall("cds-Rv[0-9]+", pos)
    if not matches:
        continue
    name += matches[0][6:]
    name += 'i' if 'IGR' in pos else 'u' if 'UTR' in pos else ''
    name += 'c' if pos.startswith('Antisense') else ''

    D.loc[index, 'Name'] = name
    if pos in repetitions:
        repetitions[pos].append(index)
    else:
        repetitions[pos] = [index]

# Insert Letters for repetitions
for v in repetitions.values():
    if len(v) == 1:
        continue
    for i in range(len(v)):
        name = str(D.loc[v[i], 'Name'])
        if name.endswith('c'):
            new_name = name[:-1] + LETTERS[i] + name[-1]
        else:
            new_name = name + LETTERS[i]
        D.loc[v[i], 'Name'] = new_name

D.to_csv('46smallProtoutput.csv', index=False)

Names= D['Name']
Names[Names.duplicated(keep= False)].to_csv('duplicated_smallProt46.csv',index= False)
