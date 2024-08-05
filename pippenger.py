from sympy import integer_nthroot
from math import log2, floor
from itertools import combinations
from group import Group



'''def integer_nthroot(y, n):
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
'''



def subset_of(l):
    return sum(map(lambda r: list(combinations(l, r)), range(1, len(l)+1)), [])

class Pippenger:

    def __init__(self, group : Group):
        self.G : Group = group
        'G is the group used to initialize the Pippenger instance.'
        
        self.order : int = group.order
        'Order p = 2^lambda'
        
        self.lamb : int = group.order.bit_length()
        'lamb is the number of bits required to represent the order.'

    # Returns g^(2^j)
    # This is for section 2, g'_(i,j)
    def _pow2powof2(self, g, j):
        tmp = g
        for _ in range(j):
            tmp = self.G.square(tmp)
        return tmp

    # multiexp - Arsalan 
    
    # Returns Prod of all g_i ^ e_i
    def multiexp(self, gs: list[Group], es: list[int]) -> int:

        # gs is group elements
        # es is the exponents
        if len(gs) != len(es):
            raise Exception('Different number of group elements and exponents')

        # Modulo all of them by the order
        # TODO replace with an allo loop
        es: list[int] = [ei%self.G.order for ei in es]

        #remove in allo?
        if len(gs) == 0:
            return self.G.unit
            # If there is only one group, return self's unit?


        lamb: int = self.lamb
        'lamb is the number of bits required to represent the order.'

        N = len(gs)
        #TODO bring in from sympy
        # Also note that the sympy function returns a tuple, 
        # but this gets the first element and ceil's it.

        # so it does floor(y**(1/n))
        # but this does ceil(y**(1/n))
        # this extends to ceil((lamb//N)**(1/2))
        #   Or ceil(sqrt(lamb//N))
        # For the other one, 
        #   ceil(sqrt(lamb*N))

        # TODO figure out what these are
        s: int = integer_nthroot(lamb//N, 2)[0]+1
        t: int = integer_nthroot(lamb*N,2)[0]+1
        gs_bin: list[list[Group]] = []

       
        # For every one of our Pi*Ki?
        for i in range(N):

            
            # I believe this is gathering all the g's to the right side of figure 2.1
            tmp = [gs[i]]
            for j in range(1,s): # Go through one to sqrt(lamb//N), or s. 
                # Take the last element in the temp array, square it, and append it to the back of the temp array
                tmp.append(self.G.square(tmp[-1])) 
                # So this would basically be an array []
                #   This definitely seems to be building the binary integer in 2.1 down a column

            #It's interesting how it appends an array onto this array, making this a 2d array
            # It's like it's all the e_i's concatenated together
            gs_bin.append(tmp)
        

        # I don't kno if this typingg is right
        es_bin: list[list[list[int]]] = []
        # It looks like this algorithm skips the last factorization in the code interestingly enough in section 2?
        # actually idk
        for i in range(N):
            tmp1: list[list[int]] = []
            for j in range(s):
                tmp2: list[int] = []
                # interesting how this loops on the outside
                for k in range(t):
                    # get the integer in a binary string, pad it to the left to s*t, then get index 
                    # Maybe this is for e'? section 2
                    # It looks like this part is getting the integers to the left of 2.1
                    tmp2.append(int( bin(es[i])[2:].zfill(s*t)[-(j+s*k+1)]) )
                # So tmp1 will be more of a 2d array
                tmp1.append(tmp2)
                # and es bin a 3d array?
            es_bin.append(tmp1)
        
        # I believe this part is a column for every e_i until e_(N-1) as shown in 2.1
        Gs = self._multiexp_bin(
                [gs_bin[i][j] for i in range(N) for j in range(s)],
                [es_bin[i][j] for i in range(N) for j in range(s)]
                )

        ans2 = Gs[-1]
        for k in range(len(Gs)-2,-1,-1):
            ans2 = self._pow2powof2(ans2, s)
            ans2 = self.G.mult(ans2, Gs[k])

        return ans2

    # _multiexp_bin - Maya 
        
    def _multiexp_bin(self, gs: list[int], es: list[int]):
        # gs is a list of elements of G, es is a list of integer exponents
        # looks like gs and es have to be the same length 
        assert len(gs) == len(es)
        M: int = len(gs)
        b: int = floor( log2(M) - log2(log2(M)) ) # this calculation is used in the effeciency analysis section of Bootle's paper. 
                                        
        b = b if b else 1
        subsets: list[list[int]] = [list(range(i,min(i+b,M))) for i in range(0,M,b)]
        Ts = [{sub: None for sub in subset_of(S)} for S in subsets] # Look like sympy is needed
                                                                    # Was not able to find the type on VS Code

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

            
