import random
import math

def bernoulli(p):
    if random.random() < p:
        return 1
    else:
        return 0

"""
La exponencial es una geometrica en esteroides.
Tenemos muchisimos experimentos de bernoulli, que modelan los instantes que hay en una hora por ejemplo, donde en cada instante podemos o no tener un exito.
Cada uno de estos tiene un resultado BINARIO, con cierta probabilidad de exito p y de fracaso 1 - p

En la geometrica, contabamos la cantidad de fracasos antes del primer exito.
En la exponencial, nos va a interesar la cantidad de tiempo que pasa antes del primer exito.
Para ello, cortamos al tiempo en pedacitos, y en cada uno de ellos tenemos un experimento de bernoulli.

Si queremos la proba de que llegue exactamente en un momento del tiempo, tenemos que ver los eventos en los que exactamente se llego
en ese momento.

Sin embargo, esto no es exactamente lo que modela la exponencial, porque no existe un instante en el modelado continuo, uno siempre puede ir mas alla, y conseguir
un pedazo aun mas pequeño.
Lo correcto seria entonces definir un 'rango' de momentos en los que considero que tuve exito, en vez de querer calcular para el momento exacto en que se produjo un exito.
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
#Y: Omega -> R 
#     w  |-> cantidad de tiempo hasta el primer exito (i.e. cantidad de tiempo hasta la llegada del primer cliente)

def Y(w):
    i = 0
    contador = 0
    while i < len(w) and w[i] != 1:
        contador += 1
        i += 1
    return contador
    
#asi, Y cuenta la cantidad de fracasos antes de mi primer exito. Esta variable aleatoria sigue una distribucion GEOMETRICA, esto es, 
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : Y(w) = x} usando una formula conocida
#dicha formula es
def geom(p, k):
    #NOTA: la defino con k en vez de k - 1 porque a mi variable aleatoria la defini como que me cuenta la cantidad de fallos antes del exito
    #entonces para que haya coherencia, esta funcion me da la proba de ver k fallos antes del primer exito, no de ver un exito en la k-esima tirada,
    #como la definimos en clase
    return (1-p) ** k * p
    
#En realidad, sigue una distribucion EXPONENCIAL
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : Y(w) = x}, esto es, la proba de que pasen exactamente k segundos e inmediatamente llegue el primer exito
def exp(lambd, k):
    return lambd * math.e**(-lambd*k)

#compruebo
#El conjunto {Y = 3} es
Y_3 = [w for w in res if Y(w) == 3] #son todos los eventos en los que pasaron 3 segundos e inmediatamente luego vino el primer exito
#(en la catedra lo definen como los eventos en los que en la k-esimo segundo aparece el primer exito, es equivalente, solo hay que poner k-1 en vez de k en la formula)
print("El evento {Y=3} es:")
print(Y_3)
print("La proba estadistica es:")
print(len(Y_3) / N)
print("La proba teorica es:")
print(geom(p, 3))

#puedo repetir para todas las posibilidades, todos los atomos de Y, esto es, el rango de Y
#Son aquellos puntos donde P(Y=y) > 0
#Es claro que 
rg_Y = [0, 1, 2, 3, 4]
#pues si necesito 0 fallos antes del primer exito, significa que la pegue en la primera
#sin embargo, si necesito 5 fallos antes del primer exito, significa que nunca tuve exito, y eso mapea al evento [0, 0, 0, 0, 0] (0 en todas las n posiciones)
#este evento no me interesa, pues no significa nada en el contexto de la definicion de mi VA, por lo que va a fallar cualquier proba que quiera hacer sobre ese evento
for y in rg_Y:
    Y_y = [w for w in res if Y(w) == y]
    print(f"La proba estadistica de necesitar {y} fallos antes de ver mi primer exito es de {len(Y_y) / N}, y la proba teorica es de {geom(p, y), exp(lambd, y) * p}")
