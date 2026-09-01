import React, { useEffect, useRef } from 'react';

export interface OutputLine {
  kind: 'stdout' | 'stderr';
  text: string;
}

interface OutputProps {
  lines: OutputLine[];
  className?: string;
}

/**
 * The output pane. Renders the captured stdout/stderr lines from the
 * interpreter. Auto-scrolls to the bottom whenever new lines arrive.
 */
const Output: React.FC<OutputProps> = ({ lines, className = '' }) => {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'auto', block: 'end' });
  }, [lines]);

  return (
    <div
      className={`flex h-full flex-col overflow-hidden rounded-md bg-slate-950 ring-1 ring-slate-800 ${className}`}
    >
      <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900/60 px-3 py-1.5 text-xs uppercase tracking-wider text-slate-400">
        <span>Output</span>
        <span className="text-slate-500">{lines.length} line(s)</span>
      </div>
      <div className="scrollbar-thin flex-1 overflow-auto p-3 font-mono text-sm leading-relaxed">
        {lines.length === 0 ? (
          <div className="text-slate-600">
            (no output yet — press <span className="text-slate-400">Run</span> or{' '}
            <kbd className="rounded border border-slate-700 bg-slate-800 px-1.5 py-0.5 text-[0.7rem] text-slate-300">
              Ctrl/⌘ + Enter
            </kbd>{' '}
            to execute the program)
          </div>
        ) : (
          lines.map((line, idx) => (
            <div
              key={idx}
              className={
                line.kind === 'stderr'
                  ? 'whitespace-pre-wrap text-rose-300'
                  : 'whitespace-pre-wrap text-slate-100'
              }
            >
              {line.text}
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};

export default Output;
