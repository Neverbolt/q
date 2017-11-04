# KuhTap

A stack based, reverse polish, turing complete programming language that consists of the letter `q` and the control character `\t`.

This is powerful, use at own risk!

# Grammar

For a grammar specification see the file `formal_definition.bnf`

# Actions
q comes with a set of built-in actions that are called with positive numbers. All string actions are numeric zero terminated unless noted otherwise.

- Pop (`q`):
  - Pop the stack value
- Print (`qq`):
  - Prints all characters until it encounters a numeric zero
- Add (`qqq`):
  - Add top two stack values and push the result to stack
- Subtract (`qqqq`):
  - Subtract top two stack values and push the result to stack
- Multiply (`qqqqq`):
  - Multiply top two stack values and push the result to stack
- Divide (`qqqqqq`):
  - Divide top two stack values and push the result to stack
- Duplicate (`qqqqqqq`):
  - Duplicate the top stack value and push it to stack
- Swap (`qqqqqqqq`):
  - Swaps the top two stack value
- Over (`qqqqqqqqq`):
  - Takes the second to last stack value and duplicates it to front
- xDuplicate (`qqqqqqqqqq`):
  - Takes the top stack value and if it is a number it replaces it with the `value` to last element
- xPush (`qqqqqqqqqqq`):
  - Takes the top stack value and if it is a number takes the `value` to last element, replacing it with second to last element
