'''
Agents discussing about different topics at the same time
'''

from models import *


# A variables taking values in [1..3] where p=n is the opinion about the proposition n 
p  = Symbol('p')

#Equal preference for all the 5 values
def cte(n):
    return Lambda((p,), n)

CRing = CSemiring(R, (p,))


def compare(new, old):
    EPSILON = 0.0001
    '''Two opinions are the same if they coincide for all the values in the domain'''
    for i, x in enumerate(new):
        for j in range(5):
            if abs(x(j+1) - old[i](j+1)) > EPSILON: return False

    return True
    
print("============ CASE1 ============ ")

m = [ [cte(0.3), cte(0.7)],
      [cte(0.5), cte(0.5)] ]


def makeOp(*args):
    options= tuple( (v, Eq(p, i+1)) for  i,v in enumerate(args))
    return Lambda((p,), Piecewise(*options, (0.0, True)))

b0 = [makeOp(0.3, 0.7, 0.1), makeOp(0.4, 0.4, 0.4)]
matrixM = matrixMultiplication(CRing, m)

M1 = Model(R, b0,  m, matrixM, True, compare)

for i,b in enumerate(M1): 
    #print(f'{i}: {simplification(b)}')
    print(f'{i}: {str(b)[:30]}...')
    pass

print(f'{i}: {simplification(b)}')
printOpinion(b, [(i+1,) for i in range(3) ])


print("============ CASE2 ============ ")

# There is a different influence for each proposition
m = [ [makeOp(0.3,0.2,0.1), makeOp(0.7,0.8,0.9)],
      [makeOp(0.5,0.1,0.8), makeOp(0.5,0.9,0.2)] ]


def makeOp(*args):
    options= tuple( (v, Eq(p, i+1)) for  i,v in enumerate(args))
    return Lambda((p,), Piecewise(*options, (0.0, True)))

b0 = [makeOp(0.3, 0.7, 0.1), makeOp(0.4, 0.4, 0.4)]
matrixM = matrixMultiplication(CRing, m)

M1 = Model(R, b0,  m, matrixM, True, compare)

for i,b in enumerate(M1): 
    #print(f'{i}: {simplification(b)}')
    print(f'{i}: {str(b)[:30]}...')
    pass

#print(f'{i}: {simplification(b)}')
printOpinion(b, [(i+1,) for i in range(3) ])
