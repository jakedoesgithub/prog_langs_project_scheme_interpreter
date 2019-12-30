# Scheme4101 -- The main program of the Scheme interpreter

import sys
from Parse import *
from Tokens import TokenType
from Tree import StrLit
from Tree import Ident
from Tree import Cons
from Tree import TreeBuilder
from Tree import BuiltIn
from Tree import Environment
from Tree import Closure
from Special import Special
from Util import Util

if __name__ == "__main__":
    # Initialization file with Scheme definitions of built-in functions
    ini_file = "ini.scm"

    prompt = "> "

    # Create scanner that reads from standard input
    scanner = Scanner(sys.stdin)

    util = Util()
    Cons.setUtil(util)
    BuiltIn.setUtil(util)
    Closure.setUtil(util)
    Special.setUtil(util)

    if (len(sys.argv) > 2 or
        (len(sys.argv) == 2 and sys.argv[1] != "-d")):
        sys.stderr.write("Usage: python3 SPP.py [-d]\n")
        sys.stderr.flush()
        sys.exit(2)

    # If command line option -d is provided, debug the scanner.
    if len(sys.argv) == 2 and sys.argv[1] == "-d":
        tok = scanner.getNextToken()
        while tok != None:
            tt = tok.getType()

            sys.stdout.write(str(tt))
            if tt == TokenType.INT:
                sys.stdout.write(", intVal = " + str(tok.getIntVal()) + "\n")
            elif tt == TokenType.STR:
                sys.stdout.write(", strVal = " + tok.getStrVal() + "\n")
            elif tt == TokenType.IDENT:
                sys.stdout.write(", name = " + tok.getName() + "\n")
            else:
                sys.stdout.write("\n")
            sys.stdout.flush()

            tok = scanner.getNextToken()
    else:
        # Create parser
        builder = TreeBuilder()
        parser = Parser(scanner, builder)

        env = Environment()
        # Environment.populateEnv(env, ini_file)
        #env = Environment(env)
        BuiltIn.setEnv(env)
        Environment.populateEnvironment(env, ini_file)
        # Read-eval-print loop

        sys.stdout.write(prompt)
        sys.stdout.flush()
        root = parser.parseExp()
        while root != None:
            root.eval(env).print(0)
            sys.stdout.write(prompt)
            sys.stdout.flush()
            root = parser.parseExp()
