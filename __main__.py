#!/usr/bin/python3
# Almost all credits are belong to Squishy
# Some are belong to Goebel and Anders
import sys
import re
import inspect
from machine import MachineState

sys.setrecursionlimit(10000)

# Print "Hello World!"
if __name__ == '__main__':
    """code = (" q q "
            " qqqqqqqq qqq qqqqqqqq qq "
            " qqqqqq qqqq qqqqqq qqqqqqqqqqqq qqqqqq qqqqqqqqqqqqqqqqqq qqqqqq qqqqqqqqqqqqqqq qqqqqqq qqqqqqqqqqqqqqqqqqqqqqq "
            " qqqqqqqq q "
            " qqqqqq qqqqqqqqqqqqqqq qqqqqq qqqqqqqqqqqq qqqqqq qqqqqqqqqqqq qqqqqq qqqqq qqqqqqq qqqqqqqq "
            " qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q "
            " qq q qqq q"
            )"""
    code = ("""
                qqqq qqqqq 5 qqqq qq 2
                q q method1begin
                    qqqq q 1 qqqq qqqqq qqq q -
                qq q method1end qqq qqq methode1execWHILE
                qqqq qqq qqq q print
            """)

    program = re.sub(r"[^q ]", "", code).split()
    machine = MachineState(debug=True)

    for token in program:
        machine.eval(token)
