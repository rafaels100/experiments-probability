import math
import random
import numpy as np

#el experimento consiste en contar la cantidad de clientes que atiende la caja de un supermercado.

#voy a cortar al tiempo total en intervalos de 1 segundo. 
t = 1 #hora, la duracion de la presentacion de woz
#Sabiendo que hay 60 minutos en una hora, y que hay 60 segundos en cada minuto, la longitud T de los intervalos sera
T = t/(60*60)
#esto genera periodos de
n = int(t / T)#60*60 = 3600 segundos, 3600 bins/intervalos/sets para correr un experimento de bernoulli
print(n)
#La teoria de probabilidad del proceso de poisson nos dice que la proba de un exito en alguno de estos intervalos viene dada por 
#la multiplicacion de la proba promedio de que ocurra el exito en el tiempo t total, por la longitud del intervalo que estoy considerando
#Por experiencia, sabemos que en promedio llegan 5 clientes por hora a la caja
lambd = 12 / 3600 #12 errores en promedio por segundo
p_e = lambd #como lambda esta en minutos, lo convierto a horas para multiplicarlo por T, que lo pense desde las horas
#y la probabilidad de fracaso en cada uno es de 
p_f = 1 - lambd

#si fuera a correr ahora el tiempo, y ver que sucede en una hora de observar a la gente llegar al supermercado
#y, segundo a segundo, anotar un exito o un fracaso segun el experimento de Bernoulli
def bernoulli(p):
    return int(random.random() < p)

#corro el experimento N veces, estos es, voy al supermercado N veces y me quedo observando y registrando N horas, segundo a segundo anotando resultados
N = 1000
res = [[bernoulli(p_e) for _ in range(n)] for _ in range(N)]
    
#tiempo hasta el k-esimo exito
def Z(w, k):
    #lista de tiempos en donde ocurrieron los exitos
    Ts = [i for i, valor in enumerate(w) if valor == 1]
    if (k > len(Ts)):
        return -1 #para indicar que se esta pidiendo mas exitos de los que ocurrieron en el experimento
    #sino, devuelvo la suma de los tiempos hasta el k-esimo exito
    return Ts[k - 1]

#esta variable aletoria sigue una distribucion gamma
def f_gamma(alfa):
    dt = 0.01
    return sum([t ** (alfa - 1) * np.exp(-t) * dt for t in np.arange(0, 10, dt)])
    
print(f_gamma(1), f_gamma(2), f_gamma(3))

def f_Z(lambd, alfa, t):
    return (lambd ** alfa) / math.gamma(alfa) * (t ** (alfa - 1)) * np.exp(-lambd * t)

"""
def f_Z(lambd, alfa, t):
    return (lambd / f_gamma(alfa)) * (lambd * t) ** (alfa - 1) * np.exp(-lambd * t)
"""

def F_Z(lambd, alfa, t_f):
    dt = 0.01
    return sum([f_Z(lambd, alfa, t) * dt for t in np.arange(0, t_f, dt)])
    
#obtengo muchas muestras de la cantidad de tiempo hasta el k-esimo exito, en este caso k = 2
t_dos_ex = [Z(w, 2) for w in res]
#sin embargo, la proba es un juego de cantidad de eventos / espacio muestral, y esto no tiene cantidad de eventos, 
#sino cantidad de tiempo. Si quiero dar una proba, debo capturar eventos. Esto lo hago usando a la V.A.
#de esta forma {w : omega / Z(w) <= t}
#Puedo calcular F_Z(k) con la definicion: P(Z <= t) = F_Z(t)
def F_Z_amano(k, t, res):
    #print([Z(w, k) for w in res if Z(w, k) <= t])
    return len([w for w in res if Z(w, k) <= t]) / len(res)

#evaluo las funciones para la proba de obtener 2 exitos antes de 10 minutos
print(F_Z_amano(2, 10 * 60, res), F_Z(lambd, 2, 10 * 60)) #le tengo que pasar segundos, 10 mintuos * 60 segundos
