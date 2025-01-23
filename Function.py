# This file contains the definition of the function and its integral.
import numpy as np

class Function:
    """
    This class is used to define a function and its integral.
    Usage:
    f = Function(function, integral)

    where function is the primary function and integral is its integral.
    """
    def __init__(self, function, integral=None):
        self.f = function
        self.f_i = integral

    def __call__(self, x, integral=False):
        if integral:
            if self.f_i is None:
                raise ValueError("Integral function not defined")
            elif isinstance(x, list) or isinstance(x, np.ndarray):
                if len(x) != 2:
                    raise ValueError("For definite integrals, x must be a list or array with two elements [a, b].")
                return self.f_i(x[1]) - self.f_i(x[0])
            else:
                return self.f_i(x)
        return [self.f(i) for i in x] if isinstance(x, (list, np.ndarray)) else self.f(x)


# Example functions
def f(x):
    if isinstance(x, (list, np.ndarray)):
        sol = []
        for i in x:
            if 0 <= i < 0.5:
                sol.append(4 * i)
            else:
                sol.append(4 - 4 * i)
        return np.array(sol)
    else:
        if 0 <= x < 0.5:
            return 4 * x
        else:
            return 4 - 4 * x


def f_i(x):
    if isinstance(x, (list, np.ndarray)):
        if len(x) != 2:
            raise ValueError("x must be a list or array with two elements [a, b].")
        x0, x1 = x
        if 0 <= x0 <= 0.5 and 0 <= x1 <= 0.5:
            return 2 * x1**2 - 2 * x0**2
        elif 0 <= x0 <= 0.5 and 0.5 <= x1 <= 1:
            return 4 * x1 - 2 * x1**2 - 2 * x0**2 - 1
        else:
            return 4 * x1 - 2 * x1**2 - 4 * x0 + 2 * x0**2
    else:
        if 0 <= x <= 0.5:
            return 2 * x**2
        else:
            return 4 * x - 2 * x**2 - 1


# Instantiate the Function class
f_instance = Function(f, f_i)

# Test examples
x_values = [0.2, 0.4, 0.6, 0.8]
print(f_instance(x_values))  # Evaluating f(x)
print(f_instance([0, 1], integral=True))  # Evaluating the definite integral


