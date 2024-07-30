# Used for Allo
# Python Algorithm from https://github.com/wborgeaud/python-pippenger/blob/master/src/pippenger.py
# Maya and Arsalan 

from sympy import integer_nthroot
from math import log2, floor
from itertools import combinations
# ^^ Have to figure out ways to do this w/o ^^ 

# Using example files from Allo github as an example to mimic
# Such as gemm.py 

import os
import json
import allo
from allo.ir.types import int32, float32
import allo.ir.types as T

def subset_of(l):
    return sum(map(lambda r: list(combinations(l, r)), range(1, len(l)+1)), [])

def pippenger(concrete_type, p, r, q, beta=0.1):
    def __init__(self, group):
        self.G = group
        self.order = group.order
        self.lamb = group.order.bit_length()
    
    # Returns g^(2^j)
    def _pow2powof2(self, g, j):
        tmp = g
        for _ in range(j):
            tmp = self.G.square(tmp)
        return tmp

    # Returns Prod g_i ^ e_i
    def multiexp(self, gs, es):
        if len(gs) != len(es):
            raise Exception('Different number of group elements and exponents')

        es = [ei%self.G.order for ei in es]

        if len(gs) == 0:
            return self.G.unit

        lamb = self.lamb
        N = len(gs)
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

    def kernel_pip[
        T: (float32, int32), P: int32, Q: int32, R: int32
    ](A: "T[P, Q]", B: "T[Q, R]", C: "T[P, R]", output: "T[P, R]"):
        out_AB: T[P, R]
        mm1[T, P, Q, R](A, B, out_AB)
        ele_add[T, P, R](out_AB, C, output)

    sch0 = allo.customize(__init__, instantiate=[concrete_type, p, q, r])
    sch1 = allo.customize(_pow2ofpow2, instantiate=[concrete_type, p, r])
    sch2 = allo.customize(multiexp, instantiate=[concrete_type, p, q, r])
    sch3 = allo.customize(_multiexp_bin, instantiate=[concrete_type, p, q, r])

    sch = allo.customize(kernel_pip, instantiate=[concrete_type, p, q, r])
    sch.compose(sch0)
    sch.compose(sch1) 
    sch.compose(sch2)
    sch.compose(sch3)
    

if __name__ == "__main__":
    P = 5
    R = 5
    Q = 5
    beta = 0.1
    concrete_type = float32
    sch = pippenger(concrete_type, P, R, Q, beta=beta)
    mod = sch.build()
    


            
