'''
We are doing this to improve our skill matching and NLP techniques to provide a better and smarter match score.

We’ll improve our system in 3 layers:

🔹 Layer 1 (NOW)

Fix scoring + improve skill matching (real logic)

🔹 Layer 2 (NEXT)

Use better skill extraction (spaCy NLP)

🔹 Layer 3 (LATER)

Turn into API + Web App
'''

# import sys
# sys.path.append("../src")

# from skill_extraction import extract_skills

import spacy 
# high speed nlp library , it can understand text, detect entities: Words → Tokens → Meaning
nlp = spacy.load("en_core_web_sm")

# def extract_skills_doc(text):

#     doc = nlp(text)
    
#     skills = []

#     for token in doc:
#         # Only keep meaningful words
#         if token.pos_ in ["NOUN", "PROPN"]:
#             skills.append(token.text.lower())

#     return list(set(skills))

#After doing this , we may still havae extracted words like "experience", "Company","Year"
#So we do Skill Filtering


SKILL_DB = [
    "python", "sql", "machine learning", "data analysis",
    "html", "css", "javascript", "react", "nodejs",
    "excel", "communication", "management", "marketing"

    "marketing", "communication", "management",
    "recruitment", "payroll", "employee relations",
    "digital marketing", "social media", "branding",
    "market research", "sales"
]



def extract_skills(text):

    text = text.lower()
    doc = nlp(text)   # NLP processing
    
    tokens = [token.text for token in doc]   # tokenize words
    
    found_skills = []

    for skill in SKILL_DB:
        skill_tokens = skill.split()   # handle multi-word skills
        
        # Check if all words of skill are in tokens
        if all(word in tokens for word in skill_tokens):
            found_skills.append(skill)

    return list(set(found_skills))