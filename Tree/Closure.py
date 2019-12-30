# Closure -- the data structure for function closures

# Class Closure is used to represent the value of lambda expressions.
# It consists of the lambda expression itself, together with the
# environment in which the lambda expression was evaluated.

# The method apply() takes the environment out of the closure,
# adds a new frame for the function call, defines bindings for the
# parameters with the argument values in the new frame, and evaluates
# the function body.

import sys
from Tree import Node
from Tree import Environment
from Tree import Nil
from Tree import Cons

class Closure(Node):
    util = None

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, f, e, trimmed = False):
        if not trimmed:
            f.setCar(f.getCar().getCdr())
        self.fun = f                    # a lambda expression
        self.env = e                    # the environment in which
                                        # the function was defined

    def getFun(self):
        return self.fun

    def getEnv(self):
        return self.env

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Procedure")
        if self.fun != None:
            self.fun.print(abs(n) + 4)
        for _ in range(abs(n)):
            sys.stdout.write(' ')
        sys.stdout.write(" }\n")
        sys.stdout.flush()

    def apply(self, args):

        #create a new enviroment where env will be the current env then
        #the frame variable of the new enviroment will represent the function environment
        environment = Environment(self.getEnv())
        parameters = self.fun.getCar()
        body= self.fun.getCdr()

        #Check that argument count is correct, if the parameters are a well-formed list
        if self.util.length(parameters) != -1 and self.util.length(parameters) is not self.util.length(args):
            sys.stdout.write("Invalid argument count\n")
            return Nil.getInstance()
        
        #Map all required parameters to arguments
        while parameters.isPair():
            environment.define(parameters.getCar(), Cons(args.getCar(), Nil.getInstance()))
            args = args.getCdr()
            parameters = parameters.getCdr()
        #if there is a remaining list argument, define it
        if not parameters.isNull():
            environment.define(parameters, Cons(args, Nil.getInstance()))
        #evaluating function
        return self.util.begin(body,environment)

    #Unspecified how eval should react. This should never get called but its in the UML
    def eval(self, env):
        return Nil.getInstance()
