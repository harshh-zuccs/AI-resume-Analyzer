# AI Resume Analyzer

An AI-powered Resume Analyzer that matches resumes with job descriptions using NLP and Machine Learning.

## 🚀 Features

- Skill extraction using spaCy
- Resume-job matching (TF-IDF + skill matching)
- Resume ranking system
- FastAPI backend
- PDF resume upload support

## 🛠 Tech Stack

- Python
- FastAPI
- spaCy
- Scikit-learn

## ▶️ Run Locally

```bash
pip install -r requirements.txt
cd src
uvicorn api:app --reload

📌 API Endpoints
/analyze → Analyze text resume

/analyze-pdf → Upload and analyze PDF