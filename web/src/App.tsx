import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import Header from './components/Header';
import Toolbar from './components/Toolbar';
import CodeEditor from './components/CodeEditor';
import Output, { OutputLine } from './components/Output';
import ExamplePicker from './components/ExamplePicker';
import ErrorBanner from './components/ErrorBanner';
import { EXAMPLES, DEFAULT_EXAMPLE_ID, getExampleById } from './lib/examples';
import { Lexer } from './python/lexer';
import { Parser } from './python/parser';
import { Interpreter, OutputWriter } from './python/interpreter';

const STORAGE_CODE_KEY = 'py-playground:code:v1';
const STORAGE_EXAMPLE_KEY = 'py-playground:example:v1';

/**
 * Read a string from localStorage safely.
 */
function loadString(key: string, fallback: string): string {
  try {
    if (typeof window === 'undefined') return fallback;
    const raw = window.localStorage.getItem(key);
    if (raw === null) return fallback;
    return raw;
  } catch {
    return fallback;
  }
}

function saveString(key: string, value: string): void {
  try {
    if (typeof window === 'undefined') return;
    window.localStorage.setItem(key, value);
  } catch {
    /* ignore quota / private-mode errors */
  }
}

/**
 * A simple line-buffered OutputWriter that pushes each printed line into
 * a callback so React can render it.
 */
function makeOutputWriter(onLine: (line: OutputLine) => void): OutputWriter {
  return {
    stdout(text: string) {
      // Each `print()` call already includes its trailing '\n', so each
      // stdout call is a single line of output.
      onLine({ kind: 'stdout', text });
    },
    stderr(text: string) {
      onLine({ kind: 'stderr', text });
    },
  };
}

const App: React.FC = () => {
  const initialExampleId = loadString(STORAGE_EXAMPLE_KEY, DEFAULT_EXAMPLE_ID);
  const initialExample =
    getExampleById(initialExampleId) ?? getExampleById(DEFAULT_EXAMPLE_ID)!;

  const [exampleId, setExampleId] = useState<string>(initialExample.id);
  const [code, setCode] = useState<string>(() =>
    loadString(STORAGE_CODE_KEY, initialExample.code)
  );
  const [output, setOutput] = useState<OutputLine[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState<boolean>(false);

  // Ref so async/timeout-based code can read the running flag without
  // forcing a re-render.
  const runningRef = useRef<boolean>(false);

  // Persist code & current example to localStorage.
  useEffect(() => {
    saveString(STORAGE_CODE_KEY, code);
  }, [code]);
  useEffect(() => {
    saveString(STORAGE_EXAMPLE_KEY, exampleId);
  }, [exampleId]);

  const handleExampleChange = useCallback((id: string) => {
    const ex = getExampleById(id);
    if (!ex) return;
    setExampleId(id);
    setCode(ex.code);
    setOutput([]);
    setError(null);
  }, []);

  const handleClearOutput = useCallback(() => {
    setOutput([]);
    setError(null);
  }, []);

  const handleReset = useCallback(() => {
    const ex = getExampleById(exampleId) ?? getExampleById(DEFAULT_EXAMPLE_ID)!;
    setCode(ex.code);
    setOutput([]);
    setError(null);
  }, [exampleId]);

  const handleRun = useCallback(() => {
    if (runningRef.current) return;
    setRunning(true);
    runningRef.current = true;
    setError(null);
    setOutput([]);

    // Defer to a microtask so the UI can paint the "Running…" state first.
    queueMicrotask(() => {
      try {
        const writer = makeOutputWriter((line) => {
          setOutput((prev) => [...prev, line]);
        });

        const lexer = new Lexer(code);
        const tokens = lexer.tokenize();
        const parser = new Parser(tokens);
        const program = parser.parse();
        const interpreter = new Interpreter(writer);
        interpreter.interpret(program);
      } catch (e: any) {
        const message =
          e && typeof e === 'object' && 'message' in e
            ? String((e as { message: unknown }).message)
            : String(e);
        setError(message);
        setOutput((prev) => [...prev, { kind: 'stderr', text: message }]);
      } finally {
        setRunning(false);
        runningRef.current = false;
      }
    });
  }, [code]);

  const handleStop = useCallback(() => {
    // The interpreter is synchronous, so "stop" just flips the UI flag.
    // Long-running programs cannot be interrupted yet.
    runningRef.current = false;
    setRunning(false);
  }, []);

  const exampleOptions = useMemo(() => EXAMPLES, []);

  return (
    <div className="flex h-full min-h-screen flex-col bg-slate-950 text-slate-100">
      <Header />
      <div className="border-b border-slate-800 bg-slate-900/30 px-4 py-2">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-2">
          <ExamplePicker value={exampleId} onChange={handleExampleChange} />
          <div className="text-xs text-slate-500">
            {exampleOptions.length} bundled example
            {exampleOptions.length === 1 ? '' : 's'}
          </div>
        </div>
      </div>

      <Toolbar
        onRun={handleRun}
        onStop={handleStop}
        onReset={handleReset}
        onClearOutput={handleClearOutput}
        running={running}
        hasCode={code.trim().length > 0}
      />

      <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-3 p-3">
        <ErrorBanner message={error} onDismiss={() => setError(null)} />

        <div className="grid h-full min-h-[60vh] flex-1 grid-cols-1 gap-3 lg:grid-cols-2">
          <div className="flex h-full min-h-[40vh] flex-col">
            <div className="mb-1 flex items-center justify-between text-xs text-slate-400">
              <span>Source</span>
              <span className="text-slate-500">Ctrl/⌘ + Enter to run</span>
            </div>
            <CodeEditor
              value={code}
              onChange={setCode}
              onRun={running ? undefined : handleRun}
              className="flex-1"
            />
          </div>
          <div className="flex h-full min-h-[40vh] flex-col">
            <div className="mb-1 flex items-center justify-between text-xs text-slate-400">
              <span>Console</span>
              <span className="text-slate-500">
                {output.length} captured line{output.length === 1 ? '' : 's'}
              </span>
            </div>
            <Output lines={output} className="flex-1" />
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800 bg-slate-900/40 px-4 py-2 text-center text-xs text-slate-500">
        Built with React + Vite + TailwindCSS. The Python subset is interpreted
        from scratch in TypeScript — no Pyodide, no remote execution.
      </footer>
    </div>
  );
};

export default App;
