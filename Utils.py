import numpy as np
import matplotlib as plt
from qiskit import QuantumCircuit,ClassicalRegister,QuantumRegister, transpile
from qiskit.circuit.library import UnitaryGate, RYGate
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import pandas as pd

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

class Utils:
    @staticmethod
    def f(x):
        sol = []
        for i in range(len(x)):
            if 0 <= x[i] < 0.5:
                sol.append(4 * x[i])
            else:
                sol.append(4 - 4 * x[i])
        return np.array(sol)

    @staticmethod
    def int_f(x):
        if 0 <= x[0] <= 0.5 and 0 <= x[1] <= 0.5:
          return 2 * x[1]**2 - 2 * x[0]**2
        elif 0 <= x[0] <= 0.5 and 0.5 <= x[1] <= 1:
            return 4 * x[1] - 2 * x[1]**2 - 2 * x[0]**2 - 1
        else:
            return 4 * x[1] - 2 * x[1]**2 - 4 * x[0] + 2 * x[0]**2 

    @staticmethod
    def generar_puntos(n):
        """
        Genera una lista de puntos en el intervalo [0, 1] con una amplitud de 1/2^n.
        
        :param n: El valor de n que determina la amplitud 1/2^n.
        :return: Una lista de puntos.
        """
        amplitud = 1 / 2**n
        puntos = [i * amplitud for i in range(2**n + 1)]
        return puntos

    @staticmethod
    def calcular_theta(n, f_instance):
        """
        Calcula un conjunto de valores theta a partir de una función a integrar y una malla generada.
        
        Parámetros:
        - n (int): Número de niveles de la malla. Determina cuántos valores de theta calcular.
        - funcion_a_integrar (función): Función que se utilizará para calcular las integrales numéricas.
        
        Devuelve:
        - result (lista de listas): Una lista que contiene sublistas de valores de theta calculados en cada nivel.
        """
        result = []  # Lista principal que contendrá las sublistas de resultados
        
        for l in range(1, n + 1):
            malla = Utils.generar_puntos(l)  # Genera la malla para el nivel l
            thetas = []  # Sublista para almacenar los valores de theta en el nivel l
            
            for i in range(2**(l - 1)):
                # Calcula las integrales en los intervalos correspondientes
                num = f_instance([malla[2 * i],malla[2 * i +1]],integral = True)
                denom = f_instance([malla[2 * i],malla[2 * i + 2]],integral = True)
            
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

    @staticmethod
    def descomponer_binario(k, n):
        """
        Devuelve la descomposición en binario de un entero k con n dígitos, invertida.
        
        :param k: El entero a descomponer.
        :param n: El número de dígitos en la representación binaria.
        :return: La representación binaria invertida de k con exactamente n dígitos.
        """
        # Verificar que k esté dentro del rango válido
        if not (0 <= k < 2**n):
            raise ValueError(f"El entero k debe estar en el rango [0, {2**n - 1}] para n = {n}.")
        
        # Convertir k a binario invertido con ceros a la izquierda hasta tener n dígitos
        return format(k, f'0{n}b')[::-1]
    
    @staticmethod
    def grover_rudolph(n,f_instance):
        # Calcular los valores de theta
        thetas = Utils.calcular_theta(n, f_instance)
        
        # Crear el registro de qubits y bits clásicos
        q = QuantumRegister(n,'Q')
        circuit = QuantumCircuit(q, name='Grover_Rudolph')
        
        for i in range(len(thetas)):
            if len(thetas[i]) == 1:
                # Aplicar la puerta U_1
                circuit.ry( 2*thetas[0][0], q[n - 1])
                circuit.barrier()
            else:
                for j in range(len(thetas[i])):
                    # Aplicar la puerta U_i multicontrolada
                    theta = 2* thetas[i][j]
                    q_controls = q[n - 1:n - 1 - i:-1]  # Seleccionar los últimos `i` qubits como controles
                    q_target = q[n - 1 - i]            # El siguiente qubit como objetivo
                    mode = Utils.descomponer_binario(j, len(q_controls))  # Convertir `j` a binario
                    print(mode)
                    control_gate= RYGate(theta).control(len(q_controls), ctrl_state= mode) 
                    circuit.append(control_gate, q_controls + [q_target])                       
                circuit.barrier()
        return circuit




     

