Student Grade Prediction — Dev + Docker Compose

Local Dev
- Backend: FastAPI in student/main.py
  1) python -m venv .venv
  2) .venv\Scripts\activate
  3) pip install -r student\requirements.txt
  4) cd student && ..\.venv\Scripts\python main.py
  - Health: curl http://localhost:8000/api/health

- Frontend: React + Vite in react-project
  1) cd react-project
  2) npm install
  3) npm run dev
  - App: http://localhost:5173 (uses VITE_API_URL from .env.development)

Docker Compose
- Build + run both services:
  1) docker compose build
  2) docker compose up
  - API: http://localhost:8000/api/health
  - Web: http://localhost:5173

Deploy
- Backend: Push Docker image then deploy (Azure App Service for Containers or Render). Ensure port 8000 and /api path.
- Frontend: Vercel. Set VITE_API_URL to your backend URL + /api.
