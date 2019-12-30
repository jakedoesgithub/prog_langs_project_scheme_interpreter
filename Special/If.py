# If -- Parse tree node strategy for printing the special form if

from Tree import BoolLit
from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class If(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printIf(t, n, p)
    def eval(self, t, env):
        cond = t.getCdr().getCar().eval(env)                    #element 2 is condition
        if cond.boolVal:
            return t.getCdr().getCdr().getCar().eval(env)       #element 3 is evaluated if cond is true
        return t.getCdr().getCdr().getCdr().getCar().eval(env)  #else, element 4 is evaluated
        
        self._error("If does not define eval()")
