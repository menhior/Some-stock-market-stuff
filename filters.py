import pandas as pd

p_t_fcf_df = pd.read_csv("p_t_fcf.csv", index_col=0)

p_t_fcf_df = p_t_fcf_df[(0.0 < p_t_fcf_df['2019'])  & (p_t_fcf_df['2019'] < 15.0)]

p_t_fcf_vals = list(p_t_fcf_df.index.values)

p_t_fcf_results = []

for i in p_t_fcf_vals:
	p_t_fcf_results.append('D_t_A___' + i[10:])

d_t_a_df = pd.read_csv("d_t_a.csv", index_col=0)

d_t_a_df = d_t_a_df.loc[p_t_fcf_results]

d_t_a_df = d_t_a_df[(0.0 < d_t_a_df['2019'])  & (d_t_a_df['2019'] < 0.15)]

d_t_a_results = []

d_t_a_df_vals = list(d_t_a_df.index.values)

for c in d_t_a_df_vals:
	d_t_a_results.append('P_t_FCF___' + c[8:])

#roc_df = pd.read_csv("roc.csv", index_col=0)



#roc_df = roc_df.loc[d_t_a_results]


p_t_fcf_df = p_t_fcf_df.loc[d_t_a_results]
p_t_fcf_df = p_t_fcf_df.dropna(subset=['2019'])
p_t_fcf_df = p_t_fcf_df.sort_values(by='2019', ascending=False)


#roc_df = roc_df.dropna(subset=['2019'])
#roc_df = roc_df.sort_values(by='2019', ascending=False)

#d_t_a_df_vals = list(d_t_a_df.index.values)

print(p_t_fcf_df)
#roc_df.to_csv("filters_2.csv")
p_t_fcf_df.to_csv("filters_2.csv")