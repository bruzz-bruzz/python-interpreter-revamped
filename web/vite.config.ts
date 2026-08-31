import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Use a relative base so the built `index.html` works whether the
  // app is deployed at the domain root or under a subpath (e.g. on
  // Vercel preview URLs and user-named project domains).
  base: './',
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
  build: {
    outDir: 'dist',
    // Don't blow up the build if the bundle is on the larger side
    // (Pyodide-related code paths and CodeMirror push us over 500 kB).
    chunkSizeWarningLimit: 1500,
    // Split the heaviest dependencies into their own chunks so the
    // initial paint isn't blocked on CodeMirror / Pyodide code.
    rollupOptions: {
      output: {
        manualChunks: {
          'codemirror': [
            '@uiw/react-codemirror',
            '@codemirror/lang-python',
            'codemirror',
          ],
        },
      },
    },
  },
});
