import random
from math import comb

def bernoulli(p):
    if random.random() < p:
        return 1
    else:
        return 0

"""
La binomial negativa surge cuando la variable aleatoria cuenta la cantidad de intentos que tuve que hacer hasta lograr cierta cantidad de exitos. Esta cantidad
es FIJA, esta hardcodeada en la variable aleatoria.
Esto en un contexto en el cual corremos un experimento de bernoulli muchas veces, y el resultado es binario.
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

#puedo incluso definir una variable que tenga naturaleza binomial negativa
#Z: Omega -> R 
#     w  |-> cantidad de tiradas hasta obtener 2 exitos
def Z(w):
    contador = 0
    i = 0
    while i < len(w) and contador < 2:
        if (w[i] == 1): contador += 1
        i += 1
    if contador < 2:
        return -1 #devuelvo -1 para invalidar eventos que no entran en el caso borde {Z = n}
    return i
#NOTAR que en las variables aleatorias con binomial negativa, lo que esta fijo es la cantidad de exitos, al igual que en las variables aleatorias 
#con binomial, lo que esta fijo es la cantidad de tiradas

"""
IMPORTANTE:
El if extra que chequea si se alcanzo a contar 2 exitos es por el caso en que recorro todo w e intente todas las veces
que pude y no logre conseguir los dos exitos, como es el caso del [0, 0, 0, 0, 0] o el [0, 0, 0, 0, 1] van a contar 5 intentos pero van a tener un contador de 0 y 1 respectivamente.
Tambien el [1, 0, 0, 0, 0]. Cualquier evento que no logre los dos exitos en las 5 tiradas, de hecho. Vemos que si no tengo ese if, en el caso borde {Z = n = 5} voy a 
estar incluyendo muchos puntos muestrales que no pertenecen a ese evento, pues cuentan 5 intentos, pero no logran la cantidad de exitos necesarias para estar en ese conjunto.

Estos eventos no estan siendo mapeados por mi V.A., pues la defini solo para los eventos que tienen >= 2 exitos. Es una de las limitaciones de esta V.A.
(Mas sobre esta discusion al final del script)

En los otros casos en que quiero los eventos cuya cantidad de intentos antes del primer exito es < n = 5, va a funcionar sin ese if, pues
ni bien se alcanzen los exitos deseados ya sale del while con la cantidad de intentos realizados hasta lograr los dos exitos (y no entra al if).
"""

#asi, Z cuenta la cantidad de intentos/tiradas/extracciones que tuve que hacer hasta obtener 2 exitos. Esta variable aleatoria sigue una distribucion BINOMIAL NEGATIVA, esto es, 
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : Z(w) = z} usando una formula conocida
#dicha formula es
def bin_neg(n, k, p):
    return comb(n - 1, k - 1) * p**k * (1-p)**(n-k) 

#compruebo
#El conjunto {Z = 3} son todos los eventos en que necesite 3 extracciones para lograr el 2do exito, o lo que es lo mismo,
#los eventos en que el segundo exito vino en la tirada numero 3
Z_3 = [w for w in res if Z(w) == 3]
print("El evento {Z=3} es:")
print(Z_3)
print("La proba estadistica es:")
print(len(Z_3) / N)
print("La proba teorica es:")
print(bin_neg(3, 2, p))

#puedo repetir para todas las posibilidades, todos los atomos de Z, esto es, el rango de Z
#Son aquellos puntos donde P(Z=z) > 0
#Es claro que 
rg_Z = [2, 3, 4, 5]
#pues si o si necesito 2 tiradas para obtener 2 exitos
#y en el peor caso, voy a necesitar de mis 5 tiradas para obtener los dos exitos
#es cierto que hay eventos que tienen 0 probabilidad de ocurrir por esta V.A., pues P{Z = 1} es imposible porque necesito tirar al menos dos veces para ver 2 exitos
#asi, los eventos del estilo {[1, 0, 0, 0, 0]} donde solo vemos un exito no estan siendo considerados por esta V.A. (esta bien, no es necesario que sea sobreyectiva)
for z in rg_Z:
    Z_z = [w for w in res if Z(w) == z]
    print(f"La proba estadistica de necesitar {z} intentos para lograr mis 2 exitos es de {len(Z_z) / N}, y la proba teorica es de {bin_neg(z, 2, p)}")

#print([w for w in res if Z(w) == 5])

"""
REFLEXIONES SOBRE LA VARIABLE ALEATORIA Z:
hay eventos que no estan siendo mapeados por Z, Como el (1, 0, 0, 0, 0, .. 0), pues nunca lograra 2 exitos. Entonces esta variable aleatoria NO esta bien definida sobre todo
el espacio muestral, pues no sale de todo el espacio muestral, solo de los puntos muestrales que tienen >= 2 exitos.

Sin embargo, cuando digo    
if contador < 2:
        return -1
En realidad estoy mapeando los eventos que en los 5 intentos no logran dos exitos, y los estoy mapeando al atomo -1, como 'invalidandolos' en el contexto
de la V.A. y la distribucion que le quiero asignar, pues nada puedo decir de ese atomo y estos eventos con la formula de la distribucion binomial negativa,
ya que no hay 2 exitos que distribuir, y el k = 2 esta hardcodeado en mi definicion de V.A. y en mi formula de binomial negativa (aunque sea un parametro
en la formula, teoricamente esta fijo).

Asi, lo que conviene es asignar otra variable aleatoria con otra distribucion para esos casos.

Pero como tenemos esa potestad para definir cosas, lo hacemos teniendo en cuenta puntos que nos parecen interesantes en nuestro espacio muestral,
o que queremos estudiar.
A veces nos enfocamos en tan solo una parte de nuestro espacio muestral con las variables aleatorias que definimos, y eso esta bien, si queremos
estudiar cierta 'particion' de nuestro experimento. Pero debemos ser conscientes de las limitaciones de las V.A. que definimos, ser conscientes 
de las 'restricciones' que le estamos poniendo, los puntos muestrales en que nos vamos a enfocar y aquellos que pueden quedar de lado cuando 
las definimos.

Mientras tengamos en cuenta estas cosas, el hecho de que una V.A. no mapee todos y cada uno de los puntos muestrales de nuestro espacio muestral,
no es tan grave, siempre y cuando sea util definir esa V.A. para estudiar esa parte de nuestro experimento.
"""
