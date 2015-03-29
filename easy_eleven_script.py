import sys
import pandas as pd
import scipy
import eleven

'''
USAGE:

easy_eleven qPCR_data_file.csv Reference_Genes.csv Control_sample_name


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
Output of rank_targets()



'''
df = pd.read_csv(sys.argv[1])
print df

censored = eleven.censor_background(df)
print censored

#Read Reference_Genes.csv 
with open('ref_genes.csv', 'r') as f:
	ref_genes = [line.strip() for line in f]

constant_sample = sys.argv[3]

ranked = eleven.rank_targets(censored, ref_genes, constant_sample)

print ranked

nf = eleven.calculate_nf(censored, ranked.ix['Target',0:3],constant_sample)

print nf

censored['RelExp'] = eleven.expression_nf(censored, nf, constant_sample)

print censored