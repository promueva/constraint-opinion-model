'''
This module defines: 
 - The abstract class defining the operations on the semiring
 - The following subclasses as well-known instances of semirings:
     - Crisp (true/false values)
     - R (non negative real numers)
     - CSemiring (lifting the operations to constraints)
'''

from abc import ABC, abstractclassmethod
from functools import reduce
from sympy import *
from itertools import chain, combinations

import utils


class Semiring(ABC):
    '''
    An object of type ```Semiring``` provides the needed operations to
    represent the structure 
    :math:`\\langle A, \\oplus, \\otimes, \\bot, \\top\\rangle`

    All the methods of this class are abstract but ```sum``` and ```prod```
    that compute :math:`\\sum_i a_i` and :math:`\\Pi_i a_i` respectively. 
    '''

    @abstractclassmethod
    def plus(cls,x,y):
        '''+ operator'''
        pass

    @abstractclassmethod
    def times(cls,x,y):
        '''* operator'''
        pass

    @abstractclassmethod
    def one(cls):
        '''1 constant'''
        pass

    @abstractclassmethod
    def zero(cls):
        '''0 constant'''
        pass

    @classmethod
    def sum(cls,values):
        '''
        Returns:
            :math: `\\sum_i a_i` over a collection of semiring values
        '''
        return reduce(cls.plus, values, cls.zero())

    @classmethod
    def prod(cls,values):
        '''
        Returns:
            :math: `\\Pi_i a_i` over a collection of semiring values
        '''

        return reduce(cls.times, values, cls.one())


class Crisp(Semiring):
    '''
    Boolean semiring
    '''

    @classmethod
    def plus(cls,x,y): return Or(x,y)

    @classmethod
    def times(cls,x,y): return And(x, y)

    @classmethod
    def one(cls): return S.true

    @classmethod
    def zero(cls): return S.false


class R(Semiring):
    '''
    Non negative real numbers.
    One (infty) is not defined
    '''

    @classmethod
    def plus(cls,x,y): return x + y

    @classmethod
    def times(cls,x,y): return x * y

    @classmethod
    def one(cls): pass

    @classmethod
    def zero(cls): return 0.0

class Fuzzy(Semiring):
    '''
    Interval [0,1] with Max as + and min as *
    '''

    @classmethod
    def plus(cls,x,y): return Max(x, y)

    @classmethod
    def times(cls,x,y): return Min(x , y)

    @classmethod
    def one(cls): 1.0

    @classmethod
    def zero(cls): return 0.0

class Prob(Semiring):
    '''
    Interval [0,1] where * is multiplication and + is max
    '''

    @classmethod
    def plus(cls,x,y): return Max(x, y)

    @classmethod
    def times(cls,x,y): return x * y 

    @classmethod
    def one(cls): 1.0

    @classmethod
    def zero(cls): return 0.0
        
def Set(iset):
    '''
    Powetset construction

    Args:
        - iset: A finite set

    Returns:
        A semiring where elements are subsets of `iset`, 
        :math:`+` is :math:`\\cup` and :math: `\\times` is :math:`\\cap`
    '''
    class CSet(Semiring):

        @classmethod
        def plus(cls,x,y): return x.union(y)

        @classmethod
        def times(cls,x,y): return x.intersection(y)

        @classmethod
        def one(cls): return iset

        @classmethod
        def zero(cls): return set()

    return CSet

def CSemiring(semiring, vs):
    '''
    Lifiting operations at the level of constraints.

    Args:
       -semiring: underlying semiring for the constraints
       -vs: tuple defining the parameters of constraints

    Returns: 
       The semiring lifted to constraints math:
        c_1 \\times c_2 (\\vec{v}) = c_1(v) \\times c_2(v) 
        c_1 \\plus c_2 (\\vec{v}) = c_1(v) \\plus c_2(v) 
    '''
    class C(Semiring):

        @classmethod
        def plus(cls,x,y): return Lambda(vs,  semiring.plus(x(*vs), y(*vs)))

        @classmethod
        def times(cls,x,y): 
            return Lambda(vs,  semiring.times(x(*vs), y(*vs)))

        @classmethod
        def one(cls): return Lambda(vs, semiring.one())

        @classmethod
        def zero(cls): return Lambda(vs, semiring.zero())

    return C
