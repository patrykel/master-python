from df_utility.DFProvider import *
from df_utility.HitLinesProvider import *
from df_utility.ResultDataframeProvider import *
from minimization.SolutionProvider import *
from geom_classes.Constants import *
from df_utility.DFUtility import *
import pandas as pd

geom_df = get_df_from_csv("geom_df.csv")
hits_df = get_df_from_csv("single_20k_abw_df.csv")
iterable_event_group_list = get_iterable_event_group_list(hits_df)



N_row_limit = 500

Constants.K_X = 1
Constants.K_Y = 1
Constants.TRANSLATION = 50 * 1000

row = 1
row_dfs = []

# Iteruj sie po event / group
for event_id, group_id in iterable_event_group_list:
    if row > N_row_limit:
        break

    print("row = {}\tev = {}\tgroup = {}".format(row, event_id, group_id))

    hit_lines = extract_hit_lines(hits_df, geom_df, event_id, group_id, translate_first_z_to_zero=True, in_mm=True)
    solution, method, exec_time = get_solution_track(hit_lines, geom_df)
    row_df = get_solution_df(event_id, group_id, method, exec_time, solution, hit_lines, geom_df, with_det_distances=False)

    row_dfs.append(row_df)
    row = row + 1




# print("Uncomment below to combine dataframes -- watch out for inconsistencies int det-id column names!!!")
print("R")
print("E")
result_df = pd.concat(row_dfs, ignore_index=True)
print("D")
print("Y")


