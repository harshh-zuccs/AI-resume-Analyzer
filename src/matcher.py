# import sys
# sys.path.append("../src")

# from matcher import analyze_resume, rank_resumes



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skill_extraction import extract_skills


def analyze_resume(resume_text, job_skills):

    resume_skills = extract_skills(resume_text)

    # Convert skills to text
    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_skills)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Hybrid score
    skill_match = len(set(resume_skills) & set(job_skills)) / len(job_skills)

    score = (0.7 * skill_match + 0.3 * similarity[0][0]) * 100

    missing = list(set(job_skills) - set(resume_skills))

    if missing:
        recommendation = f"Improve your resume by learning: {', '.join(missing)}"
    else:
        recommendation = "Your resume is well matched for this role"

    return score, resume_skills, missing, recommendation


def rank_resumes(resume_df, job_text):

    results = []

    #  Compute once
    job_skills = extract_skills(job_text)

    for i in range(10):   # testing

        resume = resume_df['clean_resume'].iloc[i]

        score, skills, missing = analyze_resume(resume, job_skills)

        print("Processing:", i)

        results.append({
            "index": i,
            "score": score,
            "skills": skills,
            "missing": missing
        })

    ranked = sorted(results, key=lambda x: x["score"], reverse=True)

    return ranked

