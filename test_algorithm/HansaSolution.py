from df_utility.HitLinesProvider import *

def get_odd_dets_line():
    pass

def get_even_dets_line():
    pass

def get_hansa_solution(hits_df, geom_df, event_id, group_id):
    odd_dets_line = get_odd_dets_line()
    even_dets_line = get_even_dets_line()

    current_hits = get_current_hits_df(event_id, group_id, hits_df)
    pass
    # ok now take