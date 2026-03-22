from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skill_extraction import extract_skills


def analyze_resume(resume_text: str, job_skills: list[str]):
    """
    Compare a resume against a list of required job skills.

    Returns:
        score          (float)  – 0–100 match percentage
        resume_skills  (list)   – skills found in the resume
        missing        (list)   – skills in the JD but not in the resume
        recommendation (str)    – human-readable next step
    """
    resume_skills = extract_skills(resume_text)

    # ── BUG FIX: guard against empty skill lists ──────────────────────────────
    if not job_skills:
        return 0.0, resume_skills, [], "No job skills to compare against."

    # ── Skill-overlap score (primary signal) ─────────────────────────────────
    matched = set(resume_skills) & set(job_skills)
    skill_match = len(matched) / len(job_skills)

    # ── TF-IDF cosine similarity (secondary signal) ───────────────────────────
    # Convert skill lists to plain-text documents for vectorisation
    resume_doc = " ".join(resume_skills) if resume_skills else "none"
    job_doc    = " ".join(job_skills)

    try:
        vectorizer  = TfidfVectorizer()
        tfidf       = vectorizer.fit_transform([resume_doc, job_doc])
        similarity  = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
    except Exception:
        similarity = 0.0

    # ── Hybrid score: 70 % skill overlap + 30 % cosine similarity ────────────
    score = (0.7 * skill_match + 0.3 * similarity) * 100

    # ── Missing skills & recommendation ──────────────────────────────────────
    missing = list(set(job_skills) - set(resume_skills))

    if not missing:
        recommendation = "Great news — your resume covers all the key skills for this role!"
    elif len(missing) <= 3:
        recommendation = f"Almost there! Consider adding: {', '.join(missing)}."
    else:
        top_missing = missing[:5]
        recommendation = (
            f"To strengthen your resume, focus on learning: {', '.join(top_missing)}"
            + (f" (and {len(missing) - 5} more)." if len(missing) > 5 else ".")
        )

    return score, resume_skills, missing, recommendation


# ── Batch ranking (kept for future use) ──────────────────────────────────────

def rank_resumes(resume_df, job_text: str):
    job_skills = extract_skills(job_text)
    results = []

    for i in range(min(10, len(resume_df))):
        resume = resume_df["clean_resume"].iloc[i]
        score, skills, missing, _ = analyze_resume(resume, job_skills)
        results.append({"index": i, "score": score, "skills": skills, "missing": missing})

    return sorted(results, key=lambda x: x["score"], reverse=True)
