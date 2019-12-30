# Let -- Parse tree node strategy for printing the special form let

from Tree import Nil
from Tree import Environment
from Tree import Cons
from Print import Printer
from Special import Special

class Let(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printLet(t, n, p)
    def eval(self, t, env):
        newEnv = Environment(env)
        bindings = t.getCdr().getCar()
        for i in range(self.util.length(bindings)):
            identifier = bindings.getCar().getCar()
            val = bindings.getCar().getCdr().getCar().eval(env)
            newEnv.define(identifier, Cons(val, Nil.getInstance()))
            bindings = bindings.getCdr()
        body = t.getCdr().getCdr()
        return self.util.begin(body, newEnv)