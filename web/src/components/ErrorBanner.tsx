import React from 'react';

interface ErrorBannerProps {
  message: string | null;
  onDismiss?: () => void;
  className?: string;
}

/**
 * A small inline error banner. Shown at the top of the output / editor when
 * the interpreter raises an error.
 */
const ErrorBanner: React.FC<ErrorBannerProps> = ({
  message,
  onDismiss,
  className = '',
}) => {
  if (!message) return null;
  return (
    <div
      role="alert"
      className={`flex items-start gap-2 rounded-md border border-rose-700/60 bg-rose-950/60 px-3 py-2 text-sm text-rose-200 ${className}`}
    >
      <span className="mt-0.5 font-semibold">⚠</span>
      <pre className="flex-1 whitespace-pre-wrap break-words font-mono text-[0.8rem] leading-relaxed">
        {message}
      </pre>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          className="rounded px-1 text-rose-300 hover:bg-rose-900/60"
          aria-label="Dismiss error"
        >
          ✕
        </button>
      )}
    </div>
  );
};

export default ErrorBanner;
