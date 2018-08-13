from df_utility.HitLinesProvider import *
from df_utility.DFProvider import *
from df_utility.ResultDFUtility import normalize
from geom_classes.Point3D import *
from hansa.HansaSolutionCollector import *

'''
THEORY:
    U_LINES - ODD  NUMBERS OF SILICON_ID (1,3,5,7,9)
    V_LINES - EVEN NUMBERS OF SILICON_ID (0,2,4,6,8)
'''

V_DIRECTION = 'v'
U_DIRECTION = 'u'

hansa_solution_collector = HansaSolutionCollector()


def get_rp_row_df(rp_id):
    return rp_df.loc[(rp_df['rpID'] == rp_id)].iloc[0]


def get_avg_det_row_df(rp_id):
    return avg_det_df.loc[(avg_det_df['rpID'] == rp_id)].iloc[0]


def get_hit_in_direction_row_df(rp_id, current_hits_df, direction=V_DIRECTION):

    if direction == V_DIRECTION:
        parity = 0
    else:
        parity = 1

    hit_in_direction_row_df = current_hits_df.loc[
            (current_hits_df['rpID'] == rp_id) &
            (current_hits_df['siliconID'] % 2 == parity)
        ].iloc[0]

    return hit_in_direction_row_df


# TODO: think about translations. For now it is real z.
def get_rp_z0_mm(rp_id):
    rp_row_df = get_rp_row_df(rp_id)
    return rp_row_df['z'] * 1000


def get_x0_y0_dirdx_dirdy_mm(rp_id, direction='v'):
    avg_det_row_df = get_avg_det_row_df(rp_id)
    x0 = avg_det_row_df['x']
    y0 = avg_det_row_df['y']

    rd_dx_label = direction + '_dx'
    rd_dy_label = direction + '_dy'
    readout_dx = avg_det_row_df[rd_dx_label]
    readout_dy = avg_det_row_df[rd_dy_label]

    return x0, y0, readout_dx, readout_dy

def get_a_b0(rp_id, current_hits_df, direction=V_DIRECTION):
    hit_in_direction_row_df = get_hit_in_direction_row_df(rp_id, current_hits_df, direction=direction)
    a = hit_in_direction_row_df['uv_line_a']
    b0 = hit_in_direction_row_df['uv_line_b']
    return a, b0


# MUSIMY OZNACZYĆ PUNKTY W ŚRODKU UKŁADU WSPÓŁRZĘDNYCH
'''
PUNKTY:
    - x0, y0, z0            - środek układu współrzędnych
    - p0_x, p0_y, p0_z      - Punkt na wysokości b0, w odciętej z0 (I współrzędna) w układzie [V|U]z
    - p1_x, p1_y, p1_z      - Punkt na wysokości b1, w odciętej z0 + 1.0
    - pt0 - punkt odtworzonego tracka w z0
    - pt1 - punkt odtworzonego tracka w z1
    - pc0 - center of Hansa coordinate system
'''

def get_dz(z0):
    dz = 1.0 * np.sign(z0)
    return dz


def get_b1(a, b0, z0):
    dz = get_dz(z0)
    b1 = a * dz + b0   # tu może być błąd bo to moje a jest w [u_rad] --> to należy naprawić, ale będą jaja
    return b1


def get_p0(x0, y0, z0, readout_dx, readout_dy, b0):
    p0_x = x0 + readout_dx * b0
    p0_y = y0 + readout_dy * b0
    p0_z = z0

    return p0_x, p0_y, p0_z


def get_p1(x0, y0, z0, readout_dx, readout_dy, b1):
    dz = get_dz(z0)

    p1_x = x0 + readout_dx * b1
    p1_y = y0 + readout_dy * b1
    p1_z = z0 + dz

    return p1_x, p1_y, p1_z


def get_global_dx_dy_dz(p0_x, p0_y, p0_z, p1_x, p1_y, p1_z):
    dx = p1_x - p0_x
    dy = p1_y - p0_y
    dz = p1_z - p0_z

    return normalize(dx, dy, dz)


