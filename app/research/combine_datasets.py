import pandas as pd
import os

def combine(name_dir):
    path_dir = 'datasets/' + name_dir

    df = ""
    i = 0
    for _, __, files in os.walk(path_dir):
        for file in files:
            if i == 0:
                df = pd.read_csv(path_dir + f'/{file}')
                i = 1
            else:
                df1 = pd.read_csv(path_dir + f'/{file}')
                df = pd.merge(df, df1, how="outer", on=["e", "v", "Nu"], sort=True, suffixes=(False, False))


    df.to_csv(f'datasets/{name_dir}/combined_nusselt.csv', index=False)


import sys
combine(sys.argv[1])