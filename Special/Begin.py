# Begin -- Parse tree node strategy for printing the special form begin

from Tree import Nil
from Print import Printer
from Special import Special
class Begin(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printBegin(t, n, p)
    #Eval should evaluate all expressions, returning the result of the last expression
    def eval(self, t, env):
        tree = t.getCdr()
        lastRes = None
        while not tree.isNull():
            lastRes =tree.getCar().eval(env)
            tree = tree.getCdr()
        return lastRes