from df_utility.DFUtility import *
from df_utility.ResultDFUtility import *

def get_hansa_column_names():
    return ['Event', 'Group', 'RP', 'x', 'y', 'z', 'dx', 'dy', 'dz',
            'dx2+dy2+dz2', 'dx/dz angle [mili rad]', 'dy/dz angle [mili rad]']


def get_hansa_data_2D(hansa_solution_lines, event_id, group_id):
    hansa_data_2D = []

    for line in hansa_solution_lines:
        dx_dz_angle = get_mili_rad_angle(line.dx, line.dz)
        dy_dz_angle = get_mili_rad_angle(line.dy, line.dz)
        group       = get_group(group_id)

        line_data = [event_id, group, int(line.det_id / 10),
                     line.x, line.y, line.z,
                     "{:.10f}".format(line.dx), "{:.10f}".format(line.dy), "{:.10f}".format(line.dz),
                     line.dx ** 2 + line.dy ** 2 + line.dz ** 2,
                     dx_dz_angle, dy_dz_angle]

        hansa_data_2D.append(line_data)

    return hansa_data_2D


def get_hansa_next_row_dfs(hansa_solution_lines, event_id, group_id):
    data_2d = get_hansa_data_2D(hansa_solution_lines, event_id, group_id)
    column_names = get_hansa_column_names()
    return get_df(data_2d, column_names)

