import numpy as np
import pandas as pd
g = pd.read_csv('13sRNALocation.csv')

g['sRNA Position']= np.nan
for index, row in g.iterrows():
    if pd.isna(row['anno_STRAND']):
        g.loc[index, 'sRNA Position'] = row['anno_location']
    elif row['sRNA_STRAND']==row['anno_STRAND']:
        sRNA_location= 'Sense to '+ row['anno_location']
        g.loc[index, 'sRNA Position'] = sRNA_location
    else:
        sRNA_location= 'Antisense to '+ row['anno_location']
        g.loc[index, 'sRNA Position']=sRNA_location
g.to_csv('13smallRNAoutputLocation.csv',index = False)
