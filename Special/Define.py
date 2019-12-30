# Define -- Parse tree node strategy for printing the special form define

from Tree import Ident
from Tree import Nil
from Tree import Cons
#from Tree import Void
from Print import Printer
from Special import Special
from Tree import Closure
class Define(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printDefine(t, n, p)
    def eval(self, t, env):
        #if variable definition
        if t.getCdr().getCar().isSymbol():
            env.define(t.getCdr().getCar(), Cons(t.getCdr().getCdr().getCar().eval(env), Nil.getInstance()))
        #If definition is for a closure
        elif t.getCdr().getCar().isPair():
            env.define(t.getCdr().getCar().getCar(), Cons(Closure(t.getCdr(), env), Nil.getInstance()))
        return Nil.getInstance()