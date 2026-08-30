/**
 * High-level "run user code" wrapper. Streams stdout/stderr line-by-line
 * through a callback so the UI can render incrementally.
 */

import { getPyodide } from './pyodide';

export interface RunCallbacks {
  onStdout: (line: string) => void;
  onStderr: (line: string) => void;
  onDone: (info: { ok: true } | { ok: false; error: string }) => void;
}

/**
 * Run a Python-subset program. Streams lines as they are produced.
 *
 * Pyodide's `runPythonAsync` doesn't easily yield partial stdout
 * unless we register a custom stream. We do that with
 * `setStdout({ batched })` and pull chunks through a queue.
 */
export async function runProgram(
  source: string,
  cb: RunCallbacks,
  signal: AbortSignal,
): Promise<void> {
  let pyodide;
  try {
    pyodide = await getPyodide();
  } catch (err) {
    cb.onStderr(
      `[playground] Could not start Python runtime: ${(err as Error).message}`,
    );
    cb.onDone({ ok: false, error: (err as Error).message });
    return;
  }

  // Build a Python source string that:
  //  - writes the user's program to /user.py
  //  - installs custom stdout/stderr that push to a JS-side queue
  //  - lexes / parses / interprets
  //  - flushes everything at the end
  //
  // We escape the source with repr() to handle all the multi-line
  // strings, quotes, and unicode that user code may contain.
  const escaped = JSON.stringify(source);

  const driver = `
import sys, traceback

USER_SOURCE = ${escaped}

# --- stream bridge ---
class _StreamProxy:
    def __init__(self, target, is_err=False):
        self._target = target
        self._is_err = is_err
        self._buf = ""

    def write(self, s):
        if not s:
            return 0
        self._buf += s
        # Flush complete lines immediately so the UI can render them.
        while "\\n" in self._buf:
            line, self._buf = self._buf.split("\\n", 1)
            self._target(line)
        return len(s)

    def flush(self):
        if self._buf:
            self._target(self._buf)
            self._buf = ""

# JS-side callbacks (we look them up via pyodide.globals.get)
import js
_on_stdout = js._onStdout
_on_stderr = js._onStderr

def _push_stdout(line): _on_stdout(line)
def _push_stderr(line): _on_stderr(line)

_real_stdout = sys.stdout
_real_stderr = sys.stderr
sys.stdout = _StreamProxy(_push_stdout, is_err=False)
sys.stderr = _StreamProxy(_push_stderr, is_err=True)

ok = True
err_msg = ""
try:
    # Stage the user source in /user.py so any errors are reported
    # against "user.py" rather than the driver.
    import os
    with open("/user.py", "w", encoding="utf-8") as f:
        f.write(USER_SOURCE)
    from lexer.lexer import Lexer
    from parser.parser import Parser
    from interpreter.interpreter import Interpreter

    tokens = Lexer(USER_SOURCE, filename="user.py").tokenize()
    program = Parser(tokens).parse()
    Interpreter().interpret(program)
except SystemExit as e:
    err_msg = f"SystemExit: {e.code}"
    ok = False
except BaseException as e:
    err_msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    ok = False
finally:
    sys.stdout = _real_stdout
    sys.stderr = _real_stderr
    # Flush any partial trailing line.
    sys.stdout.flush() if hasattr(sys.stdout, "flush") else None
    sys.stderr.flush() if hasattr(sys.stderr, "flush") else None

js._onDone(ok, err_msg)
`;

  // Hook the JS callbacks into the Pyodide global namespace so the
  // driver can find them. We delete them after the run completes.
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const w = window as any;
  w._onStdout = (line: string) => cb.onStdout(line);
  w._onStderr = (line: string) => cb.onStderr(line);
  w._onDone = (ok: boolean, err: string) => {
    delete w._onStdout;
    delete w._onStderr;
    delete w._onDone;
    cb.onDone(
      ok ? { ok: true } : { ok: false, error: err },
    );
  };

  // Wire up abort. Pyodide doesn't have a direct cancel API for a
  // running Python script, so we set a flag the user can check
  // and rely on the next runProgram call to discard any late output.
  w._aborted = false;
  const onAbort = () => {
    w._aborted = true;
    cb.onStderr('[playground] Stop requested.');
  };
  if (signal.aborted) {
    onAbort();
  } else {
    signal.addEventListener('abort', onAbort, { once: true });
  }

  try {
    await pyodide.runPythonAsync(driver);
  } catch (err) {
    // runPythonAsync itself can throw (e.g. import error inside the
    // driver). Surface that as a stderr line and finish.
    cb.onStderr(`[pyodide] ${(err as Error).message}`);
    cb.onDone({ ok: false, error: (err as Error).message });
  } finally {
    signal.removeEventListener('abort', onAbort);
    delete w._aborted;
  }
}
