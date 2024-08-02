#from sympy import integer_nthroot
from math import log2, floor
from itertools import combinations
from group import Group

# hello 

def integer_nthroot(y, n):
    """
    Return a tuple containing x = floor(y**(1/n))
    and a boolean indicating whether the result is exact (that is,
    whether x**n == y).

    Examples
    ========

    >>> from sympy import integer_nthroot
    >>> integer_nthroot(16, 2)
    (4, True)
    >>> integer_nthroot(26, 2)
    (5, False)

    To simply determine if a number is a perfect square, the is_square
    function should be used:

    >>> from sympy.ntheory.primetest import is_square
    >>> is_square(26)
    False

    See Also
    ========
    sympy.ntheory.primetest.is_square
    integer_log
    """
    y, n = as_int(y), as_int(n)
    if y < 0:
        raise ValueError("y must be nonnegative")
    if n < 1:
        raise ValueError("n must be positive")
    if y in (0, 1):
        return y, True
    if n == 1:
        return y, True
    if n == 2:
        x, rem = mpmath_sqrtrem(y)
        return int(x), not rem
    if n > y:
        return 1, False
    # Get initial estimate for Newton's method. Care must be taken to
    # avoid overflow
    try:
        guess = int(y**(1./n) + 0.5)
    except OverflowError:
        exp = _log(y, 2)/n
        if exp > 53:
            shift = int(exp - 53)
            guess = int(2.0**(exp - shift) + 1) << shift
        else:
            guess = int(2.0**exp)
    if guess > 2**50:
        # Newton iteration
        xprev, x = -1, guess
        while 1:
            t = x**(n - 1)
            xprev, x = x, ((n - 1)*x + y//t)//n
            if abs(x - xprev) < 2:
                break
    else:
        x = guess
    # Compensate
    t = x**n
    while t < y:
        x += 1
        t = x**n
    while t > y:
        x -= 1
        t = x**n
    return int(x), t == y  # int converts long to int if possible




def subset_of(l):
    return sum(map(lambda r: list(combinations(l, r)), range(1, len(l)+1)), [])

class Pippenger:
    def __init__(self, group : Group):
        self.G : Group = group
        self.order : int = group.order
        # self.lamb is the number of bits required to represent the order.
        self.lamb : int = group.order.bit_length()
    
    # Returns g^(2^j)
    def _pow2powof2(self, g, j):
        tmp = g
        for _ in range(j):
            tmp = self.G.square(tmp)
        return tmp

    # Returns Prod g_i ^ e_i
    def multiexp(self, gs: list[int], es: list[int]):

        # gs is group elements
        # es is the exponents
        if len(gs) != len(es):
            raise Exception('Different number of group elements and exponents')

        # Modulo all of them by the order
        # TODO replace with an allo loop
        es = [ei%self.G.order for ei in es]

        #remove in allo
        if len(gs) == 0:
            return self.G.unit


        lamb = self.lamb
        N = len(gs)
        #TODO bring in from sympy
        # Also note that the sympy function returns a tuple 
        s = integer_nthroot(lamb//N, 2)[0]+1
        t = integer_nthroot(lamb*N,2)[0]+1
        gs_bin = []
        
        for i in range(N):
            tmp = [gs[i]]
            for j in range(1,s):
                tmp.append(self.G.square(tmp[-1]))
            gs_bin.append(tmp)
        es_bin = []
        for i in range(N):
            tmp1 = []
            for j in range(s):
                tmp2 = []
                for k in range(t):
                    tmp2.append(int( bin(es[i])[2:].zfill(s*t)[-(j+s*k+1)]) )
                tmp1.append(tmp2)
            es_bin.append(tmp1)
        
        Gs = self._multiexp_bin(
                [gs_bin[i][j] for i in range(N) for j in range(s)],
                [es_bin[i][j] for i in range(N) for j in range(s)]
                )

        ans2 = Gs[-1]
        for k in range(len(Gs)-2,-1,-1):
            ans2 = self._pow2powof2(ans2, s)
            ans2 = self.G.mult(ans2, Gs[k])

        return ans2
        
    def _multiexp_bin(self, gs, es):
        assert len(gs) == len(es)
        M = len(gs)
        b = floor( log2(M) - log2(log2(M)) )
        b = b if b else 1
        subsets = [list(range(i,min(i+b,M))) for i in range(0,M,b)]
        Ts = [{sub: None for sub in subset_of(S)} for S in subsets]

        for T,S in zip(Ts, subsets):
            for i in S:
                T[(i,)] = gs[i]
            # Recursively set the subproducts in T
            def set_sub(sub):
                if T[sub] is None:
                    if T[sub[:-1]] is None:
                        set_sub(sub[:-1])
                    T[sub] = self.G.mult(T[sub[:-1]], gs[sub[-1]])
            for sub in T:
                set_sub(sub)
            
        Gs = []
        for k in range(len(es[0])):
            tmp = self.G.unit
            for T,S in zip(Ts, subsets):
                sub_es = [j for j in S if es[j][k]]
                sub_es = tuple(sub_es)
                if not sub_es:
                    continue
                tmp = self.G.mult(tmp, T[sub_es])
            Gs.append(tmp)
            
        return Gs
    
    '''
    sch0 = allo.customize(__init__, instantiate=[concrete_type, p, q, r])
    sch1 = allo.customize(_pow2ofpow2, instantiate=[concrete_type, p, r])
    sch2 = allo.customize(multiexp, instantiate=[concrete_type, p, q, r])
    sch3 = allo.customize(_multiexp_bin, instantiate=[concrete_type, p, q, r])

    sch = allo.customize(kernel_pip, instantiate=[concrete_type, p, q, r])
    sch.compose(sch0)
    sch.compose(sch1) 
    sch.compose(sch2)
    sch.compose(sch3)
    '''

            
