# Deployment Notes

## Backend on Render

Root Directory:

```text
backend
```

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

Health Check Path:

```text
/api/health
```

Required environment variables on Render:

```env
SECRET_KEY=replace-with-a-random-secret
FRONTEND_URL=https://your-frontend-name.vercel.app
DATABASE_URL=your-render-postgresql-url
```

You may use `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` instead of `DATABASE_URL`.

## Frontend on Vercel

Root Directory:

```text
frontend
```

Build Command:

```bash
npm run build
```

Output Directory:

```text
dist
```

Required environment variable on Vercel:

```env
VITE_API_BASE_URL=https://your-backend-name.onrender.com/api
```

## Notes

- `.env`, `venv`, `node_modules`, `__pycache__`, logs, and local database files are removed from this deployment-ready package.
- Model files under `backend/app/models/` and RAG/vector files under `backend/app/vector_store/` are kept because the backend needs them.
- The frontend style folder was normalized to lowercase `src/styles` so the Vercel Linux build does not fail from case-sensitive imports.
