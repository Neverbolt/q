# All credits are belong to Squishy

debug = False


class MachineState:
    def __init__(self):
        # stack to store operators
        self.stack = []
        # next action to allow one pass execution, parameters are pushed to temp
        #            method             temp storage
        # eg: (self.printNextStack, ["param1", 12, 15])
        # new actions should initialize themselves with:
        #     (`method`, [])
        self.nextActions = []
        # set of possible interpreter states
        self.states = {"action": 0, "type": 1, "value": 2}
        # current internal state/next expected value
        self.state = self.states["action"]
        # action resolving
        self.actions = {"q": self.push,
                        "qq": self.printNextStack}
        # type resolving
        self.types = {"+Number": "q",
                      "-Number": "qq",
                      "lChar": "qqq",
                      "uChar": "qqqq",
                      "sChar": "qqqqq",
                      "eval": "qqqqqqqqqq"}
        self.sChars = "  !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        self.currentType = self.types["eval"]

    # evaluate the current token in respect to state and action stack
    def eval(self, token):
        if self.state is self.states["action"]:
            # if action can be resolved do setup and change to parameter mode
            if token in self.actions:
                self.actions[token](init=True)
                if debug:
                    print("EXECUTING: " + str(self.actions[token]))
            else:
                print("ACTION ERROR: " + str(token))

        elif self.state is self.states["type"]:
            if token is self.types["eval"]:
                self.state = self.actions["action"]
            else:
                if token in self.types.values():
                    self.currentType = token
                    if debug:
                        print("TYPE: " + str(list(self.types.keys())[list(self.types.values()).index(self.currentType)]))
                else:
                    print("TYPE ERROR: " + str(token))

                self.state = self.states["value"]

        elif self.state is self.states["value"]:
            if self.currentType == self.types["+Number"]:
                self.pushParam(len(token))
            elif self.currentType == self.types["-Number"]:
                self.pushParam(-len(token))
            elif self.currentType == self.types["lChar"]:
                self.pushParam(chr(97 + (len(token) - 1) % 26))
            elif self.currentType == self.types["uChar"]:
                self.pushParam(chr(65 + (len(token) - 1) % 26))
            elif self.currentType == self.types["sChar"]:
                self.pushParam(self.sChars[len(token) % len(self.sChars)])
            else:
                print("INTERNAL ACTION ERROR: " + str(self.currentType) + " : " + str(list(self.types.keys())[list(self.types.values()).index(self.currentType)]))

            if debug:
                print(self.currentAction())
            self.currentAction()()

        else:
            print("INTERNAL STATE ERROR: " + str(self.state))

    # helper method for eval
    def pushParam(self, param):
        self.nextActions[-1][1].append(param)
        if debug:
            print("PUSHED PARAM: " + str(param))

    # helper method to get currently evaluating method
    def currentAction(self):
        return self.nextActions[-1][0]

    # helper method to get currently evaluating parameters
    def currentParameters(self):
        return self.nextActions[-1][1]

    # prints the topmost element from stack
    def printNextStack(self, init=False):
        print(self.stack.pop())

    # put value onto stack
    # is always prepended by preparePush
    def push(self, init=False):
        if init is True:
            self.nextActions.append((self.push, []))
            self.state = self.states["type"]
        else:
            self.stack.append(self.currentParameters()[0])
            self.nextActions.pop()
            self.state = self.states["action"]


# value delimiter
#  'q'    '\t'

# q
# +0123456789...
# qq
# -0123456789...
# qqq
# abcdefghijklmnopqrstuvwxyz
# qqqq
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# qqqqq
#  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
# qqqqqqqqqq
# `eval`

# hello
# ' '
# world!
# \print(12)
code = (" q qqqqq qq"
        " q qqq qqqq q qqq qqqqqqqqqqqq q qqq qqqqqqqqqqqqqqqqqq q qqq qqqqqqqqqqqqqqq q qqqq qqqqqqqqqqqqqqqqqqqqqqq"
        " q qqqqq q"
        " q qqq qqqqqqqqqqqqqqq q qqq qqqqqqqqqqqq q qqq qqqqqqqqqqqq q qqq qqqqq q qqqq qqqqqqqq"
        " qq qq qq qq qq qq qq qq qq qq qq qq")

program = code.split()
machine = MachineState()

for token in program:
    machine.eval(token)
