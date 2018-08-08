from hansa.HansaSolutionColumnNames import *
from df_utility.DFUtility import *

'''
If you are curious what HansaSolutionCollector stores
please visit hansa.HansaSolutionColumnNames
'''

class HansaSolutionCollector():
    def __init__(self):
        self.t0_data2D = []
        self.t1_data2D = []
        self.track_data2D = []

    def collect(self, points_0, points_1, uv_directions, track_data):
        t0_data = self.get_points(points_0) + uv_directions
        t1_data = self.get_points(points_1) + uv_directions

        self.t0_data2D.append(t0_data)
        self.t1_data2D.append(t1_data)

    def get_points(self, points_arr):
        points_data = []

        for p in points_arr:
            points_data = points_data + [p.x, p.y, p.z]

        return points_data

    def get_t0_df(self):
        t0_column_names = get_t0_column_names()
        t0_df = get_df(self.t0_data2D, t0_column_names)
        return t0_df

    def get_t1_df(self):
        t1_column_names = get_t1_column_names()
        t1_df = get_df(self.t1_data2D, t1_column_names)
        return t1_df

    def get_track_df(self):
        track_data_column_names = get_track_data_column_names()
        track_df = get_df(self.track_data2D, track_data_column_names)
        return track_df
