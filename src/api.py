from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from matcher import analyze_resume
from skill_extraction import extract_skills
from job_roles import job_descriptions
import PyPDF2

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/roles")
def get_roles():
    """Return all available job roles."""
    return {"roles": list(job_descriptions.keys())}


@app.post("/analyze-pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    job_role: str = Form(...),
    custom_jd: str = Form(""),
):
    # ── 1. Extract text from uploaded PDF ────────────────────────────────────
    pdf_text = extract_text_from_pdf(file.file)

    if not pdf_text.strip():
        return {"error": "Could not extract text from the uploaded PDF. Please ensure it is not scanned/image-only."}

    # ── 2. Resolve job description text ──────────────────────────────────────
    # BUG FIX: previously job_text was assigned inside the else block but read
    # outside it, so custom_jd was silently ignored.
    if custom_jd.strip():
        job_text = custom_jd
    else:
        if job_role not in job_descriptions:
            return {
                "error": f"Invalid job role: '{job_role}'",
                "available_roles": list(job_descriptions.keys()),
            }
        job_text = job_descriptions[job_role]

    # ── 3. Extract skills & analyse ───────────────────────────────────────────
    job_skills = extract_skills(job_text)

    if not job_skills:
        return {"error": "No recognisable skills found in the job description."}

    score, resume_skills, missing, recommendation = analyze_resume(pdf_text, job_skills)

    return {
        "score": round(score, 2),
        "skills": resume_skills,
        "missing": missing,
        "recommendation": recommendation,
    }


# ── Helper ────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(file) -> str:
    try:
        reader = PyPDF2.PdfReader(file)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return ""
