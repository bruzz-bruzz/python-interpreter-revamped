import React from 'react';

interface HeaderProps {
  className?: string;
}

/**
 * Top-of-page header. Renders the app title and a short tagline.
 */
const Header: React.FC<HeaderProps> = ({ className = '' }) => {
  return (
    <header
      className={`border-b border-slate-800 bg-slate-900/70 backdrop-blur ${className}`}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-emerald-400 to-cyan-500 text-slate-900 font-bold">
            py
          </div>
          <div>
            <h1 className="text-base font-semibold text-slate-100">
              Python Interpreter Playground
            </h1>
            <p className="text-xs text-slate-400">
              A from-scratch Python subset running natively in your browser.
            </p>
          </div>
        </div>
        <div className="hidden text-xs text-slate-500 sm:block">
          Lexer · Parser · AST · Tree-walking Interpreter
        </div>
      </div>
    </header>
  );
};

export default Header;
