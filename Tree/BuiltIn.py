# BuiltIn -- the data structure for built-in functions

# Class BuiltIn is used for representing the value of built-in functions
# such as +.  Populate the initial environment with
# (name, BuiltIn(name)) pairs.

# The object-oriented style for implementing built-in functions would be
# to include the Python methods for implementing a Scheme built-in in the
# BuiltIn object.  This could be done by writing one subclass of class
# BuiltIn for each built-in function and implementing the method apply
# appropriately.  This requires a large number of classes, though.
# Another alternative is to program BuiltIn.apply() in a functional
# style by writing a large if-then-else chain that tests the name of
# the function symbol.

import sys
from Parse import *
from Tree import Node
from Tree import BoolLit
from Tree import IntLit
from Tree import StrLit
from Tree import Ident
from Tree import Nil
from Tree import Cons
from Tree import TreeBuilder

class BuiltIn(Node):
    env = None
    util = None

    @classmethod
    def setEnv(cls, e):
        cls.env = e
        #TODO: Cleanup
        builtins = ["b+","b-","b/", "b*", "b=", "b<", "number?", "null?", "procedure?","pair?", "cons", "car",
        "cdr", "set-car!", "set-cdr!", "eq?", "interaction-environment", "load", "read", "write", "display",
        "eval", "apply", "newline"]
        for i in builtins:
            cls.env.define(Ident(i),Cons(BuiltIn(StrLit(i)), Nil.getInstance()))

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, s):
        self.symbol = s                 # the Ident for the built-in function

    def getSymbol(self):
        return self.symbol

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Built-In Procedure ")
        if self.symbol != None:
            self.symbol.print(-abs(n) - 1)
        sys.stdout.write('}')
        if n >= 0:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def apply(self,args):
        argLength = self.util.length(args)
        name = self.symbol.strVal
        if name == "b+":                                                 #Binary Addition
            if argLength is not 2:
                return self.invalidArgCount()
            if not args.getCar().isNumber() or not args.getCdr().getCar().isNumber():
                return self.invalidArgType()
            sum = args.getCar().intVal + args.getCdr().getCar().intVal
            return IntLit(sum)
        elif name == "b-":                                               #Binary Subtraction
            if argLength is not 2:
                return self.invalidArgCount()
            if not args.getCar().isNumber() or not args.getCdr().getCar().isNumber():
                return self.invalidArgType()
            diff = args.getCar().intVal - args.getCdr().getCar().intVal
            return IntLit(diff)
        elif name == "b*":                                               #Binary Multiplication
            if argLength is not 2:
                return self.invalidArgCount()
            if not args.getCar().isNumber() or not args.getCdr().getCar().isNumber():
                return self.invalidArgType()
            return IntLit(args.getCar().intVal * args.getCdr().getCar().intVal)
        elif name == "b/":                                               #Binary Division
            if argLength is not 2:
                return self.invalidArgCount()
            if not args.getCar().isNumber() or not args.getCdr().getCar().isNumber():
                return self.invalidArgType()
            return IntLit(args[0].intVal / args.getCdr().getCar().intVal)
        elif name == "number?":                                          #Check if is a number
            if argLength is not 1:
               return self.invalidArgCount()
            if args.getCar().isNumber():
                return BoolLit.getInstance(True)
            return BoolLit.getInstance(False)
        elif name == "b=":
            if argLength is not 2:
               return self.invalidArgCount()
            if not args.getCar().isNumber() or not args.getCdr().getCar().isNumber():
                return self.invalidArgType()
            return BoolLit.getInstance(True) if args.getCar().intVal == args.getCdr().getCar().intVal else BoolLit.getInstance(False)
        elif name == "b<":
            if argLength is not 2:
               return self.invalidArgCount()
            if not args.getCar().isNumber() or not args.getCdr().getCar().isNumber():
                return self.invalidArgType()
            return BoolLit.getInstance(True) if args.getCar().intVal < args.getCdr().getCar().intVal else BoolLit.getInstance(False)
        elif name == "null?":
            if argLength is not 1:
               return self.invalidArgCount()
            if args.getCar().isNull():
                return BoolLit.getInstance(True)
            return BoolLit.getInstance(False)
        elif name == "procedure?":
            if argLength is not 1:
               return self.invalidArgCount()
            if args.getCar().isProcedure():
                return BoolLit.getInstance(True)
            return BoolLit.getInstance(False)
        elif name == "pair?":
            if argLength is not 1:
                return self.invalidArgCount()
            return BoolLit.getInstance(True) if args.getCar().isPair() else BoolLit.getInstance(False)
        elif name == "cons":
            if argLength is not 2:
                return self.invalidArgCount()
            return Cons(args.getCar(), args.getCdr().getCar())
        elif name == "car":
            if argLength is not 1:
                return self.invalidArgCount()
            if not args.getCar().isPair():
                return self.invalidArgType()
            return args.getCar().getCar()
        elif name == "cdr":
            if argLength is not 1:
                return self.invalidArgCount()
            if not args.getCar().isPair():
                return self.invalidArgType()
            return args.getCar().getCdr()
        elif name == "set-car!":
            if argLength is not 2:
                return self.invalidArgCount()
            if not args.getCar().isPair():
                return self.invalidArgType()
            args.getCar().setCar(args.getCdr().getCar())
            return Nil.getInstance()
        elif name == "set-cdr!":
            if argLength is not 2:
                return self.invalidArgCount()
            if not args.getCar().isPair():
                return self.invalidArgType()
            args.getCar().setCdr(args.getCdr().getCar())
            return Nil.getInstance()
        elif name == "eq?":
            if args.getCar().isSymbol() and args.getCdr().getCar().isSymbol():
                arg1_name = args.getCar().getName()
                arg2_name = args.getCdr().getCar().getName()
                return BoolLit.getInstance(arg1_name == arg2_name)
            return BoolLit.getInstance(args.getCar() == args.getCdr().getCar())
        
        #load
        elif name == "load":       
            if not args.getCar().isString(): 
                return self.invalidArgType()
            filename = args.getCar().strVal
            try:
                scanner = Scanner(open(filename))
                builder = TreeBuilder()
                parser = Parser(scanner, builder)

                root = parser.parseExp()
                while root != None:
                    root.eval(BuiltIn.env)
                    root = parser.parseExp()
            except IOError:
                self._error("could not find file " + filename)
            return Nil.getInstance()  # or Unspecific.getInstance()
        
        #read, calls parser and returns a parse tree
        elif name == "read":
            scanner = Scanner(sys.stdin)
            builder = TreeBuilder()
            parser = Parser(scanner, builder)
            #return parse tree here 
            if parser != None:
                return parser.parseExp()
            return Ident('End of Parse Tree')

        #write, calls pretty printer
        elif name == "write":
            if argLength is not 1:
                return self.invalidArgCount()
            args.getCar().print(-1)
            return Nil.getInstance()
            
        #display, calls pretty printer
        elif name == "display":
            if argLength is not 1:
                return self.invalidArgCount()
            StrLit.include_quote = 0
            args.getCar().print(-1)
            StrLit.include_quote = 1
            return Nil.getInstance()

        #eval, calls python eval function
        elif name == 'eval':
            if argLength is not 2:
                return self.invalidArgCount()
            if args.getCdr().getCar().isEnvironment():
                return args.getCar().eval(args.getCdr().getCar())
            return self.invalidArgType()

        #apply, calls python apply function
        elif name == "apply":
            if argLength is not 2:
                return self.invalidArgCount()
            return args.getCar().apply(args.getCdr().getCar())

        #interaction-environment, returns a pointer to interpreter's global environment
        elif name == "interaction-environment":
            return BuiltIn.env

        #newline without optional port argument
        elif name== "newline":
            sys.stdout.write('\n')
            sys.stdout.flush()
            return Nil.getInstance()

        return StrLit("Error: BuiltIn.apply not yet implemented for " + self.symbol)

    def eval(self, env):
        return Nil.getInstance()
    def invalidArgCount(self):
        self._error("Invalid argument count")
        return Nil.getInstance()
    def invalidArgType(self):
        self._error("Invalid argument type")
        return Nil.getInstance()