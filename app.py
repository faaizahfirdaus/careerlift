from flask import Flask, render_template, request, send_file, redirect, url_for
from io import BytesIO
from matcher import normalise_skills, match_roles, learning_plan
from resume import build_resume

app = Flask(__name__)

ACRONYMS = {"crm", "seo", "sql", "gst", "html", "css", "ms"}

@app.template_filter("pretty")
def pretty(skill):
    return " ".join(w.upper() if w in ACRONYMS else w.capitalize() for w in skill.split())

def _profile(form):
    return {
        "name": form.get("name", "").strip(), "email": form.get("email", "").strip(),
        "phone": form.get("phone", "").strip(), "city": form.get("city", "").strip(),
        "education": form.get("education", "").strip(), "experience": form.get("experience", "").strip(),
        "interests": form.get("interests", "").strip(),
        "skills": normalise_skills(form.get("skills", "")),
    }

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/analyze")
def analyze():
    profile = _profile(request.form)
    if not profile["skills"]:
        return render_template("index.html", error="Please enter at least one skill.", form=request.form), 400
    matches = match_roles(profile["skills"], profile["interests"])
    plan = learning_plan(matches)
    return render_template("results.html", p=profile, matches=matches, plan=plan,
                           skills_csv=", ".join(profile["skills"]))

@app.post("/resume")
def resume():
    profile = _profile(request.form)
    pdf = build_resume(profile, request.form.get("target_role", ""))
    fname = (profile["name"] or "resume").strip().replace(" ", "_") + "_Resume.pdf"
    return send_file(BytesIO(pdf), mimetype="application/pdf", as_attachment=True, download_name=fname)

if __name__ == "__main__":
    app.run(debug=True)
