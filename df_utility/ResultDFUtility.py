from geom_classes.Line import Line
from geom_classes.dets_inclusion_test import *
import numpy as np

detector_map = {
    1 : "L-TOP",
    2 : "L-BOT",
    3 : "L-HOR",
    4 : "R-TOP",
    5 : "R-BOT",
    6 : "R-HOR"
}


def get_group(group_id):
    return detector_map[group_id]


# DISTANCES
def get_distances(solution, hit_lines):
    track = Line(params=solution.x)
    return [track.distance(line) for line in hit_lines]


def get_dist_sum(solution, hit_lines):
    distances = get_distances(solution, hit_lines)
    return sum(distances)


def get_dist_max(solution, hit_lines):
    distances = get_distances(solution, hit_lines)
    return max(distances)

# CHI2
SIGMA = 0.0659 / np.sqrt(2)


def get_chi2(solution, hit_lines):
    track = Line(params=solution.x)                                                 # CREATING FITTED TRACK
    return sum([(track.distance(hit_line)/SIGMA)**2 for hit_line in hit_lines])  # SUM OF DISTANCES


def get_chi2_N(solution, hit_lines):
    return get_chi2(solution, hit_lines) / (len(hit_lines) - len(solution.x))


# TRACK PARAMETERS
ZERO_THRESHOLD = 1e-10


def normalize(dx, dy, dz):
    v = np.array([dx, dy, dz])
    return v / np.linalg.norm(v)


def get_track_params(solution):
    x, y, z, dx, dy, dz = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    if len(solution.x) == 5:
        x, y, dx, dy, dz = solution.x
        z = 0.0
    elif len(solution.x) == 6:
        x, y, z, dx, dy, dz = solution.x

    if abs(dx ** 2 + dy ** 2 + dz ** 2 - 1.0) > ZERO_THRESHOLD:
        dx, dy, dz = normalize(dx, dy, dz)

    return [x, y, z, dx, dy, dz]


# ATAN
def get_mili_rad_angle(da, dz):
    return 1000 * np.arctan(da/dz)


# INSIDE TEST
def get_det_id_list(hit_lines):
    return [line.det_id for line in  hit_lines]


def get_det_with_track_list(det_id_list, track_line, geom_df):
    return [det_id for det_id in det_id_list if det_contains_track(det_id, track_line, geom_df)]


def get_tracks_in_det_no(solution, hit_lines, geom_df):
    track_line      = Line(params=solution.x)
    det_id_list     = get_det_id_list(hit_lines)
    det_with_track  = get_det_with_track_list(det_id_list, track_line, geom_df)

    return len(det_with_track)

