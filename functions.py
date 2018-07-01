import pandas as pd

df = pd.read_csv('https://s3.us-east-2.amazonaws.com/stats-app-assets/zscores.csv', names=['z','probability'])
df.apply(pd.to_numeric)
op = df['probability'].values

def search_z(pvalue):
    ap=10
    p=0
    v=1-pvalue
    for index,row in df.iterrows():
        d = abs(row['probability']-v)
        if d < ap:
            ap = d
            p = row['probability']
    r=df.loc[df['probability']==p,'z']
    r=abs(r.iloc[0])
    return r
