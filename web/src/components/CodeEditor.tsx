import React from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { EditorView } from '@codemirror/view';

interface CodeEditorProps {
  value: string;
  onChange: (next: string) => void;
  onRun?: () => void;
  className?: string;
  readOnly?: boolean;
}

/**
 * The code editor pane. Wraps CodeMirror with a Python language module and
 * a keyboard binding for Ctrl/Cmd+Enter to trigger a run.
 */
const CodeEditor: React.FC<CodeEditorProps> = ({
  value,
  onChange,
  onRun,
  className = '',
  readOnly = false,
}) => {
  const extensions = [
    python(),
    EditorView.lineWrapping,
    EditorView.theme({
      '&': { height: '100%' },
    }),
  ];

  return (
    <div className={`relative h-full overflow-hidden rounded-md ring-1 ring-slate-800 ${className}`}>
      <CodeMirror
        value={value}
        onChange={onChange}
        extensions={extensions}
        editable={!readOnly}
        basicSetup={{
          lineNumbers: true,
          highlightActiveLine: true,
          highlightActiveLineGutter: true,
          foldGutter: true,
          autocompletion: true,
          bracketMatching: true,
          closeBrackets: true,
        }}
        theme="dark"
        height="100%"
        onKeyDown={(event) => {
          if (onRun && (event.metaKey || event.ctrlKey) && event.key === 'Enter') {
            event.preventDefault();
            onRun();
          }
        }}
      />
    </div>
  );
};

export default CodeEditor;
