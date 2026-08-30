import { useEffect, useRef } from 'react';

export type OutputLine = { channel: 'stdout' | 'stderr'; text: string };

interface OutputProps {
  lines: OutputLine[];
  status: 'idle' | 'loading' | 'running' | 'done' | 'error';
  onClear: () => void;
}

const STATUS_LABEL: Record<OutputProps['status'], string> = {
  idle: 'Ready',
  loading: 'Loading Python runtime…',
  running: 'Running…',
  done: 'Finished',
  error: 'Error',
};

const STATUS_COLOR: Record<OutputProps['status'], string> = {
  idle: 'text-slate-400',
  loading: 'text-warn',
  running: 'text-accent-400',
  done: 'text-success',
  error: 'text-error',
};

export function Output({ lines, status, onClear }: OutputProps) {
  const scrollRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll to the bottom as new lines stream in.
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [lines.length, status]);

  return (
    <div className="panel flex h-full flex-col overflow-hidden">
      <div className="flex items-center justify-between border-b border-ink-600 px-3 py-2">
        <div className="flex items-center gap-2">
          <span
            className={`inline-block h-2 w-2 rounded-full ${
              status === 'running'
                ? 'bg-accent-400 animate-pulse-slow'
                : status === 'error'
                  ? 'bg-error'
                  : status === 'done'
                    ? 'bg-success'
                    : status === 'loading'
                      ? 'bg-warn animate-pulse-slow'
                      : 'bg-ink-500'
            }`}
          />
          <span className={`text-xs font-medium ${STATUS_COLOR[status]}`}>
            {STATUS_LABEL[status]}
          </span>
        </div>
        <button onClick={onClear} className="btn-ghost text-xs">
          Clear
        </button>
      </div>

      <div
        ref={scrollRef}
        className="flex-1 overflow-auto bg-ink-900/60 p-3 font-mono text-[13px] leading-relaxed"
      >
        {lines.length === 0 ? (
          <div className="text-slate-500 italic">
            Press <kbd className="rounded bg-ink-700 px-1.5 py-0.5 text-[11px] not-italic">Run</kbd> or
            hit <kbd className="rounded bg-ink-700 px-1.5 py-0.5 text-[11px] not-italic">Ctrl+Enter</kbd> to execute your program.
          </div>
        ) : (
          lines.map((line, i) => (
            <div
              key={i}
              className={`whitespace-pre-wrap break-words ${
                line.channel === 'stderr' ? 'text-error' : 'text-slate-200'
              } animate-fade-in`}
            >
              {line.text}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
