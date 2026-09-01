/**
 * Headless smoke-test runner.
 *
 * Reads each bundled example from src/lib/examples.ts by statically
 * importing the compiled JS, runs the TypeScript interpreter on it, and
 * prints the output for visual inspection.
 *
 * Invoked via `npx tsx scripts/smoke-test.ts` (or compiled JS).
 */

import { EXAMPLES } from '../src/lib/examples';
import { Lexer } from '../src/python/lexer';
import { Parser } from '../src/python/parser';
import { Interpreter, OutputWriter } from '../src/python/interpreter';

interface BufferedWriter extends OutputWriter {
  stdout: (text: string) => void;
  stderr: (text: string) => void;
}

function makeBufferedWriter(): { writer: BufferedWriter; output: () => string } {
  const buf: string[] = [];
  const writer: BufferedWriter = {
    stdout(text: string) {
      buf.push(text);
    },
    stderr(text: string) {
      buf.push(text);
    },
  };
  return { writer, output: () => buf.join('') };
}

let failed = 0;
let passed = 0;

for (const ex of EXAMPLES) {
  console.log('==================================================');
  console.log(`Example: ${ex.name}  (id=${ex.id})`);
  console.log('--------------------------------------------------');
  try {
    const { writer, output: getOutput } = makeBufferedWriter();
    const lexer = new Lexer(ex.code);
    const tokens = lexer.tokenize();
    const parser = new Parser(tokens);
    const program = parser.parse();
    const interpreter = new Interpreter(writer);
    interpreter.interpret(program);
    const output = getOutput();
    if (output.length === 0) {
      console.log('(no output)');
    } else {
      // Indent the output for readability.
      const indented = output
        .split('\n')
        .map((line) => (line.length > 0 ? `  ${line}` : ''))
        .join('\n');
      process.stdout.write(indented);
      if (!output.endsWith('\n')) process.stdout.write('\n');
    }
    passed += 1;
  } catch (e: any) {
    failed += 1;
    console.error(`FAILED: ${e?.message ?? e}`);
  }
}

console.log('==================================================');
console.log(`Smoke test: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
