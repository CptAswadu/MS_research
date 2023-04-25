import tabula
from tabula.io import read_pdf
import pandas as pd

df = read_pdf("12920_2018_372_MOESM1_ESM.pdf", pages='all', lattice=True, pandas_options={'header': None})
df_all = pd.concat(df[0:24])
df_all = df_all.rename(columns={0: "indernal_id", 1: "hpo_id", 2: "disorder", 3: "orphanet", 4: "gene", 5: "hgnc_id", 6: "locus", 7: "inheritant"})
df_all = df_all[df_all['hpo_id'].notna()]
df_all = df_all[df_all['gene']!='Gene']
df_all = df_all[['indernal_id','hpo_id', 'disorder', 'gene', 'hgnc_id']]
df_all['indernal_id'] = df_all['indernal_id'].str.replace('\r',' ')
df_all['hpo_id'] = df_all['hpo_id'].str.replace('\r',' ')
df_all['disorder'] = df_all['disorder'].str.replace('\r',' ')
df_all['gene'] = df_all['gene'].str.replace('\r',' ')
df_all['hgnc_id'] = df_all['hgnc_id'].str.replace('\r',' ')
