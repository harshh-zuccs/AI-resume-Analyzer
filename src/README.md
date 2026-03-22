# AI Resume Analyzer

An intelligent resume scoring tool. Upload a PDF résumé, pick a target job role, and instantly see your match score, matched skills, missing skills, and a personalised recommendation.

---

## Project Structure

```
├── api.py               # FastAPI backend
├── matcher.py           # Scoring logic (TF-IDF + skill overlap)
├── skill_extraction.py  # NLP skill extraction (spaCy + SKILL_DB)
├── job_roles.py         # Job description keyword bank
├── index.html           # Frontend UI
├── styles.css           # Styling
├── scripts.js           # Frontend logic
└── requirements.txt     # Python dependencies
```

---

## Local Setup

### 1 — Clone / download the project

```bash
git clone <your-repo-url>
cd ai-resume-analyzer
```

### 2 — Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4 — Start the backend

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at `http://127.0.0.1:8000`.

### 5 — Open the frontend

Open `index.html` directly in your browser (double-click) or serve it with any static server:

```bash
# Python quick server
python -m http.server 5500
```

Then visit `http://localhost:5500`.

---

## Deploying to a Server (e.g. Render / Railway / EC2)

1. Push all files to a GitHub repository.
2. On your hosting provider, set the **start command** to:
   ```
   uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
3. Add a **build command**:
   ```
   pip install -r requirements.txt && python -m spacy download en_core_web_sm
   ```
4. Update `API_URL` and `ROLES_URL` in `scripts.js` to point to your deployed backend URL instead of `http://127.0.0.1:8000`.

---

## Bug Fixes Applied

| File | Bug | Fix |
|------|-----|-----|
| `skill_extraction.py` | Missing comma caused string concatenation, silently dropping ~8 skills | Fixed comma; rebuilt complete `SKILL_DB` covering all 10 roles |
| `skill_extraction.py` | Token-by-token matching failed for compound/hyphenated skills (`node.js`, `scikit-learn`, `ci/cd`) | Replaced with substring + variant matching |
| `api.py` | `job_text` assigned inside `else` block but used outside it — `custom_jd` was always ignored | Moved assignment to correct scope |
| `matcher.py` | Division by zero when `job_skills` is empty | Added guard clause |
| `job_roles.py` | Skill keywords too sparse; most roles returned 0 matches | Expanded every role description with the full relevant skill vocabulary |
