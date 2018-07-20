import pandas as pd

def get_df(row_data, column_names):
    row_data_dict = {}
    for i, (key, val) in enumerate(zip(column_names, row_data)):
        row_data_dict[key] = [val]

    return pd.DataFrame(row_data_dict, columns=column_names)