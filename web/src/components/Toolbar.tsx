import { EXAMPLES } from '../lib/examples';

interface ToolbarProps {
  isRunning: boolean;
  isReady: boolean;
  onRun: () => void;
  onStop: () => void;
  onClearOutput: () => void;
  onPickExample: (id: string) => void;
  activeExampleId: string | null;
}

export function Toolbar({
  isRunning,
  isReady,
  onRun,
  onStop,
  onClearOutput,
  onPickExample,
  activeExampleId,
}: ToolbarProps) {
  return (
    <div className="flex flex-wrap items-center gap-2 border-b border-ink-600 bg-ink-800/50 px-4 py-2">
      <div className="flex items-center gap-2">
        {isRunning ? (
          <button onClick={onStop} className="btn-danger" disabled={!isReady}>
            <StopIcon /> Stop
          </button>
        ) : (
          <button onClick={onRun} className="btn-primary" disabled={!isReady}>
            <PlayIcon /> Run
          </button>
        )}
        <button onClick={onClearOutput} className="btn-ghost" title="Clear output">
          <BroomIcon /> Clear
        </button>
      </div>

      <div className="mx-2 hidden h-6 w-px bg-ink-600 sm:block" />

      <label className="flex items-center gap-2 text-xs text-slate-400">
        Example:
        <select
          className="rounded-md border border-ink-600 bg-ink-700 px-2 py-1 text-sm text-slate-100
                     focus:border-accent-500 focus:outline-none focus:ring-2 focus:ring-accent-500/40"
          value={activeExampleId ?? ''}
          onChange={(e) => onPickExample(e.target.value)}
          disabled={isRunning}
        >
          <option value="" disabled>
            Choose…
          </option>
          {EXAMPLES.map((ex) => (
            <option key={ex.id} value={ex.id}>
              {ex.name}
            </option>
          ))}
        </select>
      </label>

      <div className="ml-auto flex items-center gap-2 text-[11px] text-slate-500">
        <kbd className="rounded bg-ink-700 px-1.5 py-0.5">Ctrl</kbd>
        <span>+</span>
        <kbd className="rounded bg-ink-700 px-1.5 py-0.5">Enter</kbd>
        <span>to run</span>
      </div>
    </div>
  );
}

function PlayIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M8 5v14l11-7z" />
    </svg>
  );
}
function StopIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <rect x="6" y="6" width="12" height="12" rx="1.5" />
    </svg>
  );
}
function BroomIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
      <path d="M3 21h18M5 21V11l7-7 7 7v10M9 21v-6h6v6" />
    </svg>
  );
}
