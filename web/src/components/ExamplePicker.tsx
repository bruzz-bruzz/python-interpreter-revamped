import React from 'react';
import { EXAMPLES, Example } from '../lib/examples';

interface ExamplePickerProps {
  value: string;
  onChange: (id: string) => void;
  className?: string;
}

/**
 * Drop-down picker for the bundled example programs. Selecting an example
 * hands the example object back to the parent for loading.
 */
const ExamplePicker: React.FC<ExamplePickerProps> = ({
  value,
  onChange,
  className = '',
}) => {
  const current: Example | undefined = EXAMPLES.find((e) => e.id === value);

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <label htmlFor="example-picker" className="text-xs text-slate-400">
        Example:
      </label>
      <select
        id="example-picker"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-sm text-slate-100 focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400"
      >
        {EXAMPLES.map((ex) => (
          <option key={ex.id} value={ex.id}>
            {ex.name}
          </option>
        ))}
      </select>
      {current && (
        <span className="hidden text-xs text-slate-500 md:inline">
          {current.description}
        </span>
      )}
    </div>
  );
};

export default ExamplePicker;
