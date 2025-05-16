import random
import math

def bernoulli(p):
    if random.random() < p:
        return 1
    else:
        return 0

"""
La poisson es una binomial en esteroides.
Tenemos muchisimos experimentos de bernoulli, que modelan los instantes que hay en una hora por ejemplo, donde en cada instante podemos o no tener un exito.
Cada uno de estos tiene un resultado BINARIO, con cierta probabilidad de exito p y de fracaso 1 - p
"""

"""
Por ejemplo, supongamos que el experimento consiste en contar la cantidad de personas que atiende una caja de supermercado en una hora.
Sabemos, por observaciones empiricas del supermercado cuando vamos a comprar los guayma, que la caja atiende en promedio 5 clientes por hora. Decimos lambda = 5,
la cantidad promedio de exito en el lapso de tiempo estudiado.

La idea es partir al intervalo de tiempo en n pedazos, y decir que existe una probabilidad de lambda/n de que, instante a instante, ocurra un exito, llegue
un cliente a la caja.
Si bien cuando n->inf esta probabilidad es minuscula, al haber tantos intentos, tantos experimentos de bernoulli, vamos eventualmente a observar algunos exitos,
y el modelo se condecira bien con lo que observamos en la realidad, que en promedio llegan 5 clientes por hora.

Detras de la cortina, todo es un experimento de Bernoulli?
"""
n = 100000 #instantes dt
lambd = 5 #promedio de personas que se atienden por hora
p = lambd/n #proba de exito, de que llegue un cliente en un instante dt
N = 100 #cantidad de veces que corro el experimento (de observar por una hora la llegada o no llegada de clientes instante a instante).

#corro el experimento N veces, esto es, gasto N horas de mi tiempo en ver si alguien llega o no a la caja, instante a instante (soy flash)
res = [[bernoulli(p) for _ in range(n)] for _ in range(N)]
#print(res)

#defino la variable aleatoria
#X: Omega -> R 
#     w  |-> cantidad de clientes que llegan al supermercado en una hora
def X(w):
    return sum(w)

#asi, X cuenta la cantidad de exitos totales en mi experimento. Esta variable aleatoria sigue una distribucion BINOMIAL, esto es, 
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : X(w) = x} usando una formula conocida
#dicha formula es
def bin(n, k, p):
    return math.comb(n, k) * (p)**k * (1 - p) ** (n-k)
    
#En realidad, sigue una distribucion de poisson, pues cuando k esta fijo y n->inf, llegamos a la Poisson
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : X(w) = x}, esto es, la proba de que lleguen exactamente x clientes en una hora, usando una formula conocida
def poi(lambd, k):
    return (lambd**k / math.factorial(k)) * math.e**-lambd 

#compruebo
#si quiero todos los w tal que {X = 1}, es decir, {w pert(Omega) : X(w) = 1}
X_1 = [w for w in res if X(w) == 1] #estos son todos los eventos en los que solo obtuve un exito en mis n extracciones/experimentos de Bernoulli/instantes
print("El evento {X=1} es:")
print(X_1)
print("La proba estadistica de obtener un exito es de:")
print(len(X_1) / N)
print("La proba teorica es:")
print(bin(n, 1, p))

#puedo repetir para todas las posibilidades, todos los atomos de X, esto es, el rango de X
#Son aquellos puntos donde P(X=x) > 0
#Es claro que 
rg_X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] #pues puedo obtener de 0 a n (infinito teorico, cantidad de instantes en una hora) exitos, pero lo mas probable es que 
#la cantidad de exitos ronde los 5, pues si la caja atiende en promedio 5 clientes, es poco probable que veamos 100 clientes siendo atendidos en esa hora. No es imposible, 
#pues 100 < n la cantidad de instantes en una hora que estoy considerando. Pero es poco probable.
for x in rg_X:
    X_x = [w for w in res if X(w) == x]
    print(f"La proba estadistica de obtener exactamente {x} exitos es de {len(X_x) / N}, y la proba teorica es de: con Binomial: {bin(n, x, p)}, y con Poisson: {poi(lambd, x)}")
