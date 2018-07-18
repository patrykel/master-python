from scipy.optimize import minimize     # MINIMIZATION
from scipy.optimize import least_squares
from minimization.MinimizationConfigurationProvider import *
from geom_classes.Line import Line
import time

LINE_SET = []


# OBJECTIVE FUNCTION
def objective(params):
    x, y, dx, dy, dz = params
    x = x  # * 10.0
    y = y  # * 10.0
    line = Line(x=x, y=y, dx=dx, dy=dy, dz=dz)
    return np.sum([line.distance(other) for other in LINE_SET])  # SUM OF DISTANCES


def get_by_least_squares(x0, minimize_like_bounds):
    method = 'trf (least squares method)'

    bounds = get_bounds_for_least_squares(minimize_like_bounds)

    start_time = time.time()
    solution = least_squares(objective, x0, bounds=bounds, jac='2-point', method='trf')
                             # gtol=1e-10, xtol=1e-10, ftol=1e-10)
    # solution = least_squares(objective, x0, jac='2-point', method='lm',
    #                          gtol=1e-10, xtol=1e-10, ftol=1e-10)
    exec_time = time.time() - start_time

    return solution, method, exec_time


def get_by_minimize(x0, constraints, bounds):
    optimizing_methods = get_optimizing_methods()

    start_time = time.time()

    for method in optimizing_methods:
        solution = minimize(objective, x0, method=method, constraints=constraints, bounds=bounds)

        if solution.success:
            break

    exec_time = time.time() - start_time

    return solution, method, exec_time



def get_solution_track(hit_lines, geom_df):
    global LINE_SET
    LINE_SET = hit_lines

    x0 = get_x0(hit_lines, geom_df, z_fixed=True)
    constraints = get_constraints()
    bounds = get_bounds(x0, hit_lines, geom_df)

    return get_by_least_squares(x0, bounds)
    # return get_by_minimize(x0, constraints, bounds)
    # return get_by_curve_fit(hit_lines, bounds)