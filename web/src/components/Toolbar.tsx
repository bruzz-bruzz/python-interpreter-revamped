import React from 'react';

interface ToolbarProps {
  onRun: () => void;
  onStop?: () => void;
  onReset?: () => void;
  onClearOutput?: () => void;
  running: boolean;
  hasCode: boolean;
  className?: string;
}

/**
 * The toolbar that sits above the editor. Holds Run / Stop / Reset / Clear buttons.
 */
const Toolbar: React.FC<ToolbarProps> = ({
  onRun,
  onStop,
  onReset,
  onClearOutput,
  running,
  hasCode,
  className = '',
}) => {
  return (
    <div
      className={`flex items-center justify-between gap-2 border-b border-slate-800 bg-slate-900/40 px-4 py-2 ${className}`}
    >
      <div className="flex items-center gap-2">
        {running ? (
          <button
            type="button"
            onClick={onStop}
            className="inline-flex items-center gap-1.5 rounded-md bg-rose-600 px-3 py-1.5 text-sm font-medium text-white shadow-sm transition hover:bg-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-400"
          >
            <span className="inline-block h-2 w-2 rounded-sm bg-white" />
            Stop
          </button>
        ) : (
          <button
            type="button"
            onClick={onRun}
            disabled={!hasCode}
            className="inline-flex items-center gap-1.5 rounded-md bg-emerald-500 px-3 py-1.5 text-sm font-medium text-slate-900 shadow-sm transition hover:bg-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <span className="inline-block">▶</span>
            Run
          </button>
        )}
        {onReset && (
          <button
            type="button"
            onClick={onReset}
            className="inline-flex items-center gap-1.5 rounded-md border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm font-medium text-slate-200 transition hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500"
          >
            Reset
          </button>
        )}
        {onClearOutput && (
          <button
            type="button"
            onClick={onClearOutput}
            className="inline-flex items-center gap-1.5 rounded-md border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm font-medium text-slate-200 transition hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500"
          >
            Clear output
          </button>
        )}
      </div>
      <div className="text-xs text-slate-500">
        {running ? (
          <span className="inline-flex items-center gap-1.5">
            <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
            Running…
          </span>
        ) : (
          <span>Ready</span>
        )}
      </div>
    </div>
  );
};

export default Toolbar;
