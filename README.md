# KuhTap

A stack based, reverse polish, turing complete programming language that consists of the letter `q`and the control character `\t`.

This is powerful, use at own risk!

# Types

## OLD:
- Eval:                `q`
- Positive number:     `qq`
- Negative number:     `qqq`
- Lowercase character: `qqqq`
- Uppercase character: `qqqqq`
- Special character:   `qqqqqq`
- Begin Code Block:    `qqqqqqq`
- End Code Block:      `qqqqqqqq`

## NEW:
- Begin Code Block:    `q`
- End Code Block:      `qq`
- Eval:                `qqq`
- Positive number:     `qqqq`
- Negative number:     `qqqqq`
- Lowercase character: `qqqqqq`
- Uppercase character: `qqqqqqq`
- Special character:   `qqqqqqqq`

# Codeblock

The parameter after an end block is the methodID which starts counting at 20. That means that if your codeblock ends with `qqqqqqqq q` it can later be called back with the ID `21` (`qqqqqqqqqqqqqqqqqqqqqqqqq`).
Eg:
```
qqqqqqq q qqq qq q q qqqqqqqq q this is the codeblock
qqqq qqqqqqqqqqqqqqqqqqqqqqqqq qqq q this sets up the code and calls the block
```

# Character usage

Lower and upper case characters repeat from a-z or A-Z respectively, special characters repeat the following sequence where the first character is a space:
```
 !\n"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
```

# Actions

- Pop (`q`):
  - Pop the stack value
- Print (`qq`):
  - Pops the top stack value and prints it
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
