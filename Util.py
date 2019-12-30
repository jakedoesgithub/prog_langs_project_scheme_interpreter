# Util -- Utility functions 

from Tree import Nil
from Tree import Cons
from Special import Begin
from Special import Cond
from Special import Define
from Special import If
from Special import Lambda
from Special import Let
from Special import Quote
from Special import Set
from Special import Regular

class Util:
    # parseList selects the Special node to attach to a Cons node
    def parseList(self, t):
        if not t.getCar().isSymbol():
            return Regular()
        else:
            name = t.getCar().getName()
            if name == "quote":
                return Quote()
            elif name == "lambda":
                return Lambda()
            elif name == "begin":
                return Begin()
            elif name == "if":
                return If()
            elif name == "let":
                return Let()
            elif name == "cond":
                return Cond()
            elif name == "define":
                return Define()
            elif name == "set!":
                return Set()
            else:
                return Regular()

    # length returns the length of a well-formed list exp and -1 otherwise
    def length(self, exp):
        if exp.isNull():
            return 0
        if not exp.isPair():
            return -1
        n = self.length(exp.getCdr())
        if n == -1:
            return -1
        return n + 1

    # mapeval calls eval on every list element of exp
    def mapeval(self, exp, env):
        if exp.isNull():
            return Nil.getInstance()
        return Cons(exp.getCar().eval(env), self.mapeval(exp.getCdr(), env))

    # begin calls eval on all list elements and returns the last value
    def begin(self, exp, env):
        res = exp.getCar().eval(env)
        cdr = exp.getCdr()
        if cdr.isNull():
            return res
        return self.begin(cdr, env)
