from math import comb
import random

"""
La hipergeometrica surge de experimentos en donde tenemos >= 2 clases de objetos, y definimos una V.A. que cuente la cantidad de objetos de esa clase que obtenemos de un evento w.

Para trabajar con una sola variable, generalmente tenemos dos clases para elegir sin reposicion. Entonces, se vuelve una binomial sin reposicion.
Esto es asi porque de esa forma con una sola variable nos alcanza para calcular la cantidad de bolitas de la otra clase, pues si solo son dos:
#blancas = #totales - #negras
"""
"""
Ej
Supongamos que tenemos una urna con 10 bolitas:
2 blancas (representadas por el numero 0)
5 negras  (representadas por el numero 1)

El experimento consiste en extraer 3 bolitas.

Si ahora creo una V.A. que cuenta la cantidad de bolitas blancas que obtuve, esta seguira una DISTRIBUCION HIPERGEOMETRICA.
"""
#urna
N = 7 #cantidad de bolitas en la urna
n = 3 #cantidad de extracciones que hago
U = [0, 0, 1, 1, 1, 1, 1]
blancas = 2 #2 blancas (0)
#5 negras  (1) (puedo calcularlas como N - blancas)

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

def X(w):
    #cuenta la cantidad de blancas extraidas en el punto muestral w (representada por el numero 0)
    return w.count(0)

#Esta variable aleatoria una distribucion HIPERGEOMETRICA
#x : cantidad de bolitas blancas que quiero ver cual es la proba de extraer
#blancas : cantidad de bolitas blancas totales
#N: cantidad de bolitas en el experimento
#n: cantidad de bolitas que extraigo
#NOTA: la cantidad de rojas la puedo inferir de la cantidad total y la cantidad de blancas y negras que hay
def p_X(x, blancas, N, n):
    negras = N - blancas #cantidad de negras 
    resto = n - x #son las bolitas restantes que puedo extraer despues de elegir la cantidad de blancas que quiero ver la proba de sacar
    return (comb(blancas, x) * comb(negras, resto)) / (comb(N, n))

"""
Una forma de visualizar esta funcion de probabilidad, es que en el primer combinatorio (x, blancas) se abren ciertos caminos, y en cada uno de ellos se van a abrir otros 
caminos dados por el segundo combinatorio (y, negras).
Al final del arbol, en las hojas, tendremos todoas las posibles formas en que pudieron haber ocurrido el evento que queremos (por ejemplo, que salga exactamente 1 
blanca y el resto todas negras).
Contando todos esos caminos exitosos, y dividiendo por la cantidad de caminos totales, tenemos favorables/posibles. Esto porque consideramos un espacio equiprobable,
donde cada bolita tiene la misma probabilida de salir (no asi los colores, pero nuestro espacio muestral no consiste en colores, consiste en 7 bolitas, y 
cada una de ellas las elegimos al azar, con la misma proba. Que despues veamos cuales son blancas, negras o rojas es otra historia).
Seria muy distinto si nuestro espacio muestral fuera {'B', 'N'} donde P('B') = 2/7, P('N')=5/7, ahi si el espacio no seria equiprobable, pues los puntos muestrales
en si tienen probabilidades distintas.
En el espacio muestral que definimos, todos los puntos muestrales (cada una de las 7 bolitas) tiene la misma proba de ocurrir, no asi los eventos. 
Por ejemplo, el evento {sacar una negra} es mas probable que el evento {sacar una blanca}, pero estamos hablando de eventos, no de puntos muestrales, por lo que es equiprobable.
"""

#Capturo los eventos en donde se extrajeron exactamente una bolita blanca, {w : omega / X(w) = 1}
X_1 = [w for w in res if X(w) == 1]
#print(X_1)
print(len(X_1)/n_exps, p_X(1, blancas, N, n))
