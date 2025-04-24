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
n = int(t / T)
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

#corro el experimento N veces, estos es, voy al supermercado N veces y me quedo observando y registrando N horas, segundo a segundo anotando resultados
N = 1000
res = [[bernoulli(p_e) for _ in range(n)] for _ in range(N)]


#defino la variable aleatoria
#X: Omega -> R 
#     w  |-> cantidad de bolitas blancas extraidas
def X(w):
    return sum(w)
    
#asi, X cuenta la cantidad de exitos totales en mi experimento. Esta variable aleatoria sigue una distribucion BINOMIAL, esto es, 
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : X(w) = x} usando una formula conocida
#dicha formula es
def bin(n, k, p):
    return math.comb(n, k) * (p)**k * (1 - p) ** (n-k)
    
#tambien podemos aproximar a esta binomial con una poisson de parametro p = lambda * t
def poi(n, k, lambd, t):
    return ((lambd * t) ** k * math.e ** (-lambd * t)) / math.factorial(k)

#compruebo
#si quiero todos los w tal que {X = 1}, es decir, {w pert(Omega) : X(w) = 1}
X_1 = [w for w in res if X(w) == 1] #estos son todos los eventos en los que solo obtuve un exito en mis 5 tiradas
print("El evento {X=1} es:")
print(X_1)
print("La proba estadistica de obtener un exito es de:")
print(len(X_1) / N)
print("La proba teorica es:")
print(bin(n, 1, p_e))

#puedo repetir para todas las posibilidades, todos los atomos de X, esto es, el rango de X
#Son aquellos puntos donde P(X=x) > 0
#Es claro que 
rg_X = [0, 1, 2, 3, 4, 5] #pues puedo obtener de 0 a 5 exitos, si extraigo 5 veces con reposicion y considero un exito sacar una bola blanca
for x in rg_X:
    X_x = [w for w in res if X(w) == x]
    print(f"La proba estadistica de obtener {x} exitos es de {len(X_x) / N}, y la proba teorica es de {bin(n, x, p_e), poi(n, x, lambd, t)}")
    

"""
Controlando la variable tiempo en la funcion de la exponencial, deberia ser similar a 'recortar' el espacio muestral en ciertos intervalos,
con la salvedad de que no lo puedo cortar en el 'instante' exacto, sino que en el equivalente 'floor' del intervalo en el que cae.
"""
#por ejemplo, puedo cortar a los resultados de los experimentos por la mitad, empezando del 0, y quedarme con los 
#intervalos desde t = 0 h hasta t = 1/2 hora (30 minutos). Esto es equivalente a hacer slicing por w[:len(w)/2]
res_0_30 = [w[:len(w)//2] for w in res]
#la cantidad de intervalos se redujo a la mitad, pero no debo caer en el error de redefinir N = N/2, pues 
#esos son la cantidad de experimentos que corri. Lo que se redujo a la mitad fue n, la cantidad de experimentos de Bernoulli que corri
#en cada uno de mis experimentos, que siguen siendo N. Ahora tengo N observaciones de media hora, en vez de N de una hora.

#si ahora fuera a calcular lo mismo que antes, pero con estos eventos 'cortados a la mitad', deberia ver algo similar a lo que la proba de la poisson
#me indica pero para t=1/2 hora de tiempo
rg_X = [0, 1, 2, 3, 4, 5] #pues puedo obtener de 0 a 5 exitos, si extraigo 5 veces con reposicion y considero un exito sacar una bola blanca
print("Modificando el tiempo")
for x in rg_X:
    X_x = [w for w in res_0_30 if X(w) == x]
    print(f"La proba estadistica de obtener {x} exitos es de {len(X_x) / N}, y la proba teorica es de {bin(n//2, x, p_e), poi(n/2, x, lambd, t/2)}")


#Puedo definir la exponencial en terminos de la poisson
#Sea T la variable aleatoria que cuenta el tiempo hasta el primer exito. Quiero calcular F_T(t) la acumulada de T.
#F_T(t) = P(T <= t)
#P(T <= t) = 1 - P(T > t) = 1 - P(0, long([0, t])) = 1 - P(0, t) = 1 - lambda * math.e ** (-lambda * t) 
"""
La cantidad de fracasos antes del primer exito sera ahora el tiempo que pasa antes del primer exito.

En el caso discreto, podiamos pensarlo como 'la proba de que el primer exito ocurra en el k-esimo intento'
Pero esto no sirve en discreto, porque es muy poco probable, por muchos N experimentos que corra, que 
el k-esimo intervalo en donde quiero obtener mi primer exito justo sea un exito.

Creo que llegue a la barrera en que ya no puedo contar eventos y calcular la proba estadisticamente como lo venia haciendo anteriormente.
A partir de aqui, es todo calculo, y confiar en que la teoria se condiga con los resultados del mundo real.

Well.. not so fast.
Que tal cortar a la mitad todos los intervalos, y contar por exitos. Aquellos que tienen mas de 1 exito, los descarto.
Eso me asegura de que me voy a quedar eventos cuyo primer exito VINO DESPUES de cierto tiempo t.
No me importa exactamente cuando vino, solo que vino despues.
Tengo que empezar a pensar en lo que pasa en 'intervalos de intervalos', no en intervalos puntuales del proceso de poisson.
"""
res_0_30_f = [w for w in res if sum(w[:len(w)//2]) == 0] #me quedo con los eventos donde solo tuve fracasos la primera media hora

def expo(lambd, t):
    return math.exp(-lambd * t)

print(len(res_0_30_f))
print(len(res_0_30_f)/N, expo(lambd, 1/2))
