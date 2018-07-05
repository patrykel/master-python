from scipy.optimize import minimize     # MINIMIZATION
from minimization.MinimizationConfigurationProvider import *
from geom_classes.Line import Line

LINE_SET = []


# OBJECTIVE FUNCTION
def objective(params):
    line = Line(params=params)
    return np.sum([line.distance(other) for other in LINE_SET])  # SUM OF DISTANCES


def get_solution_track(hit_lines, geom_df):
    LINE_SET = hit_lines

    x0 = get_x0(hit_lines, geom_df, z_fixed=True)
    constraints = get_constraints()
    bounds = get_bounds(x0, hit_lines, geom_df)
    optimizing_methods = get_optimizing_methods()

    for method in optimizing_methods:
        solution = minimize(objective, x0, method=method, constraints=constraints, bounds=bounds)

        if solution.success:
            print("Success method: {}".format(method))
            x = get_first_plane_parameter(hit_lines, geom_df, 'x')
            y = get_first_plane_parameter(hit_lines, geom_df, 'y')
            print("First det center: x = {}, y = {}".format(x, y))
            print()
            break

    return solution