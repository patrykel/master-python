class RPSilicon:
    A = 36.07  # side length [mm]
    E = 22.276  # edge length [mm]

    d_T = Point2D(A / 2.0, A / 2.0)  # T
    d_L = Point2D(-A / 2.0, A / 2.0)  # L
    d_R = Point2D(A / 2.0, -A / 2.0)  # R
    d_EL = Point2D(-A / 2.0, -A / 2.0 + E / np.sqrt(2))  # EL
    d_ER = Point2D(-A / 2.0 + E / np.sqrt(2), -A / 2.0)  # ER

    RP_Det_Fid_Top_a = 0.301  # [mm]
    RP_Det_Fid_Top_b = 1.0275  # [mm]
    RP_Det_Fid_Left_a = 0.301  # [mm]
    RP_Det_Fid_Left_c = 0.2985  # [mm]
    RP_Det_Fid_Right_b = 1.0275  # [mm]
    RP_Det_Fid_Right_d = 1.0255  # [mm]

    RP_Det_dx_0 = (RP_Det_Fid_Left_c - RP_Det_Fid_Right_b) / 2.0  # [mm]
    RP_Det_dy_0 = (RP_Det_Fid_Right_d - RP_Det_Fid_Left_a) / 2.0  # [mm]

    def __init__(self, center, direction, siId, T=d_T, L=d_L, R=d_R, EL=d_EL, ER=d_ER):
        self.center = center
        self.direction = direction
        self.siId = siId

        self.T = copy.deepcopy(T)
        self.L = copy.deepcopy(L)
        self.R = copy.deepcopy(R)
        self.EL = copy.deepcopy(EL)
        self.ER = copy.deepcopy(ER)
        self.points = [self.R, self.T, self.L, self.EL, self.ER]  # In sequence

        # MOVE DETECTOR POINTS
        self.move(Vector2D(self.center.x, self.center.y), self.points)  # general position

        # ROTATE AROUND CENTER
        rot_direction = self.get_rot_direction()
        self.rotate_around_center(self.points, rot_direction)

        ##################################
        # NOW WE CAN SET FIDUCIAL POINTS #
        ##################################
        self.fid_center = copy.deepcopy(self.center)
        self.fid_center.move(Vector2D(RPSilicon.RP_Det_dx_0, RPSilicon.RP_Det_dy_0))
        self.fid_center.rotate_around_point(self.center, self.get_rot_direction())

        self.fid_T = copy.deepcopy(T)
        self.fid_L = copy.deepcopy(L)
        self.fid_R = copy.deepcopy(R)
        self.fid_EL = copy.deepcopy(EL)
        self.fid_ER = copy.deepcopy(ER)

        self.fid_T.move(Vector2D(-RPSilicon.RP_Det_Fid_Top_b, -RPSilicon.RP_Det_Fid_Top_a))
        self.fid_L.move(Vector2D(RPSilicon.RP_Det_Fid_Left_c, -RPSilicon.RP_Det_Fid_Left_a))
        self.fid_R.move(Vector2D(-RPSilicon.RP_Det_Fid_Right_b, RPSilicon.RP_Det_Fid_Right_d))
        self.fid_EL.move(Vector2D(RPSilicon.RP_Det_Fid_Left_c, -RPSilicon.RP_Det_Fid_Left_c))
        self.fid_ER.move(Vector2D(-RPSilicon.RP_Det_Fid_Right_d, RPSilicon.RP_Det_Fid_Right_d))

        self.fid_points = [self.fid_R, self.fid_T, self.fid_L, self.fid_EL, self.fid_ER]

        self.move(Vector2D(self.center.x, self.center.y), self.fid_points)
        self.rotate_around_center(self.fid_points, rot_direction)

    def get_rot_direction(self):
        arm = int(self.siId / 1000)
        if arm == 0 and self.siId % 2 == 0:
            return self.direction
        elif arm == 0 and self.siId % 2 == 1:
            return Direction(self.direction.dy, -self.direction.dx)
        elif arm == 1 and self.siId % 2 == 0:
            return Direction(self.direction.dy, -self.direction.dx)
        else:
            return self.direction

    def contains(self, P):
        ''' check if detector plane contains point P'''
        det_square_points = self.get_det_square_points()
        det_missing_triangle_points = self.get_missing_triangle_points()

        return inside_rect(det_square_points, P) and not inside_triangle(det_missing_triangle_points, P)

    def get_det_square_points(self):
        TL = Vector2D(start=self.T, end=self.L)
        r_B = copy.deepcopy(self.R)  # BOTTOM point
        r_B.move(TL)

        r_T = copy.deepcopy(self.T)
        r_L = copy.deepcopy(self.L)
        r_R = copy.deepcopy(self.R)

        return np.array([r_T, r_L, r_B, r_R])  # TOP, LEFT, BOTTOM, RIGHT

    def get_missing_triangle_points(self):
        TL = Vector2D(start=self.T, end=self.L)
        r_B = copy.deepcopy(self.R)  # BOTTOM point
        r_B.move(TL)

        r_EL = copy.deepcopy(self.EL)
        r_ER = copy.deepcopy(self.ER)

        return np.array([r_B, r_EL, r_ER])

    def __repr__(self):
        return "T = {} \nL = {} \nR = {} \nEL = {}\nER = {}".format(self.T, self.L, self.R, self.EL, self.ER)

    def move(self, vector, points):
        for p in points:
            p.move(vector)

    def rotate_around_center(self, points, direction):
        for p in points:
            p.rotate_around_point(self.center, direction)

    def add_polygon_to_plot(self, ax, polygon_points, polygon_color):
        np_points = np.append(polygon_points, polygon_points[0])

        x = np.array([p.x for p in np_points])
        y = np.array([p.y for p in np_points])

        starts = [[x[i], y[i]] for i in range(len(x) - 1)]
        ends = [[x[i + 1], y[i + 1]] for i in range(len(y) - 1)]
        rp_segments = np.array(list(zip(starts, ends)))
        polygon_colors = np.full((len(polygon_points), 4), polygon_color)

        rp_line_segments = LineCollection(rp_segments, colors=polygon_colors, linewidths=0.5)
        ax.add_collection(rp_line_segments)

    def add_point_to_plot(self, point, alpha=0.5):
        x = [point.x]
        y = [point.y]

        ax.plot(x, y, 'ok', markersize=2, alpha=alpha)

    def add_to_plot(self, ax, distances, rp_color=[0, 0, 0, 1], hit_color=[1, 0, 0, 1]):

        # PLOTTING SILICON DETECTOR
        self.add_polygon_to_plot(ax, self.points, rp_color)
        self.add_polygon_to_plot(ax, self.fid_points, [1, 0, 0, 1])

        # PLOTTING CENTER POINT
        self.add_point_to_plot(self.center, alpha=0.1)
        self.add_point_to_plot(self.fid_center, alpha=0.5)

        # PLOTTING HIT LINES
        hit_segments = [HitSegment(d, self).get_segment() for d in distances]
        hit_colors = np.full((len(distances), 4), hit_color)

        hit_lines = LineCollection(hit_segments, colors=hit_colors, linewidths=0.5)
        ax.add_collection(hit_lines)