def get_direction_projection_line(rp_id, current_hits_df, direction=V_DIRECTION):
    '''
    :param rp_id:
    :return: Line(x,y,z,dx,dy,dz) of projected line

    STEPS:
        rp_geom_df          - z
        avg_det_geom_df     - x, y, readout_dx, readout_dy
        current_hits_df     - a, b
    '''

    z0                              = get_rp_z0_mm(rp_id)
    x0, y0, readout_dx, readout_dy  = get_x0_y0_dirdx_dirdy_mm(rp_id, direction)
    a, b0                           = get_a_b0(rp_id, current_hits_df, direction=direction)
    b1                              = get_b1(a, b0, z0)

    p0_x, p0_y, p0_z                = get_p0(x0, y0, z0, readout_dx, readout_dy, b0)
    p1_x, p1_y, p1_z                = get_p1(x0, y0, z0, readout_dx, readout_dy, b1)

    p0 = Point3D(p0_x, p0_y, p0_z)
    p1 = Point3D(p1_x, p1_y, p1_z)

    # This violates law that method does exactly one well defined thig
    return p0, p1, readout_dx, readout_dy, b0, b1, a


def get_pc0(rp_id, direction=V_DIRECTION):
    z0 = get_rp_z0_mm(rp_id)
    x0, y0, readout_dx, readout_dy = get_x0_y0_dirdx_dirdy_mm(rp_id, direction)
    pc0 = Point3D(x0, y0, z0)

    return pc0


def get_pc1(pc0):
    pc1_x = pc0.x
    pc1_y = pc0.y
    pc1_z = pc0.z + 1.0 * np.sign(pc0.z)

    pc1 = Point3D(pc1_x, pc1_y, pc1_z)
    return pc1


def get_pt(pu, v_b, v_dx, v_dy):
    '''
    :param p_u:     point track projection in Uz plane
    :param v_b:
    :param v_dx:    direction of Vz
    :param v_dy:
    :return:
    '''
    pt_x = pu.x + v_dx * v_b
    pt_y = pu.y + v_dy * v_b
    pt_z = pu.z

    pt = Point3D(pt_x, pt_y, pt_z)
    return pt


def get_hansa_track_line(rp_id, current_hits_df):
    '''
    NOTE THAT THESE LINES DOES NOT HAVE SAME P0
    WE ASSUME THAT READOUT DIRECTIONS ARE PERPENDICULAR

    I need:
        x0, y0, z0

    :param rp_id:
    :param current_hits_df:
    :return:
    '''

    p_u0, p_u1, u_dx, u_dy, u_b0, u_b1, u_a = get_direction_projection_line(rp_id, current_hits_df, direction=U_DIRECTION)
    p_v0, p_v1, v_dx, v_dy, v_b0, v_b1, v_a = get_direction_projection_line(rp_id, current_hits_df, direction=V_DIRECTION)

    pc0 = get_pc0(rp_id)
    pc1 = get_pc1(pc0)

    pt0 = get_pt(p_u0, v_b0, v_dx, v_dy)
    pt1 = get_pt(p_u1, v_b1, v_dx, v_dy)

    t_dx = pt1.x - pt0.x
    t_dy = pt1.y - pt0.y
    t_dz = pt1.z - pt0.z

    points_0 = [pc0, p_u0, p_v0, pt0]
    points_1 = [pc1, p_u1, p_v1, pt1]
    uv_directions = [u_dx, u_dy, v_dx, v_dy]
    track_data = [u_a, u_b0, u_b1, v_a, v_b0, v_b1]  # jej  tu nie mam informacji o tych podstawowych rzeczach... :(
    hansa_solution_collector.collect(points_0, points_1, uv_directions, track_data)

    t_dx, t_dy, t_dz = normalize(t_dx, t_dy, t_dz)

    # TODO: Fix this ugly det_id setting
    return Line(pt0.x, pt0.y, pt0.z, t_dx, t_dy, t_dz, det_id=rp_id*10)


def get_rps_numbers(current_hits_df):
    return current_hits_df.rpID.unique().tolist()


def get_hansa_solutions(hits_df, geom_df, event_id, group_id):
    '''
    :param hits_df:
    :param geom_df:
    :param event_id:
    :param group_id:
    :return:
    '''

    hansa_lines = []

    current_hits_df = get_current_hits_df(event_id, group_id, hits_df)
    rp_ids = get_rps_numbers(current_hits_df)

    for rp_id in rp_ids:
        hansa_line = get_hansa_track_line(rp_id, current_hits_df)
        hansa_lines.append(hansa_line)

    return hansa_lines