# CV-Driven AI Interviewer Frontend

React + TypeScript UI for the V2 text interview flow.

## Routes

- `/text-interview` - start a text interview from an existing candidate id
- `/text-interview/:sessionId` - resume a text interview session
- `/settings` - local defaults for interview configuration

## Run

```bash
npm install
npm run dev
```

Set `VITE_API_BASE_URL` to the backend origin, without a trailing `/api`. During
local Vite development it defaults to `http://127.0.0.1:8000`; production builds
without this variable use the current origin.

## Build

```bash
npm run build
```

Production builds require all values in `.env.production.example` and fail with
a list of missing names. These variables contain the public Firebase web app
configuration and backend origin only. Never place a Firebase ID token, service
account key, or backend secret in a `VITE_*` variable.

## Firebase Hosting

The included `firebase.json` publishes `dist`, rewrites SPA routes to
`index.html`, caches hashed assets for one year, and disables caching for the
HTML entry point.

```bash
npm run build
npx firebase-tools deploy --only hosting --project <project-id>
```

Add the resulting `*.web.app` and any custom production domain to Firebase
Authentication's Authorized Domains list before testing Google Sign-In.
