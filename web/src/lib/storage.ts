/**
 * Tiny localStorage wrapper for persisting the editor buffer and
 * the last-selected example between reloads.
 */

const KEY_BUFFER = 'py-playground:buffer';
const KEY_EXAMPLE = 'py-playground:last-example';

export function loadBuffer(): string | null {
  try {
    return localStorage.getItem(KEY_BUFFER);
  } catch {
    return null;
  }
}

export function saveBuffer(source: string): void {
  try {
    localStorage.setItem(KEY_BUFFER, source);
  } catch {
    /* private mode / quota — silently ignore */
  }
}

export function loadLastExample(): string | null {
  try {
    return localStorage.getItem(KEY_EXAMPLE);
  } catch {
    return null;
  }
}

export function saveLastExample(id: string): void {
  try {
    localStorage.setItem(KEY_EXAMPLE, id);
  } catch {
    /* ignore */
  }
}
