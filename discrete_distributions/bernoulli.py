import random

def bernoulli(p):
    if random.random() < p:
        return 1
    else:
        return 0

"""
CHATGPT: tambien podria hacer
def bernoulli(p):
    return int(random.random() < p)
"""

"""
La bernoulli consiste en ejecutar un solo experimento que tiene un resultado BINARIO, con cierta probabilidad de exito p y de fracaso 1 - p
"""
#por ejemplo, si tiro una moneda justa
res = bernoulli(1/2)
print(res)
#si tiro una moneda cargada para que pierda
res = bernoulli(1/100)
print(res)
