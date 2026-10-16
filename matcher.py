"""Skill normalisation, role matching and learning-plan logic for CareerLift AI."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "roles.json"), encoding="utf-8") as f:
    ROLES = json.load(f)
with open(os.path.join(HERE, "courses.json"), encoding="utf-8") as f:
    COURSES = json.load(f)

ALIASES = {
    "ms excel": "excel", "microsoft excel": "excel", "spreadsheets": "excel", "spreadsheet": "excel",
    "js": "javascript", "java script": "javascript", "html5": "html", "css3": "css",
    "github": "git", "msoffice": "ms office", "microsoft office": "ms office", "word": "ms office",
    "powerpoint": "ms office", "english speaking": "english", "spoken english": "english",
    "communication skills": "communication", "problem-solving": "problem solving",
    "writing": "content writing", "blogging": "content writing", "copywriting": "content writing",
    "instagram": "social media", "facebook": "social media", "digital marketing": "social media",
    "photo editing": "photoshop", "design": "creativity", "tally erp": "tally", "tally prime": "tally",
    "py": "python", "mysql": "sql", "data analysis": "statistics", "troubleshoot": "troubleshooting",
    "customer service": "customer handling", "teamwork": "communication", "typing speed": "typing",
}

def normalise_skills(raw: str):
    seen, out = set(), []
    for part in raw.replace("\n", ",").replace(";", ",").split(","):
        s = " ".join(part.strip().lower().split())
        if not s:
            continue
        s = ALIASES.get(s, s)
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def match_roles(user_skills, interests="", top_n=5):
    user = set(user_skills)
    interest_words = {w.strip().lower() for w in interests.replace(";", ",").split(",") if w.strip()}
    results = []
    for role in ROLES:
        req = role["skills"]
        have = [s for s in req if s in user]
        missing = [s for s in req if s not in user]
        fit = round(100 * len(have) / len(req))
        interest_match = any(w in role["category"] or role["category"] in w or w in role["title"].lower()
                             for w in interest_words)
        score = min(100, fit + (10 if interest_match else 0)) if have or interest_match else fit
        results.append({
            "title": role["title"], "category": role["category"], "remote": role["remote"],
            "fit": fit, "score": score, "have": have, "missing": missing, "interest_match": interest_match,
        })
    results.sort(key=lambda r: (r["score"], r["remote"]), reverse=True)
    return results[:top_n]

def learning_plan(matches, limit=6):
    """Missing skills across top matches, most frequently needed first."""
    freq = {}
    for m in matches:
        for s in m["missing"]:
            freq[s] = freq.get(s, 0) + 1
    ordered = sorted(freq, key=lambda s: (-freq[s], s))[:limit]
    return [{"skill": s, "topic": COURSES.get(s, f"Beginner course on {s}"),
             "roles_needing": freq[s], "url": "https://skillsbuild.org/"} for s in ordered]
