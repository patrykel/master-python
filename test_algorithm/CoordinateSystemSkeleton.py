
import numpy as np
import math
from geom_classes.Point3D import *
from test_algorithm.DeterminantsEquation2D import *

V_DIRECTION = 'v'
U_DIRECTION = 'u'

DIRECTION_PARITY = {
    V_DIRECTION : 0,
    U_DIRECTION : 1
}


class CoordinateSystemSkeleton():

    def __init__(self):
        self.reset()

    def reset(self):
        # Line representing projections of Track to Uz and Vz planes
        self.line_u_a = None
        self.line_u_b = None
        self.line_v_a = None
        self.line_v_b = None

        # U|V Readout directions
        self.u_dx = None
        self.u_dy = None
        self.v_dx = None
        self.v_dy = None

        # Beginnings of Uz Vz coordinate systems
        self.z = None
        self.u_c0 = None    # Point3D
        self.v_c0 = None    # Point3D

        #Computed stuff
        self.c0 = None
        self.b_u0 = None
        self.b_v0 = None
        self.b_u1 = None
        self.b_v1 = None
        

    def setup(self, rp_id, rp_hits_df, det_avg_geom_df, rp_geom_df):
        self.reset()
        self.setup_lines(rp_id, rp_hits_df)
        self.setup_directions(rp_id, det_avg_geom_df)
        self.setup_rp_z(rp_id, rp_geom_df)
        self.setup_coordinate_systems_centers(rp_id, det_avg_geom_df)

        # compute
        self.c0 = self.compute_c0()
        self.c1 = self.compute_c1()
        self.compute_b_uv_0()
        self.compute_b_uv_1()
        self.compute_pt0()
        self.compute_pt1()
        

    def setup_lines(self, rp_id, rp_hits_df):
        u_direction_row_df = rp_hits_df.loc[rp_hits_df['siliconID'] % 2 == DIRECTION_PARITY[U_DIRECTION]].iloc[0]
        v_direction_row_df = rp_hits_df.loc[rp_hits_df['siliconID'] % 2 == DIRECTION_PARITY[V_DIRECTION]].iloc[0]

        self.line_u_a = u_direction_row_df['uv_line_a']
        self.line_u_b = u_direction_row_df['uv_line_b']

        self.line_v_a = v_direction_row_df['uv_line_a']
        self.line_v_b = v_direction_row_df['uv_line_b']


    def setup_directions(self, rp_id, det_avg_geom_df):
        u_det_avg_df = det_avg_geom_df.loc[(det_avg_geom_df['rpId'] == rp_id) &
                                           (det_avg_geom_df['direction'] == U_DIRECTION)].iloc[0]

        v_det_avg_df = det_avg_geom_df.loc[(det_avg_geom_df['rpId'] == rp_id) &
                                           (det_avg_geom_df['direction'] == V_DIRECTION)].iloc[0]

        self.u_dx = u_det_avg_df['dx']
        self.u_dy = u_det_avg_df['dy']

        self.v_dx = v_det_avg_df['dx']
        self.v_dy = v_det_avg_df['dy']


    def setup_rp_z(self, rp_id, rp_geom_df):
        rp_row_df = rp_geom_df.loc[rp_geom_df['rpID'] == rp_id].iloc[0]
        self.rp_z = rp_row_df['z'] * 1000 # [mm]


    def setup_coordinate_systems_centers(self, rp_id, det_avg_geom_df):
        u_det_avg_df = det_avg_geom_df.loc[(det_avg_geom_df['rpId'] == rp_id) &
                                           (det_avg_geom_df['direction'] == U_DIRECTION)].iloc[0]

        v_det_avg_df = det_avg_geom_df.loc[(det_avg_geom_df['rpId'] == rp_id) &
                                           (det_avg_geom_df['direction'] == V_DIRECTION)].iloc[0]

        self.u_c0 = Point3D(u_det_avg_df['x'], u_det_avg_df['y'], u_det_avg_df['z'])
        self.v_c0 = Point3D(v_det_avg_df['x'], v_det_avg_df['y'], v_det_avg_df['z'])


    def compute_c0(self):
        '''
        We compute c0 by crammers rule

        Given two lines:
        l1:  ( x1 ) + a ( u1)  // linia u       l2:  ( x2 ) + b ( u2)  // linia v
             ( y1 ) + a ( v1)                        ( y2 ) + b ( v2)

        [ u1  -u2] * [ a ] = [ x2 - x1 ]
        [ v1  -v2]   [ b ]   [ y2 - y1 ]

        COMPLY TO THAT:
        | a1 b1 | * | x | = | c1 |        -    x --> k_u
        | a2 b2 |   | y |   | c2 |        -    y --> k_v
        '''

        mapping = {
            'x1': self.u_c0.x, 'x2': self.v_c0.x,
            'y1': self.u_c0.y, 'y2': self.v_c0.y,
            'u1': self.u_dx,   'u2': self.v_dx,
            'v1': self.u_dy,   'v2': self.v_dy,
        }

        a1 = mapping['u1']
        b1 = - mapping['u2']
        c1 = mapping['x2'] - mapping['x1']

        a2 = mapping['v1']
        b2 = - mapping['v2']
        c2 = mapping['y2'] - mapping['y1']

        equation = DeterminantsEquation2D(a1, b1, c1, a2, b2, c2)
        k_u, k_v = equation.compute_solution()

        c0_x = self.u_c0.x + k_u * self.u_dx
        c0_y = self.u_c0.y + k_u * self.u_dy
        c0_z = self.u_c0.z

        return Point3D(c0_x, c0_y, c0_z)

    def compute_c1(self):
        c1_x = self.c0.x
        c1_y = self.c0.y
        c1_z = self.c0.z + 1.0 * np.sign(self.c0.z)
        
        return Point3D(c1_x, c1_y, c1_z)

    def compute_b_uv_0(self):
        # b_u0 - distance between C0 and place indicated by self.b_u0
        self.b_u0 = self.line_u_b + (self.u_c0.x - self.c0.x) / self.u_dx
        self.b_v0 = self.line_v_b + (self.v_c0.x - self.c0.x) / self.v_dx

    def compute_b_uv_1(self):
        # b_u1 - distance between C1 and point on U axis on Uz1 plane, 
        # b_v1 - distance between C1 and point on V axis on Vz1 plane

        self.b_u1 = self.b_u0 + math.tan(self.line_u_a) * 1 # tangens - real a
        self.b_v1 = self.b_v0 + math.tan(self.line_v_a) * 1 # tangens

    def compute_pt0(self):
        pt0_x = self.c0.x + self.b_u0 * self.u_dx + self.b_v0 * self.v_dx
        pt0_y = self.c0.y + self.b_u0 * self.u_dy + self.b_v0 * self.v_dy
        pt0_z = self.c0.z
        
        self.pt0 = Point3D(pt0_x, pt0_y, pt0_z)

    def compute_pt1(self):
        pt1_x = self.c1.x + self.b_u1 * self.u_dx + self.b_v1 * self.v_dx
        pt1_y = self.c1.y + self.b_u1 * self.u_dy + self.b_v1 * self.v_dy
        pt1_z = self.c1.z

        self.pt1 = Point3D(pt1_x, pt1_y, pt1_z)

    def get_pt0(self):
        return self.pt0

    def get_pt1(self):
        return self.pt1
