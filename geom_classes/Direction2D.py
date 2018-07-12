class Direction:
    '''
    Wektor jednostkowy
    '''

    def __init__(self, dx=1.0, dy=0.0):
        self.dx = dx
        self.dy = dy

    def __repr__(self):
        return "dx = {}\tdy={}".format(self.dx, self.dy)

    def get_perpendicular(self):
        return Direction(self.dy, -self.dx)