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


# Dissected by Maya 

def subset_of(l):
    return sum(map(lambda r: list(combinations(l, r)), range(1, len(l)+1)), [])
    
    # SUM     

        # sum: a python built-in function that "returns a number, the sum of all items in an iterable" 
            # if two parameters it is sum(the tuple sequence to sum, an option number that can be added to the return value) 
                # looks like the sequence to sum comes from the map function. Analysis of that will be in the map comment. 
                # the second parameter is []. Maybe the first parameter of map is a list, which would allow it to be added into this empty list parameter.
                    # further map analysis below vvv 
        # https://www.w3schools.com/python/ref_func_sum.asp
    
    # MAP 

        # map: a python built-in function that "applies a given function to each item of iterable (like list, tuple etc.) and returns a list of results or map object." 
            # if two parameters it is map(function, iterable)
            # the function must have ONE parameter for each iterable 
            # you can add iterables that would correspond to having more parameters in the function (which is the first parameter of map)
            # it looks like the function passed in is lambda r: list(combinations(l, r)) and the iterable to have each number have that function done on it is range(1, len(l) +1)) 
                # further analysis of combinations and lambda below vvv
        #  https://www.geeksforgeeks.org/python-pass-multiple-arguments-to-map-function/

    # COMBINATIONS 
    
        # combinations: a python itertools function that returns "r length subsequences of elements from the input iterable."
                      # "The output is a subsequence of product() keeping only entries that are subsequences of the iterable. The length of the output is given by math.comb() which computes n! / r! / (n - r)! when 0 ≤ r ≤ n or zero when r > n." 
                      # seems like this is what I learned in CS 151. Combinations WITHOUT repeats. Remember order doesn't matter like it does with permutations.
            # Some examples: 
                # combinations('ABCD', 2) → AB AC AD BC BD CD
                # combinations(range(4), 3) → 012 013 023 123

        # https://docs.python.org/3/library/itertools.html#itertools.combinations
    
    # LAMBDA 

        # lambda: "A lambda function is a small anonymous function. A lambda function can take any number of arguments, but can only have one expression."
            # simple example: 
                # x = lambda a : a + 10
                # print(x(5))
                # ouput is 15. 
        # lambda is often used as the return for another function so you can make custom small functions. This is how it is used here, notingly. 
            # simple example (Use that function definition to make a function that always doubles the number you send in): 
                # def myfunc(n):
                    # return lambda a : a * n

            # mydoubler = myfunc(2)

            # print(mydoubler(11))
        # https://www.w3schools.com/python/python_lambda.asp
    
    # RANGE 

        # range: a python built-in "function that returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and stops before a specified number." 
            # if two parameters it is range(start that is inclusive, stop that is exclusive)
            # in this case, start is 1 and the length of l is the last number that will be returned.
        # https://www.w3schools.com/python/ref_func_range.asp

    # SO, after dissection of subset_of(l), this is what I understand: 
        # There is a lot happening, but to put it together let's go from the innermost part to the outermost part.
            # the map function is using lambda and creating a combinations function for all lengths of l from 1 to l. 
                # so now there are l amount of functions that allow you to return all the subsets of that specific l of any inputted length r.  
        # The user must specify the length with a parameter (which in this case is r)
        # The sum function I am not currently sure why it is there. Perhaps it creates a list of the function definitions? 
