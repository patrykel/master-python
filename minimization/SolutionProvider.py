from scipy.optimize import minimize     # MINIMIZATION
from minimization.MinimizationConfigurationProvider import *
from geom_classes.Line import Line
from scipy.optimize import least_squares

LINE_SET = []


# OBJECTIVE FUNCTION
def objective(params):
    line = Line(params=params)
    # print(len(LINE_SET))
    # print([line.distance(other) for other in LINE_SET])
    return np.sum([line.distance(other) for other in LINE_SET])  # SUM OF DISTANCES



def get_by_least_squares(x0):
    method = 'trf (least squares method)'
    solution = least_squares(objective, x0, jac='2-point', method='trf')

    return solution, method


def get_by_minimize(x0, constraints, bounds):
    optimizing_methods = get_optimizing_methods()
    for method in optimizing_methods:
        solution = minimize(objective, x0, method=method, constraints=constraints, bounds=bounds)

        if solution.success:
            break

    return solution, method



def get_solution_track(hit_lines, geom_df):
    global LINE_SET
    LINE_SET = hit_lines

    x0 = get_x0(hit_lines, geom_df, z_fixed=True)
    constraints = get_constraints()
    bounds = get_bounds(x0, hit_lines, geom_df)

    return get_by_least_squares(x0)
    # return get_by_minimize(x0, constraints, bounds)