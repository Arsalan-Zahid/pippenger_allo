from abc import ABC, abstractmethod
from ecdsa.ellipticcurve import Point
from modp import ModP


class Group(ABC):

    def __init__(self, unit: ModP | Point, order: int):
        self.unit : ModP | Point = unit
        'A ModP with x = 1 and p is set by MultiIntModP\'s constructor.'

        self.order : int = order
        'Second arg to constructor.'
    
    @abstractmethod
    def mult(self, x, y):
        pass
    
    def square(self, x):
        return self.mult(x, x)
    

class MultIntModP(Group):
    def __init__(self, p : int, order : int):
        Group.__init__(self, ModP(1, p), order)

    def mult(self, x, y):
        return x*y

class EC(Group):
    def __init__(self, curve):
        Group.__init__(self, Point(None,None,None),  curve.order)
    
    def mult(self, x, y):
        return x + y