"""Entry point for the revamped Python interpreter.

Usage:
    python interpreter.py <source_file.py>     # run a source file
    python interpreter.py                       # start a REPL
"""

import sys
import traceback
from pathlib import Path

# Make sure `src` package is importable when running this script directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.interpreter.interpreter import Interpreter
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


BANNER = "Revamped Python Interpreter 0.1.0 (type 'exit()' or Ctrl-D to quit)"


def run_source(source: str) -> None:
    """Lex, parse, and interpret a source string."""
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    Interpreter().interpret(program)


def run_file(path: str) -> int:
    """Load and interpret a Python source file."""
    try:
        source = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"interpreter: file not found: {path}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"interpreter: cannot read {path!r}: {exc}", file=sys.stderr)
        return 1
    try:
        run_source(source)
    except (SyntaxError, NameError, RuntimeError) as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


def repl() -> int:
    """Start a simple read-eval-print loop."""
    print(BANNER)
    while True:
        try:
            line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not line.strip():
            continue
        if line.strip() in ("exit()", "quit()"):
            return 0
        try:
            run_source(line)
        except (SyntaxError, NameError, RuntimeError) as exc:
            print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        except Exception:  # pragma: no cover - last-resort handler
            traceback.print_exc()


def main(argv: list) -> int:
    if len(argv) == 1:
        return repl()
    if len(argv) == 2:
        return run_file(argv[1])
    print("Usage: python interpreter.py [source_file.py]", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
