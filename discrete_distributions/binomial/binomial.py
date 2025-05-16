import random
from math import comb

def bernoulli(p):
    if random.random() < p:
        return 1
    else:
        return 0

"""
La binomial surge cuando la variable aleatoria cuenta los exitos totales de ejecutar varios experimentos de Bernoulli seguidos.
Cada uno de estos tiene un resultado BINARIO, con cierta probabilidad de exito p y de fracaso 1 - p
"""

"""
Por ejemplo, supongamos que el experimento consiste en sacar una bolita con reposicion 5 veces seguidas, de una urna con bolitas blancas y negras (resultado binario).
Si hay por ejemplo 10 bolitas en total y 3 son blancas, y considero un exito sacar una blanca, entonces la probabilidad de exito cada vez es de 3/10.
"""
n = 10 #bolitas
b = 3 #blancas
p = b/n #proba de exito
r = 5 #cantidad de extracciones que hago
N = 1000 #cantidad de veces que corro el experimento (de sacar 5 bolitas seguidas)

#corro el experimento N veces
res = [[bernoulli(p) for _ in range(r)] for _ in range(N)]
print(res)

#defino la variable aleatoria
#X: Omega -> R 
#     w  |-> cantidad de bolitas blancas extraidas
def X(w):
    return sum(w)

#asi, X cuenta la cantidad de exitos totales en mi experimento. Esta variable aleatoria sigue una distribucion BINOMIAL, esto es, 
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : X(w) = x} usando una formula conocida
#dicha formula es
def bin(n, k, p):
    return comb(n, k) * (p)**k * (1 - p) ** (n-k)

#compruebo
#si quiero todos los w tal que {X = 1}, es decir, {w pert(Omega) : X(w) = 1}
X_1 = [w for w in res if X(w) == 1] #estos son todos los eventos en los que solo obtuve un exito en mis 5 tiradas
print("El evento {X=1} es:")
print(X_1)
print("La proba estadistica de obtener un exito es de:")
print(len(X_1) / N)
print("La proba teorica es:")
print(bin(r, 1, p))

#puedo repetir para todas las posibilidades, todos los atomos de X, esto es, el rango de X
#Son aquellos puntos donde P(X=x) > 0
#Es claro que 
rg_X = [0, 1, 2, 3, 4, 5] #pues puedo obtener de 0 a 5 exitos, si extraigo 5 veces con reposicion y considero un exito sacar una bola blanca
for x in rg_X:
    X_x = [w for w in res if X(w) == x]
    print(f"La proba estadistica de obtener {x} exitos es de {len(X_x) / N}, y la proba teorica es de {bin(r, x, p)}")
