import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
  },
  // Pyodide loads its runtime from a CDN at runtime, so we don't need
  // to bundle it. The `optimizeDeps` exclusion avoids Vite pre-bundling
  // a WASM module that doesn't like it.
  optimizeDeps: {
    exclude: ['pyodide'],
  },
});
