import numpy as np

class Line:
    def __init__(self, x=0, y=0, z=0, dx=0, dy=0, dz=0, point=[], direction=[], params=[], det_id=0):
        if len(params) == 6:
            self.x, self.y, self.z = params[:3]
            self.dx, self.dy, self.dz = params[3:]
        elif len(params) == 5:
            self.x, self.y = params[:2]
            self.z = z
            self.dx, self.dy, self.dz = params[2:]
        elif len(point) == 3 and len(direction) == 3:
            self.x, self.y, self.z = point
            self.dx, self.dy, self.dz = direction
        else:
            self.x, self.y, self.z = x, y, z
            self.dx, self.dy, self.dz = dx, dy, dz

        # just to make this line a detector Line
        self.det_id = int(det_id)

    def __repr__(self):
        return "Line: det = {}\t p = ({:.3f}, {:.3f}, {:.3f})\t v = [{:.3f}, {:.3f}, {:.3f}]".format(
            self.det_id, self.x, self.y, self.z, self.dx, self.dy, self.dz
        )

    def distance(self, other):
        n_vector = np.cross(self.line_vector(), other.line_vector())
        s_o_vector = np.array([self.x - other.x, self.y - other.y, self.z - other.z])
        return np.linalg.norm(np.dot(n_vector, s_o_vector)) / np.linalg.norm(n_vector)

    def line_vector(self):
        return np.array([self.dx, self.dy, self.dz])

    def y_on_x(self, x):
        return (x - self.x) / self.dx * self.dy + self.y