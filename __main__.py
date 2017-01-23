# Almost all credits are belong to Squishy
# Some are belong to Goebel and Anders

debug = False
stackDebug = False


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
        self.states = {"error": -1, "action": 0, "type": 1, "value": 2, "flowcontrol": 3}
        # current internal state/next expected value
        self.state = self.states["type"]
        # action resolving
        self.actions = {"q" * 1: self.pop,
                        "q" * 2: self.printNextStackValue,
                        "q" * 3: self.add,
                        "q" * 4: self.subtract,
                        "q" * 5: self.multiply,
                        "q" * 6: self.divide,
                        "q" * 7: self.duplicate,
                        "q" * 8: self.swap,
                        "q" * 9: self.over,
                        "q" * 10: self.beginif,
                        "q" * 11: self.endif,
                        "q" * 12: self.beginelse,
                        "q" * 13: self.endelse,
                        """q" * 14: self.beginwhile,
                        "q" * 15: self.endwhile""": ""}
        # type resolving
        self.types = {"eval": "q",
                      "+Number": "qq",
                      "-Number": "qqq",
                      "lChar": "qqqq",
                      "uChar": "qqqqq",
                      "sChar": "qqqqqq",
                      "Number": "NUMBER"}
        self.sChars = " !\n\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        self.currentType = self.types["eval"]

    # evaluate the current token in respect to state and action stack
    def eval(self, token, overwriteState=None):
        if stackDebug:
            print(self.stack)
        # allow eval to be called from flowcontrol methods
        if overwriteState is None:
            localstate = self.state
        else:
            localstate = overwriteState

        if localstate is self.states["action"]:
            # if action can be resolved do setup and change to parameter mode
            if token in self.actions:
                localstate = self.actions[token]()
                if debug:
                    print("EXECUTING: " + str(self.actions[token].__name__) + " RETURNED " + str(localstate))
                if localstate is None:
                    localstate = self.states["type"]
            else:
                print("ACTION ERROR: " + str(token))

        elif localstate is self.states["type"]:
            if token is self.types["eval"]:
                localstate = self.states["action"]

                if debug:
                    print("TYPE: eval")

            else:
                if token in self.types.values():
                    self.currentType = token
                else:
                    print("TYPE ERROR: " + str(token))

                localstate = self.states["value"]

                if debug:
                    print("TYPE: " + str(self.getKeyFromValue(self.types, self.currentType)))

        elif localstate is self.states["value"]:
            if self.currentType == self.types["+Number"]:
                self.push(len(token), type=self.types["Number"])

            elif self.currentType == self.types["-Number"]:
                self.push(-len(token), type=self.types["Number"])

            elif self.currentType == self.types["lChar"]:
                self.push(chr(97 + (len(token) - 1) % 26))

            elif self.currentType == self.types["uChar"]:
                self.push(chr(65 + (len(token) - 1) % 26))

            elif self.currentType == self.types["sChar"]:
                self.push(self.sChars[(len(token) - 1) % len(self.sChars)])

            else:
                print("INTERNAL TYPE VALUE ERROR: " + str(self.currentType) + " : " + str(self.getKeyFromValue(self.types, self.currentType)))
                return

            if debug:
                print("VALUE: " + str(self.stack[-1]))

            localstate = self.states["type"]

        elif localstate is self.states["flowcontrol"]:
            self.currentAction()(token, self.currentParameters())

        else:
            print("INTERNAL STATE ERROR: " + str(localstate))
            return

        if overwriteState is None:
            self.state = localstate
        else:
            return localstate

    def createAction(self, action):
        self.nextActions.append((action, []))

    # helper method to get currently evaluating method
    def currentAction(self):
        return self.nextActions[-1][0]

    # helper method to get currently evaluating parameters
    def currentParameters(self):
        return self.nextActions[-1][1]

    def getKeyFromValue(self, dict, val):
        return list(dict.keys())[list(dict.values()).index(val)]

    def getCodeFromAction(self, action):
        self.getKeyFromValue(self.actions, action)

    # helper method for eval and actions
    def push(self, param, type=None):
        if type is None:
            self.stack.append((self.currentType, param))
        else:
            self.stack.append((type, param))

    # pops off the top stack element and returns it
    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()

        else:
            print("SYNTAX ERROR: no value left on stack")
            self.state = self.states["error"]

    # returns an element from stack without poping it
    def peek(self, back=0):
        if len(self.stack) - back > 0:
            return self.stack[-(back + 1)]

        else:
            print("SYNTAX ERROR: no value left on stack")
            self.state = self.states["error"]

    # prints the topmost element from stack
    def printNextStackValue(self):
        print(self.pop()[1], end="\n", flush=True)

    def add(self):
        val1 = self.pop()
        val2 = self.pop()
        if val1[0] == self.types["Number"] and val2[0] == self.types["Number"]:
            self.push(val1[1] + val2[1], type=self.types["Number"])
        elif val1[0] == self.types["lChar"] and val2[0] == self.types["Number"]:
            self.push(chr(97 + (ord(val1[1]) + val2[1] - 97) % 26), type=self.types["lChar"])
        elif val1[0] == self.types["uChar"] and val2[0] == self.types["Number"]:
            self.push(chr(65 + (ord(val1[1]) + val2[1] - 65) % 26), type=self.types["uChar"])
        elif val1[0] == self.types["sChar"] and val2[0] == self.types["Number"]:
            self.push(self.sChars[(self.sChars.index(val1[1]) + val2[1] - 1) % len(self.sChars)], type=self.types["sChar"])
        else:
            print("SYNTAX ERROR: addition of " + val1[0] + " and " + val2[0] + " not allowed")

    def subtract(self):
        val1 = self.pop()
        val2 = self.pop()
        if val1[0] == self.types["Number"] and val2[0] == self.types["Number"]:
            self.push(val1[1] - val2[1], type=self.types["Number"])
        elif val1[0] == self.types["lChar"] and val2[0] == self.types["Number"]:
            self.push(chr(97 + (ord(val1[1]) - val2[1] - 97) % 26), type=self.types["lChar"])
        elif val1[0] == self.types["uChar"] and val2[0] == self.types["Number"]:
            self.push(chr(65 + (ord(val1[1]) - val2[1] - 65) % 26), type=self.types["uChar"])
        elif val1[0] == self.types["sChar"] and val2[0] == self.types["Number"]:
            self.push(self.sChars[(self.sChars.index(val1[1]) - val2[1] - 1) % len(self.sChars)], type=self.types["sChar"])
        else:
            print("SYNTAX ERROR: subtraction of " + val1[0] + " and " + val2[0] + " not allowed")

    def multiply(self):
        val1 = self.pop()
        val2 = self.pop()
        if val1[0] == self.types["Number"] and val2[0] == self.types["Number"]:
            self.push(val1[1] * val2[1], type=self.types["Number"])
        else:
            print("SYNTAX ERROR: multiplication of " + val1[0] + " and " + val2[0] + " not allowed")

    def divide(self):
        val1 = self.pop()
        val2 = self.pop()
        if val1[0] == self.types["Number"] and val2[0] == self.types["Number"]:
            self.push(val1[1] / val2[1], type=self.types["Number"])
        else:
            print("SYNTAX ERROR: division of " + val1[0] + " and " + val2[0] + " not allowed")

    def duplicate(self):
        self.push(self.stack[-1][1], type=self.stack[-1][0])

    def xDuplicate(self):
        index = self.pop()
        if index[0] == self.types["Number"]:
            self.push(self.stack[-index[1]][1], type=self.stack[-index[1]][0])
        else:
            print("SYNTAX ERROR: index for xDuplicate has to be number")

    def xPush(self):
        index = self.pop()
        if index[0] == self.types["Number"]:
            if 0 < index[1] < len(self.stack):
                self.push(self.stack[-index[1]][1], type=self.stack[-index[1]][0])
            else:
                print("SYNTAX ERROR: index of xPush is not in range")
        else:
            print("SYNTAX ERROR: index for xPush has to be number")

    def swap(self):
        val1 = self.pop()
        val2 = self.pop()
        self.push(val1[1], type=val1[0])
        self.push(val2[1], type=val2[0])

    def over(self):
        val1 = self.pop()
        val2 = self.pop()
        val3 = self.pop()
        self.push(val1[1], type=val1[0])
        self.push(val2[1], type=val2[0])
        self.push(val3[1], type=val3[0])

    def beginif(self):
        global debug
        global stackDebug
        debug = False
        stackDebug = False
        self.createAction(self.ifaction)
        comparison = self.peek()
        currentVal = self.peek(back=1)
        evaluating = False

        if currentVal[0] == self.types["Number"] and comparison[0] == self.types["sChar"]:
            if comparison[1] == ">":
                evaluating = currentVal[1] > 0
            elif comparison[1] == "=":
                evaluating = currentVal[1] is 0
            elif comparison[1] == "<":
                evaluating = currentVal[1] < 0

        self.currentParameters().append(evaluating)
        self.currentParameters().append(self.states["type"])
        return self.states["flowcontrol"]

    def endif(self):
        if self.currentAction() == self.ifaction:
            self.nextActions.pop()
            self.state = self.states["type"]
        else:
            print("SYNTAX ERROR: endif without if")
            self.state = self.states["error"]

    def beginelse(self):
        if self.currentAction() == self.ifaction:
            # this is intended behavior to make some magic possible
            self.currentParameters()[0] = not self.currentParameters()[0]
        else:
            print("SYNTAX ERROR: else without if")
            self.state = self.states["error"]

    def endelse(self):
        if self.currentAction() == self.ifaction:
            self.nextActions.pop()
            self.state = self.states["type"]
        else:
            print("SYNTAX ERROR: endif without if")
            self.state = self.states["error"]

    # parameters = [willEval, state]
    def ifaction(self, token, parameters):
        if parameters[1] == self.states["action"]:
            if token == self.getCodeFromAction(self.endif):
                self.endif()

            if token == self.getCodeFromAction(self.endelse):
                self.endelse()

            elif token == self.getCodeFromAction(self.beginelse):
                self.beginelse()

            elif parameters[0] is True:
                parameters[1] = self.eval(token, overwriteState=parameters[1])

        elif parameters[0] is True:
            parameters[1] = self.eval(token, overwriteState=parameters[1])


