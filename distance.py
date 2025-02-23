'''
Distance between constraints using the Hausdorff distance between the sets of
solutions 
'''

from models import *
import math

def dist(e, X, distance=math.dist):
    '''Forward distance'''
    return min(distance(x,e) for x in X)

# Hausdorff Distance

def Hdist(X,Y,distance=math.dist):
    if X == set() and Y == set():
        return 0
    if X == set() or Y == set():
        return math.inf
    else: 
     return max(max(dist(e,X,distance) for e in Y),max(dist(e,Y, distance) for e in X))

def Sol(domain, c, s):
    '''The solutions that map c into a value s' >= s
        it assumes that >= is defined on semiring values
    '''
    S = set()
    valuations = inverse(domain, c)
    for x in valuations:
        if x >= s:
            for v in valuations[x]:
                S.add(v)
    return S

def Distance(domain, c1, c2,s):
    '''Distance between (the solutions of) two constraints'''
    return Hdist(Sol(domain,c1,s), Sol(domain,c2,s))

