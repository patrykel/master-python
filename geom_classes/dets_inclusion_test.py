from geom_classes.Point2D import Point2D
from geom_classes.Direction2D import Direction
from geom_classes.RPSilicon import RPSilicon
from geom_classes.GlobalZTranslation import GlobalZTranslation


# GETTING RP SILICON INSTANCE
def get_plane_info(det_id, geom_df):
    return geom_df.loc[(geom_df['detId'] == det_id)].iloc[0]


def get_plane_center(plane_info):
    return Point2D(x=plane_info['x'], y=plane_info['y'])


def get_plane_readout_direction(plane_info):
    return Direction(dx=plane_info['dx'], dy=plane_info['dy'])


def get_rp_silicon(det_id, geom_df):
    plane_info              = get_plane_info(det_id, geom_df)
    plane_center            = get_plane_center(plane_info)
    plane_readout_direction = get_plane_readout_direction(plane_info)

    return RPSilicon(plane_center, plane_readout_direction, det_id)


# GETTING POINT WHERE SILICON WAS HIT BY TRACK


def get_delta_z_to_first_plane(det_id, geom_df):
    plane_info = get_plane_info(det_id, geom_df)
    return plane_info['z'] * 1000 - GlobalZTranslation.FIRST_DET_Z_IN_MM


def get_track_silicon_hit_point(det_id, track_line, geom_df):
    delta_z_to_first_plane = get_delta_z_to_first_plane(det_id, geom_df)

    k = delta_z_to_first_plane / track_line.dz

    p = Point2D()
    p.x = track_line.x + k * track_line.dx
    p.y = track_line.y + k * track_line.dy

    return p


def det_contains_track(det_id, track_line, geom_df):

    rp_silicon              = get_rp_silicon(det_id, geom_df)
    track_silicon_hit_point = get_track_silicon_hit_point(det_id, track_line, geom_df)

    return rp_silicon.contains(track_silicon_hit_point)


