export function Header() {
  return (
    <header className="border-b border-ink-600 bg-ink-800/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-gradient-to-br from-accent-500 to-ink-600 text-white shadow-glow">
            <span className="font-mono text-sm font-bold">py</span>
          </div>
          <div>
            <h1 className="text-base font-semibold leading-tight text-slate-100">
              Python-subset Playground
            </h1>
            <p className="text-[11px] text-slate-400">
              A tree-walking interpreter, in your browser.
            </p>
          </div>
        </div>
        <a
          href="https://github.com/bruzz-bruzz/python-interpreter-revamped"
          target="_blank"
          rel="noopener noreferrer"
          className="hidden text-xs text-slate-400 hover:text-slate-200 sm:block"
        >
          View source on GitHub ↗
        </a>
      </div>
    </header>
  );
}
