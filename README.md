# -Functional-Language-Interpreter

This is an interpreter for a functional language (L) created using my own lexer.

A program is a list of atoms, where an atom can be:
    -a natural number
    -an empty list ()
    -a lambda expression
    -a function invocation
    -another list of atoms
    
The output is a number, or a list composed only of:
    -numbers
    -other lists (composed only of numbers or other lists)


Natural Numbers
  In L, we will use only natural numbers, without a specific upper limit; a number is any sequence of digits (from 0 to 9).

Empty List
  The empty list is a list without elements, and it is represented by the string ().

Lambda Expressions
  A lambda expression represents the definition of a 'custom' function. The syntax for defining a lambda expression is as follows:
              lambda {id}: {expr}

Where:
  -"lambda" is a specific keyword
  -{id} is an id, formed only by characters [a-z] or [A-Z]
  -{expr} is a result list, which may contain, besides regular atoms, the keyword {id}
To evaluate a lambda expression, replace all occurrences of the id inside the expression with the value it is called with.

EX:
    (lambda x: (x x) (1 2)) = ((1 2) (1 2))



Function Invocations
  A list in the form of (f x) can be evaluated as long as f is:
    -a lambda expression
    -a function from the standard library
    
  For simplicity, we will limit ourselves to 2 standard functions:
    +, which, when applied to a list, recursively sums the elements of the list and returns an atom
    ++, which, when applied to a list, concatenates all component lists

EX:
  (+ (1 2 3)) = 6;
  (+ (1 (2 3) 4)) = 10;
  (+ (())) = 0;
  
  (++ (1 (2 3))) = (1 2 3);
  (++ ((1 2) (3 4) 5)) = (1 2 3 4 5);
  (++ ((1 2) () 3)) = (1 2 3);
  (++ ((1 2 ()) (3 4))) = (1 2 () 3 4);


Whitespaces
  Within the program, we can use as many free spaces (and newline characters) for indentation without changing the program's semantics. The only spaces that matter semantically are those that separate numbers/identifiers from each other.

EX:
  (1 2 3)
  is different from
  (123)
  but is not different from
  ( 1 2 3 )
  or
  (
    1
    2
    3
  )
