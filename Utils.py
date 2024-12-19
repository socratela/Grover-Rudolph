import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit,ClassicalRegister,QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

class Utils:
    @staticmethod
    def f(x):
        sol = []
        for i in range(len(x)):
            if 0 < x[i] < 0.5:
                sol.append(4 * x[i])
            else:
                sol.append(4 - 4 * x[i])
        return np.array(sol)

    @staticmethod
    def int_f(x):
        sol = []
        for i in range(len(x)):
            if 0 < x[i] < 0.5:
                sol.append(2 * x[i]**2)
            else:
                sol.append(4 * x[i] - 2 * x[i]**2)
        return np.array(sol)

    @staticmethod
    def integrar(int_f, x):
        return int_f(x)[1] - int_f(x)[0]

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
    def calcular_theta(n, funcion_a_integrar):
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
                num = Utils.integrar(funcion_a_integrar, [malla[2 * i], malla[2 * i + 1]])
                denom = Utils.integrar(funcion_a_integrar, [malla[2 * i], malla[2 * i + 2]])
                
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
