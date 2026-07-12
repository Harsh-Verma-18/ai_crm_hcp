# Frontend — Log Interaction Screen

React + Redux Toolkit UI for the AI CRM HCP module. Talks to the FastAPI
backend for `/hcps`, `/interactions`, and `/ai/chat`.

## Setup (PowerShell, from `ai-crm-hcp\frontend`)

```powershell
npm install
copy .env.example .env
npm run dev
```

Then open http://localhost:5173 (make sure the backend is running on
http://localhost:8000 — see `backend/README` / earlier setup steps).

If your backend runs on a different host/port, edit `VITE_API_BASE_URL` in
`.env` accordingly.

## What's here

- `src/store/` — Redux Toolkit slices: `hcpSlice` (HCP list + selection),
  `interactionSlice` (structured-form create/edit + per-HCP history),
  `chatSlice` (conversation with the LangGraph agent, keyed by `thread_id`),
  `uiSlice` (form/chat mode toggle).
- `src/components/LogInteractionScreen.jsx` — composes the HCP picker, the
  mode toggle, and either `StructuredForm` or `ChatPanel`, plus the recent
  interaction timeline sidebar.
- `src/components/StructuredForm.jsx` — the discrete-fields path, posts
  directly to `POST /interactions/`.
- `src/components/ChatPanel.jsx` — the conversational path, posts to
  `POST /ai/chat`; the agent itself calls `log_interaction` /
  `edit_interaction` / etc. server-side.
