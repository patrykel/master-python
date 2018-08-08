'''
t0 - track point in center of RP (z - same as RP center)
c0 - center of RP and Uz Vz coordinate systems (in global x,y,z)
pu0 - projection of t0 in Uz
pv0 - projection of t0 in Vz
[u|v]_[dx|dy] - direction U and V
[u|v]_b[1|2] - track projection b in Uz and Vz

'''

t0_column_names = ['c0_x', 'c0_y', 'c0_z',
                   'pu0_x', 'pu0_y', 'pu0_z',
                   'pv0_x', 'pv0_y', 'pv0_z',
                   'pt0_x', 'pt0_y', 'pt0_z',
                   'u_dx', 'u_dy',
                   'v_dx', 'v_dy',
                   'u_b0', 'v_b0']

t1_column_names = ['c1_x', 'c1_y', 'c1_z',
                   'pu1_x', 'pu1_y', 'pu1_z',
                   'pv1_x', 'pv1_y', 'pv1_z',
                   'pt1_x', 'pt1_y', 'pt1_z',
                   'u_dx', 'u_dy',
                   'v_dx', 'v_dy',
                   'u_b1', 'v_b1']

track_data_column_names = ['u_a', 'u_b0', 'u_b1',
                           'v_a', 'v_b0', 'v_b1']


def get_t0_column_names():
    return t0_column_names


def get_t1_column_names():
    return t1_column_names


def get_track_data_column_names():
    return track_data_column_names
