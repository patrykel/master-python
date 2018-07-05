import pandas as pd

detector_map = {
    1 : "L-TOP",
    2 : "L-BOT",
    3 : "L-HOR",
    4 : "R-TOP",
    5 : "R-BOT",
    6 : "R-HOR"
}


def get_column_names():
    return ['Event', 'Group', 'Method', 'DistSum', 'MDH', 'Success', 'Chi', 'ChiN',
            'x', 'y', 'z', 'dx', 'dy', 'dz',
            'dx2+dy2+dz2', 'dx/dz angle [mili rad]', 'dy/dz angle [mili rad]',
            'track_in_dets', 'track_out_dets']


def get_row_data_dict(row_data):
    result = {}
    columns = get_column_names()

    for i, (key, val) in enumerate(zip(columns, row_data)):
        result[key] = [val]

    return result


def get_row_df(row_data):
    row_data_dict = get_row_data_dict(row_data)
    columns = get_column_names()

    return pd.DataFrame(row_data_dict, columns=columns)