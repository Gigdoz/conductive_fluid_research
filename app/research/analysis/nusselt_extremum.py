import matplotlib.pyplot as plt
import pandas as pd

def sort_by_param(df, param):
    if param == 'v':
        inv_param = 'e'
    else:
        inv_param = 'v'
    df = df.sort_values(by=param)
    res = pd.DataFrame([], columns=['e', 'v', 'Nu'])
    unqs = df[param].unique()
    for p in unqs:
        res = pd.concat([res, df.loc[df[param] == p].sort_values(by=inv_param)], axis=0)
    return res

def points_max_and_min(df):
    e = []
    v= []
    for i in range(1, len(df) - 1):
        if df.iloc[i]['Nu'] > df.iloc[i - 1]['Nu'] and df.iloc[i]['Nu'] > df.iloc[i + 1]['Nu'] or df.iloc[i]['Nu'] < df.iloc[i - 1]['Nu'] and df.iloc[i]['Nu'] < df.iloc[i + 1]['Nu']:
            e.append(df.iloc[i]['e'])
            v.append(df.iloc[i]['v'])
    return e, v


df = pd.read_csv('data/nusselt/nusselt e=50.0-300.0; v=2.5-7.5.csv')
df['Nu'] = 1.0 - 2/15 * df['Nu']
df = sort_by_param(df, 'e')
e, v = points_max_and_min(df)

plt.plot(v, e, '.', markersize=2)
plt.show()