'''

Constraint Opinion Model
=========================

This module defines the update function in a Constraint Opinion Model as matrix
multiplication. Some facilities are implemented to generate the next state of
the agents. 

This module defines also the function "inverse", useful to define distances
between constraints and then, polarization measures. 

'''

from semiring import *

class Model:
    '''
    A constraint opinion model
    '''

    def __init__(self, semiring, initState, influence, update, simplify=True, compare=None):
        '''
        Args:
            semiring : The underlying semiring
            initState: The initial state
            influence: The influence graph (a list of lists)
            update: The update function (from C-lists to C-lists)
            simplify : determining if simplification on expression is performed or not
            compare : The function determining whether the fixpoint has been reached (see `__next__`)
        '''
        self._semiring  = semiring
        self._B = initState
        self._influence = influence
        self._update = update
        self._next = None
        self._compare = compare
        self._simplify = simplify

    def __iter__(self):
        return self

    def __next__(self):
        '''Stops when a fixpoint has been reached'''

        if self._next is None: # First iteration
            self._next = self._B
        else:
            new = self._update(self._next)
            if self._simplify:
                new = [ simplify(x) for x in new]

            check = False
            if self._compare is None:
                check = new == self._next
            else:
                check= self._compare(new, self._next)

            if check: raise StopIteration

            self._next = new

        return self._next


# Multiplying matrices using the semiring operations
def matrixMultiplication(semiring, graph):
    '''
    Returns:
            A function of type C^n -> C^n
    '''
    def mm(opinion):
        l = len(graph)
        newOp = list(semiring.zero() for _ in  graph)
        for i in range(l):
            for j in range(l):
                newOp[i] = semiring.plus(newOp[i], semiring.times(opinion[j], graph[i][j]))
        return newOp

    return mm

def inverse(domain, c):
    '''
    Inverse of a constraint useful to define polarization measures 
    Returns:
        a map S -> 2^(V->S)
    '''
    result = {}
    for d in domain:
        s = c(*d)
        if s in result:
            result[s].add(d)
        else:
            result[s] = { d }

    return result

def simplification(B):
    '''
    Simplifying the expressions in a list of opinions
    '''
    return [ simplify(x) for x in B ]

def printOpinion(B,dom):
    '''
    Printing the constraints in the vector/opinion B where the values of the
    variables are taken from the domain dom 
    '''
    for d in dom:
        for i,c in enumerate(B):
            print(f'B{i}({d}) = {c(*d)}', end="\t")
        print("")

