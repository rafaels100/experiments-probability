import random

def bernoulli(p):
    if random.random() < p:
        return 1
    else:
        return 0

"""
La geometrica surge cuando la variable aleatoria cuenta la cantidad de fracasos que tuvieron que ocurrir antes de lograr el primer exito.
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

#defino la variable aleatoria
#Y: Omega -> R 
#     w  |-> cantidad de bolitas negras extraidas hasta obtener una blanca (i.e. cantidad de fracasos antes del primer exito)

def Y(w):
    i = 0
    contador = 0
    while i < len(w) and w[i] != 1:
        contador += 1
        i += 1
    return contador
    
"""
IMPORTANTE:
El problema de manejar espacios FINITOS es que es posible que nunca veamos un exito, es decir, existe el evento 
[0, 0, 0, 0, 0] (todos fallos)
asi, la defincion de la variable aleatoria se cae a pedazos en ese evento, porque nunca ocurre el exito en ese w.
Pero, para los casos en que consideramos k < n fallos antes del primer exito, esto funciona bien. Para el caso en que
hay k = n fallos, ya no funciona.

Por lo tanto tomo la decision de ignorar ese evento, pues mi variable aleatoria no tiene sentido cuando se lo paso, asi,
me quedo con todos los eventos en donde al menos hubo un exito.
Asi, 
rg_Y = {0, 1, ... , n - 1}

Asi, la variable aleaoria solo mapea enventos que tengan >= 1 exito.
Esto de dejar eventos en mi espacio muestral sin mapear no es un problema, siempre y cuando sepa que lo estoy haciendo.
"""

#asi, Y cuenta la cantidad de fracasos antes de mi primer exito. Esta variable aleatoria sigue una distribucion GEOMETRICA, esto es, 
#podemos calcular la probabilidad de que ocurra el evento {w pert(Omega) : Y(w) = x} usando una formula conocida
#dicha formula es
def geom(p, k):
    #NOTA: la defino con k en vez de k - 1 porque a mi variable aleatoria la defini como que me cuenta la cantidad de fallos antes del exito
    #entonces para que haya coherencia, esta funcion me da la proba de ver k fallos antes del primer exito, no de ver un exito en la k-esima tirada,
    #como la definimos en clase
    return (1-p) ** k * p

#compruebo
#El conjunto {Y = 3} es
Y_3 = [w for w in res if Y(w) == 3] #son todos los eventos en los que tuve 3 fallos antes de lograr el primer exito
#(en la catedra lo definen como los eventos en los que en la k-esima posicion aparece el primer exito, es equivalente, solo hay que poner k-1 en vez de k en la formula)
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
    print(f"La proba estadistica de necesitar {y} fallos antes de ver mi primer exito es de {len(Y_y) / N}, y la proba teorica es de {geom(p, y)}")
