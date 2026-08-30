/**
 * Built-in example programs. These are loaded from the same source
 * files the CLI interpreter uses so what you see here matches what
 * `python interpreter.py examples/foo.py` would print.
 *
 * We use Vite's `?raw` suffix to import the .py files as strings.
 */
import hello from '../../../examples/hello.py?raw';
import factorial from '../../../examples/factorial.py?raw';
import fizzbuzz from '../../../examples/fizzbuzz.py?raw';
import sum from '../../../examples/sum.py?raw';
import primes from '../../../examples/primes.py?raw';
import lists from '../../../examples/lists.py?raw';
import membership from '../../../examples/membership.py?raw';
import breakContinue from '../../../examples/break_continue.py?raw';
import stringMethods from '../../../examples/string_methods.py?raw';

export interface Example {
  id: string;
  name: string;
  description: string;
  source: string;
}

export const EXAMPLES: Example[] = [
  { id: 'hello', name: 'Hello, world', description: 'A trivial starting program.', source: hello },
  { id: 'factorial', name: 'Factorial', description: 'Functions + recursion + loops.', source: factorial },
  { id: 'fizzbuzz', name: 'FizzBuzz', description: 'Modulo, conditionals, and printing.', source: fizzbuzz },
  { id: 'sum', name: 'Sum', description: 'Augmented assignment `+=`.', source: sum },
  { id: 'primes', name: 'Primes', description: 'Nested loops, `if/else`, `not`.', source: primes },
  { id: 'lists', name: 'Lists', description: 'List literals, indexing, iteration.', source: lists },
  { id: 'membership', name: 'Membership', description: '`in` and `not in` operators.', source: membership },
  { id: 'break_continue', name: 'break / continue', description: 'Early exit / skip in loops.', source: breakContinue },
  { id: 'string_methods', name: 'String methods', description: '`.upper()`, `.split()`, chaining.', source: stringMethods },
];
