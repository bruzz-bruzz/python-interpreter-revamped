# Python-subset Playground — web frontend

A browser playground for the Python-subset tree-walking interpreter that
lives in the parent directory. Runs **entirely in the browser** thanks
to [Pyodide](https://pyodide.org/) (CPython compiled to WebAssembly);
no Python toolchain is needed on the user's machine or on the host.

The Python source files from `../src/` and `../examples/` are bundled
into the JS at build time via Vite's `?raw` import suffix, so the
deployed app is a static bundle that can be served from any HTTP
server — including Vercel, Netlify, GitHub Pages, or `python -m
http.server`.

## Stack

- **Vite 5** + **React 18** + **TypeScript 5**
- **Tailwindcss 3** (PostCSS pipeline)
- **CodeMirror 6** (`@uiw/react-codemirror` + `@codemirror/lang-python`)
- **Pyodide 0.27** loaded from the jsDelivr CDN at runtime

## Develop

```bash
npm install
npm run dev      # http://localhost:5173
```

## Type-check / build

```bash
npm run typecheck
npm run build    # outputs dist/
```

## Deploy to Vercel

The repository ships with a `vercel.json` at the root, so a one-click
"New Project" import just works. Vercel will:

1. Run `cd web && npm install --no-audit --no-fund && npm run build`
2. Serve the contents of `web/dist/`
3. Rewrite every URL to `/index.html` (SPA fallback)
4. Cache the `/assets/*` directory for one year

### Option 1 — One-click deploy

The button below opens Vercel's "New Project" flow pre-pointed at this
repo. Click it and accept the defaults:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fbruzz-bruzz%2Fpython-interpreter-revamped&project-name=python-interpreter-playground&root-directory=.)

> If Vercel asks for a "Root Directory", leave it blank — the root
> `vercel.json` already tells it where to look.

### Option 2 — Vercel CLI

```bash
npm i -g vercel
vercel        # first run: log in, accept the project settings
vercel --prod # deploy to production
```

### Option 3 — Manual

1. Push the repo to GitHub / GitLab / Bitbucket.
2. On <https://vercel.com/new>, import the repository.
3. Vercel reads the root `vercel.json`; no further config is needed.
4. Click **Deploy**. After ~30 s the playground is live on
   `https://<project-name>.vercel.app`.

## How it works

When the user clicks **Run**:

1. `src/python/pyodide.ts` injects `<script src="…/pyodide.js">` and
   initialises Pyodide from the CDN (cached on the second run).
2. The Python sources of the lexer / parser / interpreter / builtins
   are written into Pyodide's in-memory filesystem at `/lib/`.
3. `src/python/interpreter-bridge.ts` installs a stdout / stderr
   proxy that pushes each complete line to a JS callback.
4. The user's program is written to `/user.py` and executed by
   `Interpreter().interpret(Parser(Lexer(...).tokenize()).parse())`.

The Pyodide WASM itself is **not** bundled — it's fetched from
jsDelivr at runtime, so the JS bundle stays under 250 kB gzipped.

## Project layout

```
web/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
├── tsconfig.node.json
├── public/
│   └── favicon.svg
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── components/
    │   ├── Editor.tsx   # CodeMirror editor (Python highlighting)
    │   ├── Output.tsx   # stdout / stderr panel
    │   ├── Toolbar.tsx  # Run / Stop / Clear / Example picker
    │   └── Header.tsx
    ├── python/
    │   ├── pyodide.ts             # Pyodide loader + FS bootstrap
    │   └── interpreter-bridge.ts  # Streams code → Pyodide → output
    └── lib/
        ├── examples.ts  # Bundled example programs
        └── storage.ts   # localStorage persistence
```
