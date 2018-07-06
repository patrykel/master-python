import numpy as np

RP_SILICON_SIDE = 36.07                                         # side length of plane detector [mm]
HALF_RP_SILICON_DIAGONAL = 0.5 * RP_SILICON_SIDE * np.sqrt(2.0) # half of diagonal length of plane detector [mm]


def get_first_plane_id(hit_lines):
    return min([line.det_id for line in hit_lines])


def get_first_plane_info(hit_lines, geom_df):
    first_plane_id = get_first_plane_id(hit_lines)
    return geom_df.loc[(geom_df['detId'] == first_plane_id)].iloc[0]


def get_first_plane_parameter(hit_lines, geom_df, parameter='x'):
    first_plane_info = get_first_plane_info(hit_lines, geom_df)
    return first_plane_info[parameter]


def get_x0(hit_lines, geom_df, z_fixed=True):
    plane_info = get_first_plane_info(hit_lines, geom_df)

    x = plane_info['x']
    y = plane_info['y']
    z = 0.0                 # (as we translated) plane_info['z']
    dx = 0.009999749997
    dy = 0.009999749997
    dz = 0.9999

    if z_fixed:
        return [x, y, dx, dy, dz]
    else:
        return[x, y, z, dx, dy, dz]


def get_constraints():
    def constraint1(params):
        return 1.0 - np.sum([di ** 2 for di in params[-3:]])  # dx^2 + dy^2 + dz^2 = 1 (params = [..., dx, dy, dz])

    con1 = {'type': 'eq', 'fun': constraint1}
    return [con1]


def get_x_bound(hit_lines, geom_df):
    x = get_first_plane_parameter(hit_lines, geom_df, 'x')
    return (x - HALF_RP_SILICON_DIAGONAL, x + HALF_RP_SILICON_DIAGONAL)


def get_y_bound(hit_lines, geom_df):
    y = get_first_plane_parameter(hit_lines, geom_df, 'y')
    return (y - HALF_RP_SILICON_DIAGONAL, y + HALF_RP_SILICON_DIAGONAL)


def get_bounds(seed_solution, hit_lines, geom_df):
    b_x = get_x_bound(hit_lines, geom_df)  # det_center.x +/- RPSilicon.A * sqrt(2)
    b_y = get_y_bound(hit_lines, geom_df)  # det_center.y +/- RPSilicon.A * sqrt(2)
    b_z = (-1.0, 1.0)
    b_dir = (-1.0, 1.0)


    if len(seed_solution) == 6:
        result = [b_x, b_y, b_z, b_dir, b_dir, b_dir]
    if len(seed_solution) == 5:
        result = [b_x, b_y, b_dir, b_dir, b_dir]

    return result

def get_optimizing_methods():
    return ['SLSQP', 'Nelder-Mead', 'Powell']