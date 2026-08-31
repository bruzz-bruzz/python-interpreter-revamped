/**
 * Pyodide runtime loader and interpreter bridge.
 *
 * The browser doesn't have a Python interpreter, so we load Pyodide
 * (a WebAssembly build of CPython) from the official CDN and use it
 * to execute the Python-subset interpreter itself.
 *
 * On first call, we:
 *   1. Load Pyodide.
 *   2. Reconstruct the repository layout under /playground in
 *      Pyodide's in-memory filesystem: every `.py` file in
 *      `src/` (and its sub-packages) is written to
 *      `/playground/src/...`. This way the in-tree absolute
 *      imports — e.g. `from src.ast.nodes import *` inside
 *      `parser.py` — resolve just like they do in the CLI.
 *   3. Add `/playground` to `sys.path` and warm-import
 *      `src.parser.parser` / `src.interpreter.interpreter` so
 *      Pyodide catches any syntax / typo errors at install time
 *      rather than on the first user click.
 *
 * Subsequent calls just re-run the user's program against the
 * already-loaded interpreter.
 */

import type { PyodideInterface } from 'pyodide';

// The Python sources are imported as raw strings via Vite's
// `?raw` query suffix. This keeps everything in one bundle and
// avoids any CORS / fetch issues at runtime.
import srcInit from '../../../src/__init__.py?raw';
import lexerInit from '../../../src/lexer/__init__.py?raw';
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

/** Virtual location of the in-browser "repo root". */
const PROJ_ROOT = '/playground';

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
  // Lay the package out under PROJ_ROOT/src/ in Pyodide's virtual FS,
  // mirroring the on-disk layout so the in-tree absolute imports
  // (`from src.ast.nodes import *` etc.) resolve unchanged.
  const files: Array<[string, string]> = [
    [`${PROJ_ROOT}/src/__init__.py`, srcInit],
    [`${PROJ_ROOT}/src/lexer/__init__.py`, lexerInit],
    [`${PROJ_ROOT}/src/lexer/lexer.py`, lexerSrc],
    [`${PROJ_ROOT}/src/ast/__init__.py`, astInit],
    [`${PROJ_ROOT}/src/ast/nodes.py`, astNodesSrc],
    [`${PROJ_ROOT}/src/parser/__init__.py`, parserInit],
    [`${PROJ_ROOT}/src/parser/parser.py`, parserSrc],
    [`${PROJ_ROOT}/src/interpreter/__init__.py`, interpInit],
    [`${PROJ_ROOT}/src/interpreter/interpreter.py`, interpreterSrc],
    [`${PROJ_ROOT}/src/builtins/__init__.py`, builtinsInit],
    [`${PROJ_ROOT}/src/builtins/functions.py`, builtinsFunctions],
    [`${PROJ_ROOT}/src/builtins/types.py`, builtinsTypes],
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
  // it the recommended API surface). We also pre-import the three
  // entry-point classes so any import / typo error surfaces here
  // (with a clean stack trace) rather than on the first user click.
  await pyodide.runPythonAsync(`
import sys, os
sys.path.insert(0, ${JSON.stringify(PROJ_ROOT)})

# Verify the FS layout matches expectations. (Cheap, and the
# error message is much friendlier than a bare ModuleNotFoundError.)
for _p in (
    ${JSON.stringify(`${PROJ_ROOT}/src`)},
    ${JSON.stringify(`${PROJ_ROOT}/src/parser/parser.py`)},
):
    if not os.path.exists(_p):
        raise RuntimeError(f"playground FS bootstrap failed: {_p} is missing")

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter

print("[pyodide] interpreter ready", file=sys.stderr)
`);
}
