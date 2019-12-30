# StLit -- Parse tree node class for representing string literals

import sys
from Tree import Node
from Print import Printer

class StrLit(Node):
    include_quote = 1
    def __init__(self, s):
        self.strVal = s

    def print(self, n, p=False):
        if StrLit.include_quote == 1:
            Printer.printStrLit(n, self.strVal)
        else:
            sys.stdout.write(n*' ')
            sys.stdout.write(self.strVal)
    def isString(self):
        return True
    def eval(self, env):
        return self
if __name__ == "__main__":
    id = StrLit("foo")
    id.print(0)
