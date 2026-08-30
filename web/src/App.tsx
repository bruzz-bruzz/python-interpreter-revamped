import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Header } from './components/Header';
import { Toolbar } from './components/Toolbar';
import { Editor } from './components/Editor';
import { Output, OutputLine } from './components/Output';
import { runProgram } from './python/interpreter-bridge';
import { getPyodide } from './python/pyodide';
import { EXAMPLES } from './lib/examples';
import { loadBuffer, loadLastExample, saveBuffer, saveLastExample } from './lib/storage';

const DEFAULT_EXAMPLE = 'hello';

export default function App() {
  // -------- state --------
  const initialExampleId = loadLastExample() ?? DEFAULT_EXAMPLE;
  const initialExample = EXAMPLES.find((e) => e.id === initialExampleId) ?? EXAMPLES[0];
  const initialSource = loadBuffer() ?? initialExample.source;

  const [source, setSource] = useState<string>(initialSource);
  const [activeExampleId, setActiveExampleId] = useState<string | null>(initialExample.id);

  const [lines, setLines] = useState<OutputLine[]>([]);
  const [status, setStatus] = useState<'idle' | 'loading' | 'running' | 'done' | 'error'>('idle');
  const abortRef = useRef<AbortController | null>(null);
  // We keep a ref to the latest `source` so the run callback always
  // sees the most up-to-date text without re-binding.
  const sourceRef = useRef(source);
  sourceRef.current = source;

  // Persist source on every change (debounced via a microtask).
  useEffect(() => {
    const t = setTimeout(() => saveBuffer(source), 200);
    return () => clearTimeout(t);
  }, [source]);

  // -------- actions --------
  const appendLine = useCallback((line: OutputLine) => {
    setLines((prev) => [...prev, line]);
  }, []);

  const run = useCallback(async () => {
    if (status === 'running' || status === 'loading') return;

    // Cancel any in-flight run.
    abortRef.current?.abort();
    const ctrl = new AbortController();
    abortRef.current = ctrl;

    setStatus('loading');
    setLines([]);

    try {
      // First, make sure Pyodide is up. After the first call it's
      // instant; until then we show the loading state.
      await getPyodide();
      setStatus('running');

      await runProgram(
        sourceRef.current,
        {
          onStdout: (line) => appendLine({ channel: 'stdout', text: line }),
          onStderr: (line) => appendLine({ channel: 'stderr', text: line }),
          onDone: (info) => {
            setStatus(info.ok ? 'done' : 'error');
          },
        },
        ctrl.signal,
      );
    } catch (err) {
      appendLine({ channel: 'stderr', text: `[playground] ${(err as Error).message}` });
      setStatus('error');
    }
  }, [status, appendLine]);

  const stop = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  const clearOutput = useCallback(() => {
    setLines([]);
    setStatus('idle');
  }, []);

  const pickExample = useCallback((id: string) => {
    const ex = EXAMPLES.find((e) => e.id === id);
    if (!ex) return;
    setSource(ex.source);
    setActiveExampleId(ex.id);
    saveLastExample(ex.id);
  }, []);

  // -------- keyboard shortcut at the app level (in addition to the
  // editor's own Ctrl+Enter binding, so it works when the editor
  // hasn't been focused yet). --------
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        void run();
      }
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [run]);

  // -------- derived --------
  const isReady = useMemo(() => status !== 'loading', [status]);

  return (
    <div className="flex h-full min-h-screen flex-col">
      <Header />
      <Toolbar
        isRunning={status === 'running' || status === 'loading'}
        isReady={isReady}
        onRun={run}
        onStop={stop}
        onClearOutput={clearOutput}
        onPickExample={pickExample}
        activeExampleId={activeExampleId}
      />

      <main className="mx-auto w-full max-w-7xl flex-1 p-4">
        <div className="grid h-[calc(100vh-220px)] min-h-[420px] grid-cols-1 gap-4 lg:grid-cols-2">
          <section className="flex h-full flex-col">
            <div className="mb-2 flex items-center justify-between text-xs text-slate-400">
              <span className="font-medium text-slate-300">Source</span>
              <span>{source.split('\n').length} lines</span>
            </div>
            <div className="min-h-0 flex-1">
              <Editor value={source} onChange={setSource} onRun={run} />
            </div>
          </section>

          <section className="flex h-full flex-col">
            <div className="mb-2 flex items-center justify-between text-xs text-slate-400">
              <span className="font-medium text-slate-300">Output</span>
              <span>{lines.length} line{lines.length === 1 ? '' : 's'}</span>
            </div>
            <div className="min-h-0 flex-1">
              <Output lines={lines} status={status} onClear={clearOutput} />
            </div>
          </section>
        </div>
      </main>

      <footer className="border-t border-ink-600 bg-ink-800/50 px-4 py-2 text-center text-[11px] text-slate-500">
        Python runs in your browser via Pyodide. No data leaves this page.
      </footer>
    </div>
  );
}
