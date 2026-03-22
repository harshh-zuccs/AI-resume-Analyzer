from fastapi import FastAPI,UploadFile,File,Form
from matcher import analyze_resume
from skill_extraction import extract_skills
import PyPDF2

app = FastAPI()

job_descriptions = {

    "Data Scientist": """
    Looking for a Data Scientist with experience in Python, machine learning,
    data analysis, statistics, pandas, numpy and SQL.
    """,

    "Web Developer": """
    Looking for a Web Developer skilled in HTML, CSS, JavaScript, React,
    NodeJS and Git.
    """,

    "HR Manager": """
    Looking for an HR Manager with experience in recruitment, employee relations,
    payroll, performance management, communication and organizational skills.
    """,

    "Marketing Manager": """
    Looking for a Marketing Manager skilled in marketing strategy, digital marketing,
    social media, branding, market research, communication and campaign management.
    """
}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...), job_role: str = Form(...)):

    print("Received request") 

    # Read file
    pdf_text = extract_text_from_pdf(file.file)

    print("Job role:", job_role) 
    print("Job role:", job_role) 

    # Validate job role
    if job_role not in job_descriptions:
        return {
            "error": "Invalid job role",
            "available_roles": list(job_descriptions.keys())
        }

    job_text = job_descriptions[job_role]

    job_skills = extract_skills(job_text)

    score, skills, missing, recommendation = analyze_resume(pdf_text, job_skills)

    return {
        "score": score,
        "skills": skills,
        "missing": missing,
        "recommendation": recommendation
    }


def extract_text_from_pdf(file):

    pdf_reader = PyPDF2.PdfReader(file)
    
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text