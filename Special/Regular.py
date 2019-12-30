# Regular -- Parse tree node strategy for printing regular lists

from Tree import Nil
from Print import Printer
from Special import Special
import sys
class Regular(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printRegular(t, n, p)
    def eval(self, t, env):
        if not t.getCar().isPair():
            x = env.lookup(t.getCar())
            if x.isProcedure():
                #get parameters as a list
                params = self.util.mapeval(t.getCdr(), env)
                return x.apply(params)
            else:
                sys.stdout.write("Error: Attempt to invoke a non-procedure")
                return Nil.getInstance()
        else:
            res = t.getCar().eval(env)
            return res.apply(self.util.mapeval(t.getCdr(), env))