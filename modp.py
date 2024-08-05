class ModP:

    num_of_mult: int = 0
    @classmethod
    def reset(cls):
        cls.num_of_mult = 0

    def __init__(self, x : int, p : int):
        self.x : int = x
        self.p : int = p

    def __add__(self, y : 'int | ModP') -> 'ModP':
        "Adds an int to the ModP's x value, OR adds the x value's of 2 ModPs, then modulos it by p."

        # If adding an integer add it
        if isinstance(y, int):
            return ModP(self.x+y, self.p)

        # Else, add their x values, and modulo by p.
        assert self.p == y.p
        return ModP((self.x + y.x) % self.p, self.p)

    def __mul__(self, y : 'int | ModP') -> 'ModP':

        # Standard practice: If it's an integer, just multiply it
        # Else, if it's a modp w/ the same p, multiply their x's and mod it.

        type(self).num_of_mult += 1
        if isinstance(y, int):
            return ModP(self.x*y, self.p)
        assert self.p == y.p
        return ModP((self.x * y.x) % self.p, self.p)

    def __sub__(self, y : 'int | ModP') -> 'ModP':
        # Same as above
        if isinstance(y, int):
            return ModP(self.x-y, self.p)
        assert self.p == y.p
        return ModP((self.x - y.x) % self.p, self.p)

    def __pow__(self, n : int) -> 'ModP':
        # return ModP(pow(self.x, n, self.p), self.p)

        # Raises it to a integer power?
        exp: str = bin(n)
        value : 'ModP' = ModP(self.x, self.p)

        for i in range(3, len(exp)):
            value = value * value
            if(exp[i:i+1]=='1'):
                value = value*self
        return value

    def __neg__(self) -> 'ModP':
        return ModP(self.p - self.x, self.p)


    
    def __eq__(self, y) -> bool:
        return (self.x == y.x) and (self.p == y.p)

    
    def __str__(self) -> str:
        return str(self.x)
    def __repr__(self) -> str:
        return str(self.x)