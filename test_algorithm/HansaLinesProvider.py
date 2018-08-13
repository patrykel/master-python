import pandas as pd

from geom_classes.Line import *
from test_algorithm.CoordinateSystemSkeleton import *


class HansaLinesProvider():

    def __init__(self, hits_df, avg_geom_filename, rp_geom_filename):
        self.hits_df = hits_df
        self.det_avg_geom_df = pd.DataFrame.from_csv(avg_geom_filename)
        self.rp_geom_df = pd.DataFrame.from_csv(rp_geom_filename)
        self.cs_skeleton = CoordinateSystemSkeleton()

    def compute_lines(self, event_id, group_id):
        hansa_lines = []
        group_hits_df = self.get_group_hits_df(event_id, group_id)
        rp_ids = self.get_rp_numbers(group_hits_df)

        for rp_id in rp_ids:
            rp_hits_df = self.get_rp_hits_df(rp_id, group_hits_df)
            hansa_lines.append(self.compute_line(rp_id, rp_hits_df))

        return hansa_lines

    def compute_line(self, rp_id, rp_hits_df):
        self.cs_skeleton.setup(rp_id, rp_hits_df, self.det_avg_geom_df, self.rp_geom_df)
        pt0 = self.cs_skeleton.get_pt0()
        pt1 = self.cs_skeleton.get_pt1()

        return Line(start=pt0, end=pt1)


    # FOR EXTRACTING CURRENT HITS AND RP ID
    def get_rp_hits_df(self, rp_id, group_hits_df):
        return group_hits_df.loc[group_hits_df['rpID'] == rp_id]

    def get_group_hits_df(self, event_id, group_id):
        return self.hits_df.loc[(self.hits_df['eventID'] == event_id) &
                                (self.hits_df['groupID'] == group_id)]

    def get_rp_numbers(self, current_hits_df):
        return current_hits_df.rpID.unique().tolist()
