from df_utility.DFProvider import *
from df_utility.HitLinesProvider import *
from minimization.SolutionProvider import *

df_provider = DFProvider()
geom_df = df_provider.get_geom_df()
hits_df = df_provider.get_hits_df()

row = 1

# Iteruj sie po event / group
for event_id, group_id in get_iterable_event_group_list(hits_df):
    if row > 1:
        break

    print("ev = {}\tgroup = {}".format(event_id, group_id))
    hit_lines = extract_hit_lines(hits_df, geom_df, event_id, group_id, translate_first_z_to_zero=True, in_mm=True)
    solution_track = get_solution_track(hit_lines, geom_df)

    print(solution_track)
    print("")
    for line in hit_lines:
        print(line)

    print("")
    print("Distances:")
    for line in hit_lines:
        # print("hello, solution track: {}".format(solution_track.x))
        print("Id: {} Distance: {}".format(line.det_id, Line(params=solution_track.x, z=0.0).distance(line)))

    row = row + 1