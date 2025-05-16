import math
import random

"""
X ~ Poi(lambda * t)
La poisson toma un parametro lambda_t = lambda * t

t: Nos da info de la cantidad de tiempo que dura el experimento, justo como cuando definimos una binomial le pasamos n para saber la cantidad de intentos que tenemos
lambda: Nos da el promedio de exitos en el experimento. Es el equivalente a p cuando se lo pasamos a una binomial
"""

#La teoria de probabilidad del proceso de poisson nos dice que la proba de un exito en alguno de estos intervalos viene dada por 
#la multiplicacion de la proba promedio de que ocurra el exito en el tiempo t total, por la longitud del intervalo que estoy considerando
#corto al tiempo en pedazitos, en segundos 
n = 60 * 60 #una hora son 60 minutos x 60 segundos = 3600 segundos
lambd = 12 / 3600 #clientes por segundo
p_e = lambd
#y la probabilidad de fracaso en cada uno es de 
p_f = 1 - lambd

#si fuera a correr ahora el tiempo, y ver que sucede en una hora de observar a la gente llegar al supermercado
#y, segundo a segundo, anotar un exito o un fracaso segun el experimento de Bernoulli
def bernoulli(p):
    return int(random.random() < p)

#corro el experimento N veces, estos es, voy al supermercado N veces y me quedo observando y registrando N horas, segundo a segundo anotando resultados
N = 1000
res = [[bernoulli(p_e) for _ in range(n)] for _ in range(N)]

#defino la variable aleatoria
#X: Omega -> R 
#     w  |-> cantidad de exitos en el experimento
def X(w):
    return sum(w)
    
#asi, X cuenta la cantidad de exitos totales en mi experimento. Esta variable aleatoria sigue una distribucion POISSON, esto es,
#es como una binomial en esteroides, cuenta exitos cuando la cantidad de intentos tiende al infinito (sin embargo la poisson no es continua, es discreta,
#porque devuelve valores discretos, y el tiempo t esta fijo cuando definimos la V.A. X ~ Poi(lambda * t))
def f_X(k, lambd_t):
    #la probabilidad de observar k exitos durante la realizacion de un experimento
    #(es decir, que Woz cometa exactamente k errores en una presentacion) es de:
    return ((lambd_t) ** k * math.e ** (-lambd_t)) / math.factorial(k)
    
def F_X(k, lambd_t):
    return sum([f_X(k, lambd_t) for k in range(0, k + 1)])

#tambien podemos aproximar a esta poisson con una binomial, pero mientras mas grande k, menos se parecera al resultado correcto
def bin(n, k, p):
    return math.comb(n, k) * (p)**k * (1 - p) ** (n-k)

#compruebo
#si quiero todos los w tal que {X = 1}, es decir, {w pert(Omega) : X(w) = 1}
X_1 = [w for w in res if X(w) == 1] #estos son todos los eventos en los que solo obtuve un exito en mis 5 tiradas
#print("El evento {X=1} es:")
#print(X_1)
#print("La proba estadistica de obtener un exito es de:")
#print(len(X_1) / N)
#print("La proba teorica es:")
#print(bin(n, 1, p_e))

#puedo calcular las probas usando la V.A. como condicion para capturar elementos del espacio muestral, justo como en la definicion de F_X, y usando eventos favorables / totales
#Puedo calcular F_X(k) con la definicion: P(X <= k) = F_X(k)
def F_X_amano(x, res):
    return len([w for w in res if X(w) <= x])/len(res)
    
#puedo repetir para todas las posibilidades, todos los atomos de X, esto es, el rango de X
#Son aquellos puntos donde P(X=x) > 0
#Es claro que 
rg_X = range(0, 13) #pruebo estos, pero el rango de X es 0 -> INF = 3600, pero teoricamente es infinito, podria tener exito en todos y cada una de mis tiradas,
                    #aunque es poco probable
t = 3600 #miro todo el tiempo que tengo disponible
for x in rg_X:
    print(f"La proba estadistica de obtener {x} exitos es de {F_X_amano(x, res)}, y la proba teorica es de {bin(n, x, p_e), F_X(x, lambd * t)}")

#NOTEMOS como la binomial es una buena aproximacion al principio, pero a medida que aumentamos la cantidad de exitos que queremos meter en el intervalo t,
#se aleja cada vez mas del resultado correcto que nos da F_X, que si se condice todo el tiempo con los resultados estadisticos.
    
#si quisiera manejar el tiempo, deberia crear otra V.A., que tenga parametro Poi(lambd * t), pues es como si hubiese cambiado el n en la Bin(n, p).
#X ya no me va a servir, no se va a condecir con F_X

