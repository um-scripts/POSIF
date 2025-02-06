import pandas as pd
import scipy.stats

#TWO TAILED


# D = pd.read_csv('RNaseEvsWT_pvalue.csv')
# distribution_param = 'WT_fpkm'
# test_param = 'RNaseEDep_fpkm'
#
# mean = D[distribution_param].mean()
# std = D[distribution_param].std()
# n = D.shape[0]
# D['t-statistic'] = (D[test_param] - mean) * n**0.5 / std
# D['p-value'] = scipy.stats.t.sf(D['t-statistic'].abs(), df=n-1)*2
# D.to_csv('p_value_twoTail.csv', index=False)
#----------------------------------
#LEFT TAILED
#
# D = pd.read_csv('206_NoTSS.csv')
# distribution_param = 'WT_FPKM'
# test_param = 'RNaseD_FPKM'
# mean = D[distribution_param].mean()
# print(mean)
# std = D[distribution_param].std()
# n = D.shape[0]
# D['t-statistic'] = (D[test_param] - mean) * n**0.5 / std
# D['p-value'] = scipy.stats.t.cdf(D['t-statistic'], df=n-1)
# D.to_csv('206_ControlPvalue.csv', index=False)
# #----------------------------------------------
#FILTER LEFT TAILED/SIGNIFICANCE
#
# D = pd.read_csv('5\'Control_p_value.csv')
# distribution_param = 'WildtypeFPKM'
# test_param = 'RNasedepFPKM'
# mean = D[distribution_param].mean()
# print(mean)
# std = D[distribution_param].std()
# n = D.shape[0]
# D['t-statistic'] = (D[test_param] - mean) * n**0.5 / std
# D['p-value'] = scipy.stats.t.cdf(D['t-statistic'], df=n-1)
# filterD= D[D['p-value']<0.5].copy()
# filterD.to_csv('5\'control_p_value_filtered.csv', index=False)


#
# d= pd.read_csv('206PadjControlCDS.csv')
# m= d[(d['significance']=='significant') & (d['WT_FPKM'] < d['RNaseD_FPKM'])]
# print(m)

#get the CDS start end from annotationfile
an= pd.read_csv('annotation.csv')
srna= pd.read_csv('206_NoTSS.csv')

srna['Rv']= srna['Location'].apply(lambda x: x[9:])
merge= pd.merge(srna,an, left_on= 'Rv', right_on='locationCDS', how= 'left')
merge.to_csv('cds_coord206sRNA.csv', index= False)