'''
A simple example using R+
'''

from models import *

# A single proposition 
p = Symbol('p')
 
def cte(n):
    '''The constant constraint returning the value n'''
    return Lambda((p,), n)

# The matrix of influences 
m = [ [cte(1), cte(0)],
      [cte(0.8), cte(0.2)] ]


# Representation of constraints 
# c1(0) = 0.3 and c1(1) = 0.7
c1 = Lambda((p,), Piecewise((0.3, Eq(p,0)), (0.7, True)))
c2 = Lambda((p,), Piecewise((0.8, Eq(p, 0)), (0.2, True)))

b0 = [c1, c2]

# Building R+
CRing = CSemiring(R, (p,))

# Model with matrix multiplication 
matrixM = matrixMultiplication(CRing, m)
M1 = Model(R, b0,  m, matrixM)

print("============ REAL ============ ")
last = None
for i,b in enumerate(M1): 
    last = b
    #print('.', end='')
    print(f'{simplification(b)}')
