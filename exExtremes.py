'''
Expressing extreme and moderate opinions. See more details in the
[paper](./paper.pdf)

'''

from models import *
import matplotlib.pyplot as plt
import numpy as np
import random

# A variables taking values in [1..5]
p  = Symbol('p')

# interval(2,4) means that "I'm OK with the options 2,3,4 (with equal preference between them)
def interval(l,u):
    return Lambda((p,), Piecewise((1.0/(1+u-l), Ge(p, l) & Le(p ,u)), (0.0, True)))

#Equal preference for all the 5 values
def cte(n):
    return Lambda((p,), n)

def opextreme(v1,v2):
    '''Assigning v1 in the extremes and v2 otherwise'''
    return Lambda((p,), Piecewise( (v1, Or(Eq(p,1), Eq(p,5))), (v2, True)))

ext = opextreme(1.0, 0.0)
notext = opextreme(0.0, 1.0)
dontknow = interval(1,5)

CRing = CSemiring(R, (p,))

def compare(new, old):
    EPSILON = 0.0001
    '''Two opinions are the same if they coincide for all the values in the domain'''
    for i, x in enumerate(new):
        for j in range(5):
            if abs(x(j+1) - old[i](j+1)) > EPSILON: return False

    return True

def generate_random_list(size):
    '''Generate a list o size random values in [0,1] s.t. sum(list) = 1.0'''
    if size < 1:
        raise ValueError("Size must be at least 1.")

    random_values = sorted([random.random() for _ in range(size - 1)])
    random_values = [0] + random_values + [1]
    result = [(random_values[i + 1] - random_values[i]) for i in range(size)]
    return result

def multiply_matrices(A, B):
    """Multiply two square matrices A and B represented as lists of lists."""
    size = len(A)
    if size != len(B) or any(len(row) != size for row in B):
        raise ValueError("Both matrices must be square and of the same dimensions.")

    result = [[sum(A[i][k] * B[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
    return result

def matrix_stability(A, tolerance=1e-9, max_iterations=1000):
    """Continually multiply the matrix A with itself until stability or max iterations."""
    size = len(A)
    current = [row[:] for row in A]  # Deep copy of A
    iterations = 0

    while iterations < max_iterations:
        next_matrix = multiply_matrices(current, current)
        # Check stability by comparing all elements
        if all(abs(next_matrix[i][j] - current[i][j]) < tolerance for i in range(size) for j in range(size)):
            break
        current = next_matrix
        iterations += 1

    return current, iterations

N = 10

m = [ generate_random_list(N) for _ in range(N) ]
m,_ = matrix_stability(m)

m = [ [cte(x) for x in m[i]]  for i in range(N)]

# The matrix x is already a "consensus" (all the rows are the same)
matrixM = matrixMultiplication(CRing, m)

models = [ Model(R, [ext for _ in range(i)] + [dontknow for _ in range(N-i)],  m, matrixM, False, compare) for i in range(N+1) ] 

data = [None for _ in range(len(models))]
for i,M in  enumerate(models):
    print(i)
    j=0
    for _,b in enumerate(M):  
        data[i] = b
        if j > 1: break
        j += 1
        

x_label = [i+1 for i in range (5)]
data = { f'B{i+1}': [ round(float(data[i][0](j+1)),2) for j in range(5) ] for i in range(len(models)) }

# Note that f(0) == f(4) (extremes) and f(1) == f(2) == f(3).
# Onlye f(0) and f(1) are plotted
data = [ (x[0], x[1], x[0] - x[1]) for x in data.values()]

print(data)
