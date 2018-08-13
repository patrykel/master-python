import pandas as pd

from df_utility.HansaDataframeProvider import *
from df_utility.ResultDataframeProvider import *
from minimization.SolutionProvider import *
from test_algorithm.HansaSolution import *
from test_algorithm.HansaLinesProvider import *

geom_df = get_df_from_csv("geom_df.csv")
hits_df = get_df_from_csv("single_20k_abw_df.csv")
iterable_event_group_list = get_iterable_event_group_list(hits_df)

N_row_limit = 10

Constants.K_X = 1
Constants.K_Y = 1
Constants.TRANSLATION = 50 * 1000

row = 1
row_dfs = []
hansa_row_dfs = []

hansa_lines_provider = HansaLinesProvider(hits_df,
                                          'avg_by_rp_and_direction.csv',
                                          'rp_geom_df.csv')

# Iteruj sie po event / group
for event_id, group_id in iterable_event_group_list:
    if row > N_row_limit:
        break

    print("row = {}\tev = {}\tgroup = {}".format(row, event_id, group_id))


    hit_lines = extract_hit_lines(hits_df, geom_df, event_id, group_id, translate_first_z_to_zero=True, in_mm=True)
    solution, method, exec_time = get_solution_track(hit_lines, geom_df)
    row_df = get_solution_df(event_id, group_id, method, exec_time, solution, hit_lines, geom_df,
                             with_det_distances=False)
    row_dfs.append(row_df)


    # hansa_solution_lines = get_hansa_solutions(hits_df, geom_df, event_id, group_id)
    hansa_solution_lines = hansa_lines_provider.compute_lines(event_id, group_id)

    hansa_next_row_dfs = get_hansa_next_row_dfs(hansa_solution_lines, event_id, group_id)
    hansa_row_dfs.append(hansa_next_row_dfs)

    row = row + 1


# print("Uncomment below to combine dataframes -- watch out for inconsistencies int det-id column names!!!")
print("R")
print("E")
result_df = pd.concat(row_dfs, ignore_index=True)
hansa_result_df = pd.concat(hansa_row_dfs, ignore_index=True)


# # stores t0, pu0, pv0, pt0, direction, ub_0, v_b0
# hansa_t0_df = hansa_solution_collector.get_t0_df()
#
# # stores t1, pu1, pv1, pt1, direction, ub_1, v_b1
# hansa_t1_df = hansa_solution_collector.get_t1_df()
#
# # stores 'u_a', 'u_b0', 'u_b1', 'v_a', 'v_b0', 'v_b1'
# hansa_track_df = hansa_solution_collector.get_track_df()

print("D")
print("Y")


