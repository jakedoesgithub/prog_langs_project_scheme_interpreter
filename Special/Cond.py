# Cond -- Parse tree node strategy for printing the special form cond

from Tree import BoolLit
from Tree import Nil, Cons  
#from Tree import Unspecific
from Print import Printer
from Special import Special

class Cond(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printCond(t, n, p)
    def eval(self, t, env):
        tree = t.getCdr() #tree holds the conditions to check
        while not tree.isNull():
            block = tree.getCar() #block holds condition and result
            blockLength = self.util.length(block)
            if blockLength == 3:
                if block.getCdr().getCar().isSymbol() and block.getCdr().getCar().getName() == "=>":
                    proc = block.getCdr().getCdr().getCar().eval(env)
                    if proc.isProcedure():
                        return proc.apply( Cons(block.getCar().eval(env), Nil.getInstance()))
                return Nil.getInstance()                            #Only occurs if error
            elif block.getCar().isSymbol() and block.getCar().getName() == "else":
                return block.getCdr().getCar().eval(env)
            elif block.getCar().eval(env) == BoolLit.getInstance(True):
                return block.getCdr().getCar().eval(env)
            tree = tree.getCdr()
