from itertools import chain, combinations

def powerset(iterable):
    '''
    Power set construction.
    :returns a set of tuples
    '''

    s = list(iterable)
    return [ set(x) for x in chain.from_iterable(combinations(s, r) for r in range(len(s)+1)) ]

