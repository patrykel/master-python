from df_utility.DFProvider import *
from df_utility.HitLinesProvider import *
from df_utility.ResultDataframeProvider import *
from minimization.SolutionProvider import *

geom_df = get_df_from_csv("geom_df.csv")
hits_df = get_df_from_csv("single_df.csv")

row = 1
row_dfs = []

# Iteruj sie po event / group
for event_id, group_id in get_iterable_event_group_list(hits_df):
    if row > 20:
        break

    print("row = {}\tev = {}\tgroup = {}".format(row, event_id, group_id))
    hit_lines = extract_hit_lines(hits_df, geom_df, event_id, group_id, translate_first_z_to_zero=True, in_mm=True)
    solution, method = get_solution_track(hit_lines, geom_df)
    row_df = get_solution_df(event_id, group_id, method, solution, hit_lines, geom_df)

    row_dfs.append(row_df)
    row = row + 1

result_df = pd.concat(row_dfs, ignore_index=True)
print(result_df)


# GeomDF could be in a lazy provider --> to update
