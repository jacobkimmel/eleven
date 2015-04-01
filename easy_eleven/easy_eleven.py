#!/usr/bin/python
import sys
import pandas as pd
import scipy
import eleven

'''
USAGE:

python easy_eleven.py qPCR_data_file.csv Reference_Genes.csv Control_sample_name output_path.xlsx


DATA FORMATS:

qPCR_data_file.csv
---
Sample,Target,Cq
Sample1,Target1,Cq
...
SampleN,TargetN,Cq
NTC,TargetN,Cq


Reference_Genes.csv
---
Gene1
Gene2
Gene3
Gene4

RETURNS:
raw Cq data frame, censored data frame, ranked genes, and normalization factors
Exports Excel workbook containing these data
'''

writer = pd.ExcelWriter(sys.argv[4], engine='xlsxwriter')
df = pd.read_csv(sys.argv[1])
print df

censored = eleven.censor_background(df)
print censored
censored.to_excel(writer,'Censored_Data')


#Read Reference_Genes.csv 
with open('ref_genes.csv', 'r') as f:
	ref_genes = [line.strip() for line in f]

constant_sample = str(sys.argv[3])

ranked = eleven.rank_targets(censored, ref_genes, constant_sample)

print ranked

nf = eleven.calculate_nf(censored, ranked.loc[0:2,'Target'],constant_sample)

print nf

censored['RelExp'] = eleven.expression_nf(censored, nf, constant_sample)

censored.to_excel(writer,'Relative_Exp')
ranked.to_excel(writer,'Ranked Genes')
df.to_excel(writer, 'Raw_Data')
writer.save()


