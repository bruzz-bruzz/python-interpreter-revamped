/**
 * Pyodide runtime loader and interpreter bridge.
 *
 * The browser doesn't have a Python interpreter, so we load Pyodide
 * (a WebAssembly build of CPython) from the official CDN and use it
 * to execute the Python-subset interpreter itself.
 *
 * On first call, we:
 *   1. Load Pyodide.
 *   2. Write every Python source file from /src/** into Pyodide's
 *      in-memory filesystem at /lib/.
 *   3. Add /lib to sys.path and import the package modules.
 *
 * Subsequent calls just re-run the user's program against the
 * already-loaded interpreter.
 */

import type { PyodideInterface } from 'pyodide';

// The Python sources are imported as raw strings via Vite's
// `?raw` query suffix. This keeps everything in one bundle and
// avoids any CORS / fetch issues at runtime.
import lexerSrc from '../../../src/lexer/lexer.py?raw';
import astInit from '../../../src/ast/__init__.py?raw';
import astNodesSrc from '../../../src/ast/nodes.py?raw';
import parserInit from '../../../src/parser/__init__.py?raw';
import parserSrc from '../../../src/parser/parser.py?raw';
import interpInit from '../../../src/interpreter/__init__.py?raw';
import interpreterSrc from '../../../src/interpreter/interpreter.py?raw';
import builtinsInit from '../../../src/builtins/__init__.py?raw';
import builtinsFunctions from '../../../src/builtins/functions.py?raw';
import builtinsTypes from '../../../src/builtins/types.py?raw';

const PYODIDE_VERSION = '0.27.4';
const PYODIDE_CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

let pyodidePromise: Promise<PyodideInterface> | null = null;

async function loadPyodideScript(): Promise<void> {
  // Inject the loader script exactly once.
  if (document.querySelector(`script[data-pyodide]`)) return;
  await new Promise<void>((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `${PYODIDE_CDN}pyodide.js`;
    script.dataset.pyodide = '1';
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () =>
      reject(new Error('Failed to load Pyodide from CDN. Are you online?'));
    document.head.appendChild(script);
  });
}

export async function getPyodide(): Promise<PyodideInterface> {
  if (pyodidePromise) return pyodidePromise;
  pyodidePromise = (async () => {
    await loadPyodideScript();
    // The loader exposes a global `loadPyodide` function.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const w = window as any;
    if (typeof w.loadPyodide !== 'function') {
      throw new Error('Pyodide loader script did not initialise correctly.');
    }
    const pyodide = await w.loadPyodide({ indexURL: PYODIDE_CDN });
    await installInterpreter(pyodide);
    return pyodide;
  })();
  return pyodidePromise;
}

async function installInterpreter(pyodide: PyodideInterface): Promise<void> {
  // Lay the package out under /lib/ in Pyodide's virtual FS.
  // We need to create the directories first; mkdirs is a no-op
  // if a parent is missing, so walk the tree.
  const files: Array<[string, string]> = [
    ['/lib/lexer/lexer.py', lexerSrc],
    ['/lib/ast/__init__.py', astInit],
    ['/lib/ast/nodes.py', astNodesSrc],
    ['/lib/parser/__init__.py', parserInit],
    ['/lib/parser/parser.py', parserSrc],
    ['/lib/interpreter/__init__.py', interpInit],
    ['/lib/interpreter/interpreter.py', interpreterSrc],
    ['/lib/builtins/__init__.py', builtinsInit],
    ['/lib/builtins/functions.py', builtinsFunctions],
    ['/lib/builtins/types.py', builtinsTypes],
  ];

  // Build the directory tree once, then write the files.
  const dirs = new Set<string>();
  for (const [path] of files) {
    const parts = path.split('/').slice(0, -1);
    let cur = '';
    for (const p of parts) {
      cur += '/' + p;
      dirs.add(cur);
    }
  }
  for (const dir of dirs) {
    pyodide.FS.mkdirTree(dir);
  }
  for (const [path, src] of files) {
    pyodide.FS.writeFile(path, src);
  }

  // Now make Python import them. We need to be inside a `runPythonAsync`
  // so we can use the `import` statement (and because Pyodide 0.27 made
  // it the recommended API surface).
  await pyodide.runPythonAsync(`
import sys
sys.path.insert(0, '/lib')

# Import the runtime pieces. We do NOT add them to a package;
# they're stand-alone modules and import each other with absolute
# imports.
from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter

print("[pyodide] interpreter ready", file=sys.stderr)
`);
}
