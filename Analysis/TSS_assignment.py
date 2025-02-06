import pandas as pd

df1 = pd.read_csv("FINAL_sRNA_1122_TSS_out.csv")
df2 = pd.read_csv("Control432.csv")
df3 = pd.read_csv("Control_completelyInsideCDS245.csv")

df12= pd.merge(df1,df2, on='Name', how = "right", indicator= True)
df13= pd.merge(df1,df3, on='Name', how = "right", indicator= True)
df12.drop(inplace=True, index=df12[df12['primary'].isna() & df12['alternative'].isna() & df12['internal'].isna()].index)
df13.drop(inplace=True, index=df13[df13['primary'].isna() & df13['alternative'].isna() & df13['internal'].isna()].index)
df1.drop(inplace=True, index=df1[df1['primary'].isna() & df1['alternative'].isna() & df1['internal'].isna()].index)
df12.to_csv("out432TSScontrol.csv", index = False)
df13.to_csv("out245TSScontrol.csv", index = False)
df1.to_csv("out1120TSS.csv", index = False)
