'''
A group of people discussing about the actual value of two variables x and y
See the description in the [paper](./paper.pdf). 
'''

from models import *

# The first version using only one variable
x = Symbol('x')
 
def cte(n):
    '''The constant constraint returning the value n'''
    return Lambda((x,), n)

m = [ 
      [cte(0.3), cte(0.2), cte(0.3), cte(0.2)],
      [cte(0.2), cte(0.3), cte(0.1), cte(0.4)],
      [cte(0.2), cte(0.4), cte(0.2), cte(0.2)],
      [cte(0.1), cte(0.1), cte(0.5), cte(0.3)]]

# c1: 4 <= x <= 6
c1 = Lambda((x,), Piecewise((1.0, Ge(x,4) & Le(x, 6)), (0.0, True)))
# c2 : x >=5
c2 = Lambda((x,), Piecewise((1.0, Ge(x,5) & Le(x, 10)), (0.0, True)))
# c3 : 6 <= x <= 7
c3 = Lambda((x,), Piecewise((1.0, Ge(x,6) & Le(x, 7) ), (0.0, True)))
# c4 : 1 <= x <=4
c4 = Lambda((x,), Piecewise((1.0, Ge(x,1) & Le(x, 4)), (0.0, True)))

b0 = [c1, c2, c3, c4]

# Building the R-semiring 
CRing = CSemiring(R, (x,))

matrixM = matrixMultiplication(CRing, m)
M1 = Model(R, b0,  m, matrixM, simplify=False)

print("============ ===========")
last = None
for i,b in enumerate(M1): 
    last = b
    #print('.', end='')
    #print(f'{simplification(b)}')
    #print(f'{(b)}')

for i in range(10):
        print(f'B[{i+1}]: {last[0](i+1)}')

print("============ ===========")

##########################
# Using two variables. The second one represents whether the committee must be
# formed also by external members

x,y = symbols('x y')
 
def cte(n):
    '''The constant constraint returning the value n'''
    return Lambda((x,y), n)

m = [ 
      [cte(0.3), cte(0.2), cte(0.3), cte(0.2)],
      [cte(0.2), cte(0.3), cte(0.1), cte(0.4)],
      [cte(0.2), cte(0.4), cte(0.2), cte(0.2)],
      [cte(0.1), cte(0.1), cte(0.5), cte(0.3)]]

def impdef(a,b,c,d):
    ''' y=0 -> a <= x <= b and 
        y=1 -> c <= x <= d'''
    return Lambda((x,y), Piecewise((1.0, ((Ge(x, a) & Le(x,b)) | Eq(y,1)) &  ((Ge(x, c) & Le(x,d)) | Eq(y,0))   ), (0.0, True)))


def impdef2(yv,a,b):
    ''' y = yv and  a <= x <= b'''
    return Lambda((x,y), Piecewise((1.0, Eq(y, yv) & ( Ge(x,a) & Le(x, b  ) )), (0.0, True)))


c1 = impdef(4,6,3,5)
c2 = impdef(5,10,5,10)
c3 = impdef(6,7,3,4)
#c4 = impdef(1,4,2,4)
c4 = impdef2(1,2,4)

b0 = [c1, c2, c3, c4]

# Building the R-semiring 
CRing = CSemiring(R, (x,y))

matrixM = matrixMultiplication(CRing, m)
M1 = Model(R, b0,  m, matrixM, simplify=False)

for i,b in enumerate(M1): 
    last = b
    #print('.', end='')
    #print(f'{simplification(b)}')
    #print(f'{(b)}')

for i in range(10):
    for b in range(2):
        print(f'B[{i+1, b}]: {last[0](i+1,b)}')

print('Preference for y=0', sum(last[0](i+1,0) for i in range(10)))
print('Preference for y=1', sum(last[0](i+1,1) for i in range(10)))
print()

for i in range(10):
    print(f'Preference for x={i+1}', sum(last[0](i+1,j) for j in range(2)))