# value delimiter
#  'q'    '\t'

# q
# `eval`
# qq
# +0123456789...
# qqq
# -0123456789...
# qqqq
# abcdefghijklmnopqrstuvwxyz
# qqqqq
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# qqqqqq
#  !\n"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

# Print "Hello World!"
if __name__ == '__main__':
    code = (" qqqqqq qqq qqqqqq qq "
            " qqqq qqqq qqqq qqqqqqqqqqqq qqqq qqqqqqqqqqqqqqqqqq qqqq qqqqqqqqqqqqqqq qqqqq qqqqqqqqqqqqqqqqqqqqqqq "
            " qqqqqq q "
            " qqqq qqqqqqqqqqqqqqq qqqq qqqqqqqqqqqq qqqq qqqqqqqqqqqq qqqq qqqqq qqqqq qqqqqqqq "
            " q qq q qq q qq q qq q qq q qq q qq q qq q qq q qq q qq q qq q qq"
            " qq qqqqq qqq qqq q qqq qqqqqq qqqqqqqqqqqqqqqqqqqqqq q qqqqqqqqqq q qqqqqqqq q qq q qqqqqqqqqqqq qqqq q q qq q qqqqqqqqqqqqq qq qqqqq q qq")
    """code = " q q q q q q qqq q q q q qq qqqq q q q"""  # Sashas great q code that does a lot

    program = code.split()
    machine = MachineState()

    for token in program:
        machine.eval(token)
