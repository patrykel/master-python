from df_utility.ResultDFUtility import *
import pandas as pd


def get_column_names(hit_lines):

    track_data_columns = ['Event', 'Group', 'Method', 'DistSum', 'MDH', 'Success', 'Chi', 'ChiN',
                        'x', 'y', 'z', 'dx', 'dy', 'dz',
                        'dx2+dy2+dz2', 'dx/dz angle [mili rad]', 'dy/dz angle [mili rad]',
                        'track_in_dets', 'track_out_dets']

    det_id_columns     = ["det-" + str(k) for k in get_det_id_list(hit_lines)]

    return track_data_columns + det_id_columns


def get_row_data_dict(row_data, hit_lines):
    result = {}
    columns = get_column_names(hit_lines)

    for i, (key, val) in enumerate(zip(columns, row_data)):
        result[key] = [val]

    return result


def get_row_df(row_data, hit_lines):
    row_data_dict = get_row_data_dict(row_data, hit_lines)
    columns = get_column_names(hit_lines)

    return pd.DataFrame(row_data_dict, columns=columns)


def get_solution_df(event_id, group_id, method, solution, hit_lines, geom_df):

    group               = get_group(group_id)
    dist_max            = get_dist_max(solution, hit_lines)
    dist_sum            = get_dist_sum(solution, hit_lines)
    chi2                = get_chi2(solution, hit_lines)
    chi2_N              = get_chi2_N(solution, hit_lines)
    x, y, z, dx, dy, dz = get_track_params(solution)
    dx_dz_angle         = get_mili_rad_angle(dx, dz)
    dy_dz_angle         = get_mili_rad_angle(dy, dz)
    tracks_in_det_no    = get_tracks_in_det_no(solution, hit_lines, geom_df)
    tracks_out_det_no   = len(hit_lines) - tracks_in_det_no


    track_data              = [event_id, group, method, dist_sum, dist_max, solution.success, chi2, chi2_N,
                               x, y, z,
                               "{:.10f}".format(dx), "{:.10f}".format(dy), "{:.10f}".format(dz),
                               dx ** 2 + dy ** 2 + dz ** 2, dx_dz_angle, dy_dz_angle,
                               tracks_in_det_no, tracks_out_det_no]
    det_hit_distances_data  = get_distances(solution, hit_lines)
    row_data                = track_data + det_hit_distances_data

    return get_row_df(row_data, hit_lines)
