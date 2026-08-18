# AI Persona — React + FastAPI

A premium ChatGPT-style interface for expressive AI personas. The frontend is React/Vite; the backend is FastAPI; Gemini provides the persona brain.

## Run locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="YOUR_KEY"
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The current Gemini integration uses Google's recommended `google-genai` SDK rather than the deprecated `google-generativeai` package. Set `GEMINI_API_KEY` in the backend environment; never expose the key in browser code.
