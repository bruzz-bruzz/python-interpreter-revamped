import { useCallback, useRef } from 'react';
import CodeMirror, { ReactCodeMirrorRef } from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { EditorView } from '@codemirror/view';
import { keymap, lineNumbers, highlightActiveLine } from '@codemirror/view';

interface EditorProps {
  value: string;
  onChange: (next: string) => void;
  onRun: () => void;
  readOnly?: boolean;
}

const darkTheme = EditorView.theme(
  {
    '&': {
      backgroundColor: '#11172a',
      color: '#e2e8f0',
    },
    '.cm-content': { caretColor: '#c1b3ff' },
    '.cm-cursor': { borderLeftColor: '#c1b3ff' },
    '&.cm-focused .cm-selectionBackground, ::selection': {
      backgroundColor: 'rgba(124, 92, 255, 0.25)',
    },
  },
  { dark: true },
);

export function Editor({ value, onChange, onRun, readOnly }: EditorProps) {
  const ref = useRef<ReactCodeMirrorRef | null>(null);

  const handleChange = useCallback(
    (next: string) => {
      onChange(next);
    },
    [onChange],
  );

  return (
    <div className="h-full w-full overflow-hidden panel">
      <CodeMirror
        ref={ref}
        value={value}
        height="100%"
        theme={darkTheme}
        extensions={[
          lineNumbers(),
          highlightActiveLine(),
          keymap.of([
            {
              key: 'Ctrl-Enter',
              mac: 'Cmd-Enter',
              preventDefault: true,
              run: () => {
                onRun();
                return true;
              },
            },
          ]),
          python(),
          EditorView.lineWrapping,
        ]}
        onChange={handleChange}
        readOnly={readOnly}
        basicSetup={{
          lineNumbers: true,
          highlightActiveLine: true,
          foldGutter: true,
          autocompletion: true,
          highlightSelectionMatches: false,
        }}
      />
    </div>
  );
}
