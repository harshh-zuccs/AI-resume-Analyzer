import spacy

nlp = spacy.load("en_core_web_sm")

# ── Complete skill database covering ALL job roles ────────────────────────────
# Each entry is lowercase. Multi-word skills are matched via substring search.

SKILL_DB = [
    # Programming languages
    "python", "java", "c++", "javascript", "typescript", "r", "scala", "go",

    # Data Science / ML
    "machine learning", "deep learning", "data analysis", "statistics",
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch",
    "data visualization", "feature engineering", "nlp", "computer vision",

    # Databases & querying
    "sql", "mysql", "postgresql", "mongodb", "nosql", "redis",

    # Web Development
    "html", "css", "react", "nodejs", "node.js", "angular", "vue",
    "rest api", "graphql", "django", "flask", "fastapi",

    # Data tools
    "excel", "power bi", "tableau", "google analytics", "looker",

    # DevOps / Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "linux",
    "ci/cd", "jenkins", "git", "github", "terraform",
    "scripting", "monitoring", "ansible",

    # Design / UX
    "figma", "sketch", "adobe xd", "wireframing", "prototyping",
    "design thinking", "user research", "usability testing",

    # Business / Management
    "communication", "management", "stakeholder management",
    "project management", "business analysis", "agile", "scrum",
    "product strategy", "roadmap", "analytics", "reporting",
    "problem solving", "data structures", "algorithms",

    # Marketing
    "digital marketing", "seo", "branding", "social media",
    "campaign management", "market research", "content marketing",
    "email marketing", "ppc", "google ads",

    # HR
    "recruitment", "payroll", "employee relations",
    "organizational skills", "talent acquisition", "onboarding",
    "performance management", "hris",

    # Sales & general
    "sales", "crm", "negotiation", "customer service",
]


def extract_skills(text: str) -> list[str]:
    """
    Extract skills from text using substring matching against SKILL_DB.
    Uses spaCy for lightweight normalisation (lowercasing + whitespace collapse)
    then checks whether each skill phrase appears as a contiguous substring.
    This is more reliable than strict token-by-token matching because it handles
    compound words, punctuation variants (node.js / nodejs) and partial matches.
    """
    # Normalise: lowercase + collapse whitespace
    text = " ".join(text.lower().split())

    found_skills = []

    for skill in SKILL_DB:
        skill_norm = " ".join(skill.lower().split())

        # Direct substring match (handles multi-word skills naturally)
        if skill_norm in text:
            found_skills.append(skill)
            continue

        # Fallback: handle common punctuation variants
        #   nodejs ↔ node.js,  ci/cd ↔ cicd,  c++ ↔ c plus plus, etc.
        variants = _get_variants(skill_norm)
        if any(v in text for v in variants):
            found_skills.append(skill)

    return list(set(found_skills))


def _get_variants(skill: str) -> list[str]:
    """Return common spelling/punctuation variants for a skill string."""
    variants = []

    replacements = [
        (".", ""),          # node.js → nodejs
        ("/", " "),         # ci/cd   → ci cd
        ("/", ""),          # ci/cd   → cicd
        ("-", " "),         # scikit-learn → scikit learn
        ("-", ""),          # scikit-learn → scikitlearn
        ("+", "plus "),     # c++ → cplus plus  (rough)
        (" ", ""),          # nodejs  → node js edge case
    ]

    for old, new in replacements:
        if old in skill:
            variants.append(skill.replace(old, new))

    return variants