class Pippenger:

    # Constructor of the pippenger class 
    # Note: self is like the "this" keyword in C++ 
    def __init__(self, group : Group):
        self.G : Group = group
        'G is the group used to initialize the Pippenger instance.'
        
        self.order : int = group.order
        'Order p = 2^lambda'
        
        self.lamb : int = group.order.bit_length()source //scratch/aross50/virtEnvs/vAllo/bin/activate
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
        

        # I don't know if this typing is right
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
        
    def _multiexp_bin(self, gs: list[Group], es: list[int] -> list):
        # gs is a list of elements of G, es is a list of integer exponents
        # looks like gs and es have to be the same length 
        assert len(gs) == len(es)
        #  M is the length of gs 
        M: int = len(gs)
        # b is the floor of a calculation that appeared in effeciency analysis section of Bootle's paper. 
        # This calculation also appeared in section 6 of Bernstein's paper under "Recursion level 1"
        b: int = floor( log2(M) - log2(log2(M)) )                                 
        b = b if b else 1 # prevents b from being 0

        # Figure out what subsets is and TS 

        # 1. Subsets 

            # First of all, what is the min function? 
                # a python built-in function that "returns the item with the lowest value, or the item with the lowest value in an iterable." 
                    # min(n1, n2, n3, ...) 
                    # or 
                    # min(iterable)
                    # simple example:
                        # a = (1, 5, 3, 9)
                        # x = min(a)
                        # output is 1
                    # https://www.w3schools.com/python/ref_func_min.asp

            # NOTE, subsets is defined using list comprehension 
                # The syntax
                    # newlist = [expression for item in iterable if condition == True] 
                    # "The condition is optional and can be omitted."
                    # "The expression is the current item in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list."
                # simple example: 
                    # newlist = [x for x in fruits if x != "apple"] 
                    # ^^ Only accept items that are not "apple" ^^ 
                # https://www.w3schools.com/python/python_lists_comprehension.asp

            # NOTE that i, M, and b are integers. 
            # This list comprehension is generating the list of subsets 
                # Inner parts: 
                    # range(0, M, b): This creates a range of integers starting from 0 up to M (exclusive) with a step of b. It generates the starting indices for each subset.
                    # range(i, min(i+b, M)): For each i in the range, this creates a range from i to min(i+b, M). This range determines the elements in each subset. The min(i+b, M) ensures that the range does not exceed M.
                    # list(...): This converts each range object into a list of integers.
                # ^^ explained by GPT and I think it makes sense. I don't think I should spend too much time on the small details and GPT has been a great help at accelerating my understandings of this code. 
                    # I am guided on what to look up, such as list comprehension 
                # https://chatgpt.com/share/fba22a15-2351-45f2-8d0b-f300b55dd5a4
       

        subsets: list[list[int]] = [list(range(i,min(i+b,M))) for i in range(0,M,b)]

        # 2. Ts 
        
        # The line of code below seems to be using list comprehension, as well. 
        # What GPT has to say:
            # Functionality: For each subset S in subsets, the line generates a dictionary where:
                # Each key is a tuple representing a non-empty subset of S (generated by subset_of(S)).
                # Each value is None.
            # Purpose: This creates a list of dictionaries, each storing all non-empty subsets of S as keys, effectively capturing the power set (excluding the empty set) for each S.
        # https://chatgpt.com/share/0fc42105-691b-4886-ab97-ff2fb94039c2

        Ts: Dict[tuple, None] = [{sub: None for sub in subset_of(S)} for S in subsets] 

        # What is the zip function: 
            # It is a python built-in function that returns a zip object, which is an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together etc.
            # If the passed iterables have different lengths, the iterable with the least items decides the length of the new iterator.
            # Syntax: zip(iterator1, iterator2, iterator3 ...)
            # https://www.w3schools.com/python/ref_func_zip.asp-

        
        # https://chatgpt.com/share/3e60ab07-fde1-4127-93b7-ae26029a9fca
        # > 
        for T,S in zip(Ts, subsets):
            for i in S:
                T[(i,)] = gs[i]
            # Recursively set the subproducts in T
            def set_sub(sub: tuple) -> None:
                if T[sub] is None:
                    if T[sub[:-1]] is None:
                        set_sub(sub[:-1])
                    # TODO: Change this for allo.     
                    T[sub] = self.G.mult(T[sub[:-1]], gs[sub[-1]])
            for sub in T:
                set_sub(sub)
        # > 

        Gs: list = []
        # for k = 0 going up to minus one of the length of the first exponent in es
        for k in range(len(es[0])):
            # TODO: Change in allo? 
            tmp: ModP | Point = self.G.unit
            for T,S in zip(Ts, subsets):
                #  Another list comprehension.      sub_es = [j for j in S if es[j][k]]
                sub_es: list  = [j for j in S if es[j][k]]
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

            
