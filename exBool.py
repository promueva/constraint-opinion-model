'''
Some Examples using the CRISP semiring
'''

from models import *

# The variables
x,y = symbols('x y')
# Lifting the Crisp semiring to constraints
CRing = CSemiring(Crisp, (x,y))

# True/False constants
TRUE = Lambda( (x,y), S.true)
FALSE = Lambda( (x,y), S.false)

#Some constraints   
c1 = Lambda( (x,y), x <= 42)
c2 = Lambda( (x,y), y <= 25)
c3 = Lambda( (x,y), x >= 15)
c4 = Lambda( (x,y), y >= 66)

# Combining constraints 
d1 = CRing.times(c1, c2)
d2 = CRing.plus(c3, c4)

# -------------
# 1st Example
# -------------

# Update functions as matrix multiplications
m1 = [ [TRUE , FALSE],
       [TRUE,  TRUE]]
matrixM1 = matrixMultiplication(CRing, m1)

# The opinion model
M1 = Model(CRing, [d1, d2], m1, matrixM1)

# This one reaches the fixpoint in 2 steps
print("============ M1 ============ ")
for i,b in enumerate(M1): 
    print(f'{i}: {simplification(b)}')

# -------------
# 2nd Example
# -------------
m2 = [ [TRUE , FALSE],
       [FALSE,  TRUE]]
matrixM2 = matrixMultiplication(CRing, m2)
M2 = Model(CRing, [d1, d2], m2, matrixM2)

# This one reaches the fixpoint in 1 step
print("============ M2 ============ ")
for i,b in enumerate(M2): 
    print(f'{i}: {b}')


# -------------
# 3rd Example 
# -------------
m3 = [ [FALSE , TRUE],
       [TRUE,  FALSE]]
matrixM3 = matrixMultiplication(CRing, m3)
M3 = Model(CRing, [d1, d2], m3, matrixM3)

# This never stabilizes
print("============ M3 ============ ")
for i,b in enumerate(M3): 
    print(f'{i}: {b}')
    if i>10: 
        print("stop.")
        break

# -------------
# 4th Example
# -------------
print("============ M4 ============ ")
c01 = Lambda((x,y), y <= 20)
c10 = Lambda((x,y), x >= 10)
m4 = [ [TRUE , c01],
       [c10,  TRUE]]

matrixM4 = matrixMultiplication(CRing, m4)
M4 = Model(CRing, [d1, d2], m4, matrixM4)

# This one reaches the fixpoint in 4 steps
for i,b in enumerate(M4): 
    print(f'{i}: {simplification(b)}')
