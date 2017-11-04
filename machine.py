class MachineState:
    def __init__(self, debug=False):
        self.debugging = debug

        self.stackdepth = 1
        self.blockTypeCounter = 1
        # stack to store operators
        self.stack = []
        # set of possible interpreter states
        self.states = {"error": -1, "action": 0, "type": 1, "value": 2, "block": 3}
        # current internal state/next expected value
        self.state = self.states["type"]
        # custom code blocks defined as actions
        self.codeblocks = {}
        self.declarationstack = []
        # action resolving
        self.actions = {1: self.pop,
                        2: self.makeString,
                        3: self.printNextStackValue,
                        4: self.add,
                        5: self.subtract,
                        6: self.multiply,
                        7: self.divide,
                        8: self.duplicate,
                        9: self.swap,
                        10: self.over}
        # type resolving
        self.types = {"error": -1,
                      "blockbegin": 1,
                      "blockend": 2,
                      "eval": 3,
                      "+Number": 4,
                      "-Number": 5,
                      "lChar": 6,
                      "uChar": 7,
                      "sChar": 8,
                      "Number": "NUMBER"}
        self.sChars = " !\n\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        self.currentType = self.types["eval"]

    # prints a debug message when debug is enabled
    def debug(self, msg):
        if self.debugging:
            print(msg)

    # evaluate the current token in respect to state and action stack
    def eval(self, token):
        if isinstance(token, str):
            token = len(token)

        if self.state is self.states["block"]:
            if self.blockTypeCounter % 2 == 0:
                tempState = self.parseType(token)

                if tempState != self.states["block"]:
                    self.storeBlock(token)

            elif self.currentType == self.types["blockbegin"]:
                self.debug("block " + str(token) + " has begone")
                self.declarationstack.append(-token)
                self.codeblocks[self.declarationstack[-1]] = []
                self.currentType = self.types["eval"]

            elif self.currentType == self.types["blockend"]:
                if self.declarationstack[-1] == -token:
                    self.debug("block " + str(token) + " has been gone")
                    self.push(self.declarationstack.pop(), type=self.types["Number"])
                    self.state = self.states["type"]
                else:
                    print("BLOCK ERROR: CLOSING BLOCK " + str(-token) + " IS NOT THE MOST RECENTLY OPENED ONE")

            else:
                self.storeBlock(token)

            self.blockTypeCounter += 1

        elif self.state is self.states["action"]:
            # change token action to modifier (eg if, while, etc) and last value to called code block
            # if action can be resolved do setup and change to parameter mode
            if self.peek()[0] is self.types["Number"]:
                if self.peek()[1] > 0:
                    self.state = self.actions[self.pop()[1]]()
                elif self.peek()[1] < 0:
                    blockID = self.pop()[1]

                    if blockID not in self.codeblocks:
                        print("BLOCK " + str(blockID) + " HAS NOT BEEN FOUND IN THE BLOCKSTORE")
                    else:
                        if self.stackdepth < 9990:
                            if token == 2 and self.peek()[0] != self.types["Number"]:
                                print("SYNTAX ERROR: if action has not reached number on condition but rather " + self.peek())
                                self.state = self.states["type"]
                                return

                            if token == 2 and self.pop()[1] == 1:
                                self.debug("IF CONDITION FAILED")
                                self.state = self.states["type"]
                                return

                            self.stackdepth += 1

                            self.debug("EXECUTING BLOCK " + str(-blockID))

                            if token == 3:
                                while True:
                                    if self.peek()[0] != self.types["Number"]:
                                        print("SYNTAX ERROR: while action has not reached number on condition but rather " + self.peek())
                                        self.state = self.states["type"]
                                        break

                                    if self.peek()[1] != 1:
                                        self.state = self.states["type"]
                                        break

                                    self.state = self.states["type"]

                                    self.debug("WHILE EXECUTED")

                                    for action in self.codeblocks[blockID]:
                                            self.eval(action)
                            else:
                                self.state = self.states["type"]

                                for action in self.codeblocks[blockID]:
                                    self.eval(action)

                            self.debug("BLOCK " + str(-blockID) + " FINISHED")

                            self.stackdepth -= 1
                else:
                    print("NULL METHOD WTF")

                if self.state is None:
                    self.state = self.states["type"]

        elif self.state is self.states["type"]:
            self.state = self.parseType(token)

            self.debug("TYPE FOR " + str(token) + " : " + str(self.getKeyFromValue(self.types, self.currentType)))

        elif self.state is self.states["value"]:
            self.push(*self.parseValue(token, self.currentType))

            self.debug("VALUE: " + str(self.stack[-1]))

            self.state = self.states["type"]

        else:
            print("INTERNAL STATE ERROR: " + str(self.state))

    def storeBlock(self, token):
        self.codeblocks[self.declarationstack[-1]].append(token)

    # parse the given value in relation to the current type information
    def parseValue(self, token, currentType):
        if currentType == self.types["+Number"]:
            return (token - 1, self.types["Number"])

        elif currentType == self.types["-Number"]:
            return (-(token - 1), self.types["Number"])

        elif currentType == self.types["lChar"]:
            return (chr(97 + (token - 1) % 26), self.types["lChar"])

        elif currentType == self.types["uChar"]:
            return (chr(65 + (token - 1) % 26), self.types["uChar"])

        elif currentType == self.types["sChar"]:
            return (self.sChars[(token - 1) % len(self.sChars)], self.types["sChar"])

        print("INTERNAL TYPE VALUE ERROR: " + str(self.currentType) + " : " + str(self.getKeyFromValue(self.types, self.currentType)))

        self.state = self.states["error"]
        return (0, self.types["error"])

    def parseType(self, token):
        if token == self.types["blockbegin"] or token == self.types["blockend"]:
            self.currentType = token
            return self.states["block"]

        if token is self.types["eval"]:
            return self.states["action"]

        if token in self.types.values():
            self.currentType = token
            return self.states["value"]

        print("TYPE NOT FOUND ERROR: " + str(token))
        return self.states["error"]

    def getKeyFromValue(self, dict, val):
        return list(dict.keys())[list(dict.values()).index(val)]

    # helper method for eval
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
            print("SYNTAX ERROR: no value left on stack to pop")
            self.state = self.states["error"]

    # returns an element from stack without poping it
    def peek(self, back=0):
        if len(self.stack) - back > 0:
            return self.stack[-(back + 1)]

        else:
            print("SYNTAX ERROR: no value left on stack to peek on")
            self.state = self.states["error"]

    def makeString(self):
        length = self.pop()

        if length[0] != self.types["Number"]:
            print("SYNTAX ERROR: need number as first argument of makeString")
            return

        length = length[1]
        if length < 0:
            print("SYNTAX ERROR: need positive number as first argument of makeString")
            return

        string = ""
        for n in range(length):
            char = self.pop()

            if char[0] not in [self.types["lChar"], self.types["uChar"], self.types["sChar"], self.types["Number"], self.types["String"]]:
                print("SYNTAX ERROR: tried to convert illegal type " + char[0] + " to string")
                return

            string += char[1]

        self.push(string, self.types["String"])

    # prints the topmost element from stack
    def printNextStackValue(self):
        print(self.pop()[1], flush=True, end="\n")

    def add(self):
        val2 = self.pop()
        val1 = self.pop()
        if val1[0] == self.types["Number"] and val2[0] == self.types["Number"]:
            self.push(val1[1] + val2[1], type=self.types["Number"])
        elif val1[0] == self.types["lChar"] and val2[0] == self.types["Number"]:
            self.push(chr(97 + (ord(val1[1]) + val2[1] - 97) % 26), type=self.types["lChar"])
        elif val1[0] == self.types["uChar"] and val2[0] == self.types["Number"]:
            self.push(chr(65 + (ord(val1[1]) + val2[1] - 65) % 26), type=self.types["uChar"])
        elif val1[0] == self.types["sChar"] and val2[0] == self.types["Number"]:
            self.push(self.sChars[(self.sChars.index(val1[1]) + val2[1] - 1) % len(self.sChars)], type=self.types["sChar"])
        elif val1[0] == self.types["STRING"] and val2[0] in [self.types["lChar"], self.types["uChar"], self.types["sChar"], self.types["Number"], self.types["String"]]:
            self.push(val1[1] + val2[1], self.types["String"])
        else:
            print("SYNTAX ERROR: addition of " + val1[0] + " and " + val2[0] + " not allowed")

    def subtract(self):
        val2 = self.pop()
        val1 = self.pop()
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
        elif val1[0] in [self.types["lChar"], self.types["uChar"], self.types["sChar"], self.types["String"]] and val2[0] == self.types["Number"]:
            self.push(("" + val1[1]) * val2[1], self.types["String"])
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
