from scipy.optimize import minimize     # MINIMIZATION
from scipy.optimize import least_squares
from minimization.MinimizationConfigurationProvider import *
from geom_classes.Line import Line
import time

LINE_SET = []

# OBJECTIVE FUNCTION
def objective(params):
    line = Line(params=params)
    return np.sum([line.distance(other) for other in LINE_SET])  # SUM OF DISTANCES


def get_bounds_for_least_squares(minimize_like_bounds):
    lower_bounds = []
    upper_bounds = []

    for bound in minimize_like_bounds:
        lower_bounds.append(bound[0])
        upper_bounds.append(bound[1])

    bounds = (lower_bounds, upper_bounds)

    return bounds


def get_by_least_squares(x0, minimize_like_bounds):
    method = 'trf (least squares method)'

    bounds = get_bounds_for_least_squares(minimize_like_bounds)

    start_time = time.time()
    solution = least_squares(objective, x0, bounds=bounds, jac='2-point', method='trf')
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