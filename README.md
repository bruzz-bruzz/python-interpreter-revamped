# python-interpreter-revamped

A small, clean Python-subset interpreter implemented from scratch: **lexer → parser → AST → tree-walking interpreter + REPL**.

## Overview
This project implements a Python interpreter pipeline, covering all the core components needed to understand how Python works under the hood:

1. **Lexer** — converts source text into a stream of typed tokens (with proper INDENT/DEDENT handling).
2. **Parser** — recursive-descent / Pratt-style precedence-climbing parser that builds an AST.
3. **AST** — strongly-typed node hierarchy.
4. **Interpreter** — tree-walking evaluator with scopes, closures, and control flow.
5. **Builtins** — a small set of built-in functions and types.
6. **REPL** — interactive read-eval-print loop.

## Project Structure
```
revamped-interpreter/
├── interpreter.py          # CLI entry point: run a file or start the REPL
├── README.md
├── .gitignore
├── examples/               # Example programs the interpreter can run
│   ├── hello.py
│   ├── factorial.py
│   ├── fizzbuzz.py
│   ├── sum.py
│   ├── primes.py
│   ├── lists.py
│   ├── membership.py
│   ├── break_continue.py
│   └── string_methods.py
├── src/
│   ├── lexer/
│   │   ├── __init__.py
│   │   └── lexer.py        # Token, TokenType, Lexer
│   ├── parser/
│   │   ├── __init__.py
│   │   └── parser.py       # Recursive-descent parser
│   ├── ast/
│   │   ├── __init__.py
│   │   └── nodes.py        # AST node hierarchy
│   ├── interpreter/
│   │   ├── __init__.py
│   │   └── interpreter.py  # Tree-walking evaluator
│   └── builtins/
│       ├── __init__.py
│       ├── functions.py
│       └── types.py
└── tests/                  # unittest-based test suite (no extra deps)
    ├── __init__.py
    ├── test_lexer.py
    ├── test_parser.py
    └── test_interpreter.py
```

## Features
- **Lexical analysis** with proper ordering of multi-character operators (`==`, `<=`, `>=`, `!=`) and INDENT/DEDENT token emission
- **Pratt-style precedence parsing** for expressions with correct operator associativity
- **Control flow**: `if/elif/else`, `while`, `for x in iterable:`, `return`, `break`, `continue`
- **Functions** with closures, recursion, and parameter binding
- **Comparisons**: `==`, `!=`, `<`, `>`, `<=`, `>=`, `in`, `not in`, `is`
- **Logical operators**: `and`, `or` (short-circuit evaluation), `not` (unary)
- **Arithmetic**: `+`, `-`, `*`, `/` (true division), `//` (integer division), `%` (modulo)
- **Augmented assignment**: `+=`, `-=`, `*=`, `/=`, `//=`, `%=`
- **Lists**: `[1, 2, 3]` literals, indexing `xs[0]`, iteration, methods (`.append`, `.pop`)
- **String indexing**: `s[0]`, `s[-1]` (negative indices supported)
- **String methods**: `.upper()`, `.lower()`, `.strip()`, `.split()`, `.replace()`, `.startswith()`, `.endswith()`, `.find()`, `.count()`, plus method chaining
- **Built-ins**: `print`, `len`, `range`, `str`, `int`, `float`, `type`
- **Comments** starting with `#`
- **REPL** with `>>> ` prompt

## How to Run

### Run a Python file
```bash
python interpreter.py examples/factorial.py
```

### Start the REPL
```bash
python interpreter.py
```

### Run the test suite
```bash
python -m unittest discover -s tests -v
```

## Example Session
```text
$ python interpreter.py examples/factorial.py
factorial of 1 is 1
factorial of 2 is 2
factorial of 3 is 6
factorial of 4 is 24
factorial of 5 is 120
factorial of 6 is 720
factorial of 7 is 5040
```

## Limitations (intentional, for educational scope)
- No dicts, sets, or user-defined classes with attributes
- No modules, packages, or `import` resolution
- No `try/except`, `with`, comprehensions, lambdas, decorators
- No slicing `s[a:b]` (only single-index `s[i]`)

## Development
This project is being developed incrementally. Each commit adds a discrete chunk of functionality.
