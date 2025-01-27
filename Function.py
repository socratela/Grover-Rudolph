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

def calcular_theta(n, f_instance, discrete=False):
    """
    Calcula un conjunto de valores theta a partir de una función a integrar y una malla generada.

    Parámetros:
    - n (int): Número de niveles de la malla. Determina cuántos valores de theta calcular.
    - f_instance (función): Función que se utilizará para calcular las integrales numéricas.
    - discrete (bool): Indica si se utiliza un enfoque discreto para los cálculos.

    Devuelve:
    - result (lista de listas): Una lista que contiene sublistas de valores de theta calculados en cada nivel.
    """
    result = []  # Lista principal que contendrá las sublistas de resultados

    if not discrete:
        for l in range(1, n + 1):
            malla = Utils.generar_puntos(l)  # Genera la malla para el nivel l
            thetas = []  # Sublista para almacenar los valores de theta en el nivel l

            for i in range(2**(l - 1)):
                # Calcula las integrales en los intervalos correspondientes
                num = f_instance([malla[2 * i], malla[2 * i + 1]], integral=True)
                denom = f_instance([malla[2 * i], malla[2 * i + 2]], integral=True)

                # Calcula theta usando la función arco coseno
                if denom == 0:
                    thetal = np.pi / 2 if malla[2 * i] == 0 else 0
                else:
                    thetal = np.arccos(np.sqrt(num / denom))

                # Añade el valor de theta a la sublista
                thetas.append(thetal)

            # Añade la sublista de valores de theta al resultado
            result.append(thetas)
        return result

    else:
        for l in range(1, n + 1):
            thetas = []  # Sublista para almacenar los valores de theta en el nivel l
            dist_num = 2**(n - l)
            dist_denom = 2**(n - l + 1)

            for i in range(2**(l - 1)):
                if l == n:
                    # Calcula la integral numérica para el caso especial en el último nivel
                    num = f_instance([i * dist_num], integral=True)
                else:
                    # Calcula las integrales en los intervalos correspondientes
                    num = f_instance([i * dist_num, (i + 1) * dist_num - 1], integral=True)
                denom = f_instance([i * dist_denom, (i + 1) * dist_denom - 1], integral=True)

                # Calcula theta usando la función arco coseno
                if denom == 0:
                    thetal = np.pi / 2 if i * dist_num == 0 else 0
                else:
                    thetal = np.arccos(np.sqrt(num / denom))

                # Añade el valor de theta a la sublista
                thetas.append(thetal)

            # Añade la sublista de valores de theta al resultado
            result.append(thetas)
        return result       