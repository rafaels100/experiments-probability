import math
import random
"""
Para los otros casos, fui capaz de llegar de los casos discretos al continuo, pero aca voy a tomar otro approach:

Voy a partir de un intervalo continuo y voy a tratar de discretizarlo, sabiendo cosas del intervalo de tiempo continuo.
"""

"""
Quiero observar la cantidad de clientes que llegan a una caja de supermercado en una hora.
Se que en promedio hay 5 clientes por hora que pasan por la caja.
Quiero modelar como un proceso de Bernoulli. 
El problema es que si parto a la hora en intervalos de 1 minuto... Como se que no se van a 'acumular' dos clientes en el mismo minuto?
Eso ya nos dejaria en un escenario distinto al de Bernoulli, donde tengo exito o fracaso, es binario.

Lo que voy a hacer es tomar un intervalo de tiempo de longitud l y lo voy a hacer tender a 0. Ni minutos, ni segundos, ni nanosegundos... tan chico como quiera.
Voy a trabajar entonces con un modelo continuo. Salgo de Bernoulli, y llego a un proceso de Poisson.

Para que un proceso sea de Poisson, deben cumplirse tres condiciones
Para ello deben cumplirse 3 condiciones:

1)- Homogeneidad del tiempo: La proba de que ocurran k exitos en un intervalo de longitud l es la misma para todos los intervalos de la misma longitud.

2)- Independencia: Lo que suceda en un intervalo se queda en un intervalo. Nada del exterior afecta lo que pasa alli.

3)- Propiedad de los pequeños intervalos
Sea P(k, l) la proba de ver k exitos en el intervalo l
P(0, l) = 1 - lambda * l + o(l) 
P(1, l) = lambda * l + o_1(l)

Donde o y o_1 son dos funciones que se van a 0 cuando l -> 0.

NOTA: Este lambda es lo que nos hace pegar el salto al mundo continuo. Es el promedio de clientes que tenemos por cierta cantidad de tiempo.
Al multiplicar esta proba por un periodo de tiempo muy pequeño, la estamos 'reescalando'. Mas bien, estamos dividiendo esa proba en pequeños n pedazos,
pues l = T / n   =>  lambda * l = lambda * T / n = lambda / n * T y generalmente el tiempo T es 1, pues pedimos por minuto o por hora la distro.
(Por ejemplo, nos dicen que llegan 5 clientes por hora a la caja del super, entonces debemos partir 1 hora en n pedazos de longitud l con l -> 0)
Asi, la proba en cada intervalo termina siendo 'reescalada' por la cantidad de pedazos en que partimos al intervalo.

A ver...
P(0, l) = 1 - lambda * l + o(l)
Si l -> 0 entonces P(0, l) = 1 - lambda * l    pues o(l) -> 0 si l -> 0
A su vez, lambda * l tambien va a ser muy pequeño, pero le gana a o(l) que -> 0 cuando l -> 0
Esto nos dice que : 'La proba de ver 0 exitos cuando el intervalo es muy chico tiende a 1' Tiene sentido

P(1, l) = lambda * l + o_1(l)
Si l -> 0 entonces P(1, l) = lambda * l   pues o_1(l) -> 0 si l -> 0
A su vez, lambda * l tambien va a ser muy pequeño, pero le gana a o(l) que -> 0 cuando l -> 0
Esto nos dice que : 'La proba de ver 1 exito cuando el intervalo es muy chico tiende a 0' Tiene sentido, es dificil que caiga un exito en ese intervalo tan pequeño.

Por otro lado, si consideramos P(2, l), P(3, l), etc, es decir, la proba de que caigan 2 o mas exitos en un intervalo, esto es el complemento de lo que calculamos
P(k >= 2, l) = 1 - P(k=0, l) - P(k=1, l)
             = 1 - 1 + lambda * l + o(l) - lambda * l + o_1(l) = 0      pues o(l) -> 0 y o_1(l) -> 0 cuando l -> 0
             
Asi, la proba de que caigan dos exitos en el mismo bin/intervalo es despreciable ante la proba que de caiga 1 o 0.
Esto quiere decir que nuestros intervalos son BINARIOS. Ademas, por 2), son independientes... BINOMIAL !
Con parametros:
n = T / l   donde T es el tiempo total del experimento, y l es el intervalo de longitud muy pequeña
p = lambda * l = lambda * (T / n)  donde p es la proba de exito en cada experimento de bernoulli, en cada intervalo de longitud l

El producto n * p nos da
n * p = (T / l) * (lambda * l) = T * lambda
y esto se mantiene constante cuando n -> inf
Bajo estas circunstancias, vimos que la binomial converge a una Poisson de parametro n * p = T * lambda

Recordemos que:
Bin(n, k, p) = comb(n, k) * (1 - p) ** (n - k) * p ** k

CHATGPT recomienda: 
Ver a la longitud del intervado T como el l que habia dicho antes,
n * T = t
y usar T = t / n 
para que aparezca la variable tiempo total y n la cantidad de 'cortes' que le estamos haciendo a t.

Exp(lambda * T, k) = (lambda * T) ** k / k! * math.e ** (-lambda * T)
""" 

"""
Derivacion de la geometrica dado el modelo de la Poisson

Sea T la variable aleatoria que cuenta el tiempo hasta el primer exito. Quiero calcular F_T(t) la acumulada de T.
F_T(t) = P(T <= t)
Notemos que T > t es la proba de que el primer exito llegue despues del tiempo t. Esto es, que haya exactamente 0 exitos en un intervalo de longitud [0, t]. Esta funcion 
de probabilidad ya la deducimos, es la de la binomial
P(T <= t) = 1 - P(T > t) = 1 - P(0, long([0, t])) = 1 - P(0, t) = 1 - lambda * math.e ** (-lambda * t) 

Si derivamos esta funcion acumulada obtenemos la funcion de densidad
f_T(t) = lambda * math.e ** (-lambda * t)
"""
#el experimento consiste en contar la cantidad de clientes que atiende la caja de un supermercado.
#Por experiencia, sabemos que en promedio llegan 5 clientes por hora a la caja
lambd = 5 #clientes/hora
#voy a cortar al tiempo total en intervalos de 1 segundo. 
t = 1 #h
#Sabiendo que hay 60 minutos en una hora, y que hay 60 segundos en cada minuto, la longitud T de los intervalos sera
T = t/(60*60)
#esto genera periodos de
n = t / T
print(n)#es decir, 3600 segundos, 3600 bins/intervalos/sets para correr un experimento de bernoulli

#La teoria de probabilidad del proceso de poisson nos dice que la proba de un exito en alguno de estos intervalos viene dada por 
#la multiplicacion de la proba promedio de que ocurra el exito en el tiempo t total, por la longitud del intervalo que estoy considerando
p_e = lambd * T
#y la probabilidad de fracaso en cada uno es de 
p_f = 1 - lambd * T

#si fuera a correr ahora el tiempo, y ver que sucede en una hora de observar a la gente llegar al supermercado
#y, segundo a segundo, anotar un exito o un fracaso segun el experimento de Bernoulli
def bernoulli(p):
    return int(random.random() < p)
    
res = [bernoulli(p_e) for _ in range(int(n))]
print(res)


#defino la variable aleatoria
#X: Omega -> R 
#     w  |-> cantidad de bolitas blancas extraidas
def X(w):
    return sum(w)
    
print(X(res))
