from math import comb
import random

"""
La hipergeometrica surge de experimentos en donde tenemos >= 2 clases de objetos, y definimos una V.A. que cuente la cantidad de objetos de esa clase que obtenemos de un evento w.
"""
"""
Ej
Supongamos que tenemos una urna con 10 bolitas:
2 blancas (representadas por el numero 0)
5 negras  (representadas por el numero 1)
3 rojas   (representadas por el numero 2)

El experimento consiste en extraer 3 bolitas.
"""
#urna
N = 10 #cantidad de bolitas en la urna
n = 4 #cantidad de extracciones que hago
U = [0, 0, 1, 1, 1, 1, 1, 2, 2, 2]
blancas = 2 #2 blancas (0)
negras = 5 #5 negras  (1)
            #3 rojas   (2) (la puedo calcular como N - blancas - negras)

def realizar_exp(U, n):
    #en python, todos los objetos pasan por referencia. Como voy a estar modificando la urna, creo una copia
    U_ = U[:]
    res = []
    for i in range(n):
        #en cada extraccion, elimino esa bolita de la urna y extraigo otra vez
        res.append(U_.pop(random.randint(0, len(U_) - 1)))
    return res

n_exps = 1000 #cantidad de veces que corro el experimento de extraer 4 bolitas sin reposicion
res = [realizar_exp(U, n) for _ in range(n_exps)]
#print(res)

"""
Creo dos variables aleatorias que cuentan la cantidad de blancas y negras 
"""

def X(w):
    #cuenta la cantidad de blancas extraidas en el punto muestral w (representada por el numero 0)
    return w.count(0)

def Y(w):
    #cuenta la cantidad de negras extraidas en el punto muestral w (representada por el numero 1)
    return w.count(1)
    
def XY(w):
    #cuenta la cantidad de bolitas blancas y negras extraidads en el punto muestral w
    return [X(w), Y(w)]

#Esta variable aleatoria conjunta sigue una distribucion HIPERGEOMETRICA
#x : cantidad de bolitas blancas que quiero ver cual es la proba de extraer
#y: cantidad de bolitas negras que quiero ver cual es la proba de extraer
#x : cantidad de bolitas blancas totales
#neg: cantidad de bolitas negras totales
#N: cantidad de bolitas en el experimento
#n: cantidad de bolitas que extraigo
#NOTA: la cantidad de rojas la puedo inferir de la cantidad total y la cantidad de blancas y negras que hay
def p_XY(x, y, blancas, negras, N, n):
    rojas = N - blancas - negras #cantidad de rojas 
    resto = n - x - y #son las bolitas restantes que puedo extraer despues de elegir la cantidad de blancas y negras que quiero ver la proba de sacar
    return (comb(blancas, x) * comb(negras, y) * comb(rojas, resto)) / (comb(N, n))

#Capturo los eventos en donde se extrajeron exactamente una bolita blanca y una negra, {w : omega / X(w) = 1 && Y(w) == 1} = {w : omega / XY(w) = (1, 1)}
XY_1 = [w for w in res if XY(w) == [1, 1]]
#print(X_1)
print(len(XY_1)/n_exps, p_XY(1, 1, blancas, negras, N, n))
