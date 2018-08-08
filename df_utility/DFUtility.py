import pandas as pd
from df_utility.Data.RPGeometry import *
from df_utility.Data.AverageOverSiliconsRP import *

def get_row_df(row_data, column_names):
    row_data_dict = {}
    for i, (key, val) in enumerate(zip(column_names, row_data)):
        row_data_dict[key] = [val]

    return pd.DataFrame(row_data_dict, columns=column_names)

def get_df(data2D, column_names):
    # WE ASSUME DATA IS 2D ARRAY
    row_dfs = []
    for row_data in data2D:
        row_dfs.append(get_row_df(row_data, column_names))

    return pd.concat(row_dfs, ignore_index=True)