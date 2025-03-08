# Functional Language Interpreter

This repository contains an interpreter for a custom functional language (**L**) built using a custom lexer. The interpreter evaluates expressions consisting of numbers, lists, lambda functions, and function invocations.

## Features

- **Natural numbers** as the primary numerical type.
- **Empty lists** represented as `()`.
- **Lambda expressions** for defining and using custom functions.
- **Function invocations** supporting both standard functions and user-defined lambdas.
- **Standard functions**:
  - `+` (sum): Recursively sums elements in a list.
  - `++` (concatenation): Merges nested lists into a single list.

## Syntax and Evaluation

### **Atoms and Lists**
- An expression consists of **atoms**, which can be:
  - A **natural number** (e.g., `42`).
  - An **empty list** (`()`).
  - A **lambda expression** (e.g., `lambda x: (x x)`).
  - A **function invocation** (`(f x)`).
  - Another **list of atoms**.

The output of the interpreter can be:
- A number.
- A list containing only numbers or other lists.

### **Lambda Expressions**
A **lambda expression** defines a function:
```plaintext
lambda {id}: {expr}
```
- `{id}`: A variable name (letters `[a-zA-Z]`).
- `{expr}`: The expression body where `{id}` can appear.

Example:
```plaintext
(lambda x: (x x) (1 2)) → ((1 2) (1 2))
```

### **Function Invocations**
Expressions of the form `(f x)` are valid if `f` is:
1. A **lambda expression**.
2. A function from the standard library.

#### Standard Functions
| Function | Description |
|----------|------------|
| `+`      | Recursively sums all numbers in a list. |
| `++`     | Concatenates nested lists into a single list. |

Examples:
```plaintext
(+ (1 2 3)) → 6
(+ (1 (2 3) 4)) → 10
(+ (())) → 0

(++ (1 (2 3))) → (1 2 3)
(++ ((1 2) (3 4) 5)) → (1 2 3 4 5)
(++ ((1 2) () 3)) → (1 2 3)
```

### **Whitespace Handling**
- Whitespaces are ignored, except for separating numbers/identifiers.
- `(1 2 3)` is **not** the same as `(123)`, but:
  ```plaintext
  ( 1 2 3 )
  ```
  is equivalent to:
  ```plaintext
  (
    1
    2
    3
  )
  ```

## Project Structure

```
traianis--functional-language-interpreter/
│── README.md
│── Interpreter/
│   ├── check.sh
│   ├── bonus_tests/        # Sample test cases
│   │   ├── *.l            # Input test cases
│   │   └── ref/           # Expected outputs
│   ├── src/               # Interpreter source code
│   │   ├── main.py        # Main interpreter script
│   │   ├── Lexer.py       # Lexer implementation
│   │   ├── DFA.py         # Deterministic Finite Automaton
│   │   ├── NFA.py         # Non-deterministic Finite Automaton
│   │   ├── Regex.py       # Regex parsing utilities
│   ├── test/              # Unit tests
│   │   ├── test_hw_1.py
│   │   ├── test_hw_2.py
│   │   └── test_hw_3.py
```


## Example Usage
Running:
```plaintext
(lambda x: (+ (x x)) (1 2 3))
```
Produces:
```plaintext
12
```
