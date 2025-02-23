''' 
In this example, the domain of a variables is in the interval 1..5 denoting
very bad, bad, good, very good.  The agents then express their preferences on
those values 
'''

from models import *


# A variables taking values in [1..5]
p  = Symbol('p')

# interval(2,4) means that "I'm OK with the options 2,3,4 (with equal preference between them)
def interval(l,u):
    return Lambda((p,), Piecewise((1.0/(1+u-l), Ge(p, l) & Le(p ,u)), (0.0, True)))

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
m = [ [cte(0.5), cte(0.5)],
      [cte(0.5), cte(0.5)] ]

b0 = [interval(1,2), interval(1,5)]


matrixM = matrixMultiplication(CRing, m)

    
M1 = Model(R, b0,  m, matrixM, True, compare)

for i,b in enumerate(M1): 
    #print(f'{i}: {simplification(b)}')
    print(f'{i}: {str(b)[:30]}...')
    #if i > 10: break

printOpinion(b, [(i+1,) for i in range(5) ])

print("============ CASE2 ============ ")
b0 = [interval(1,2), interval(1,5), interval(2,4), interval(1,3)]
m = [ 
     [cte(0.2), cte(0.3), cte(0.4), cte(0.1)],
     [cte(0.3), cte(0.1), cte(0.2), cte(0.4)],
     [cte(0.5), cte(0.1), cte(0.2), cte(0.2)],
     [cte(0.3), cte(0.3), cte(0.3), cte(0.1)]
    ]

matrixM = matrixMultiplication(CRing, m)

M1 = Model(R, b0,  m, matrixM, False, compare)

for i,b in enumerate(M1): 
    print(f'{i}: {str(b)[:30]}...')
    pass

#print(f'{i}: {simplification(b)}')
printOpinion(b, [(i+1,) for i in range(5) ])


print("============ CASE3 ============ ")

def opextreme(v1,v2):
    '''Assigning v1 in the extremes and v2 otherwise'''
    return Lambda((p,), Piecewise( (v1, Or(Eq(p,1), Eq(p,5))), (v2, True)))

ext = opextreme(1.0, 0.0)
notext = opextreme(0.0, 1.0)

c3 = Lambda( (p,), Piecewise( (0.3 , Eq(p,2)), (0.7, Eq(p,3)), (0.0, True)))

b0 = [ext, c3]
m = [ 
     [cte(0.3), cte(0.7)],
     [cte(0.4), cte(0.6)]
    ]

matrixM = matrixMultiplication(CRing, m)

M1 = Model(R, b0,  m, matrixM, False, compare)

for i,b in enumerate(M1): 
    print(f'{i}: {str(b)[:30]}...')
    pass

#print(f'{i}: {simplification(b)}')
printOpinion(b, [(i+1,) for i in range(5) ])


print("============ CASE4 ============ ")


b0 = [ext, notext]
m = [ 
     [cte(0.3), cte(0.7)],
     [cte(0.4), cte(0.6)]
    ]

matrixM = matrixMultiplication(CRing, m)

M1 = Model(R, b0,  m, matrixM, False, compare)

for i,b in enumerate(M1): 
    print(f'{i}: {str(b)[:30]}...')
    pass

#print(f'{i}: {simplification(b)}')
printOpinion(b, [(i+1,) for i in range(5) ])

print("============ CASE5 ============ ")


b0 = [ext, notext]
m = [ 
     [cte(0.5), cte(0.5)],
     [cte(0.5), cte(0.5)]
    ]

matrixM = matrixMultiplication(CRing, m)

M1 = Model(R, b0,  m, matrixM, False, compare)

for i,b in enumerate(M1): 
    print(f'{i}: {str(b)[:30]}...')
    pass

#print(f'{i}: {simplification(b)}')
printOpinion(b, [(i+1,) for i in range(5) ])


print("============ CASE6 ============ ")
# Adding notext or ext in the matrix is problematic (the matrix is not longer stochastic)
c1 = Lambda( (p,), Piecewise( (0.3 , Eq(p,2)), (0.7, Eq(p,3)), (0.0, True)))
c2 = Lambda( (p,), Piecewise( (0.5 , Eq(p,1)), (0.5, Eq(p,5)), (0.0, True)))

b0 = [c1, c2]
# Consensus is not reached with this matrix 
m = [ 
     [cte(0.3), notext],
     [cte(0.5), cte(0.5)]
    ]
m = [ 
     [cte(0.3), cte(0.7)],
     [cte(0.5), cte(0.5)]
    ]

matrixM = matrixMultiplication(CRing, m)

M1 = Model(R, b0,  m, matrixM, False, compare)

for i,b in enumerate(M1): 
    print(f'{i}: {str(b)[:30]}...')
    pass

#print(f'{i}: {simplification(b)}')
printOpinion(b, [(i+1,) for i in range(5) ])

