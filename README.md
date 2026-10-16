# CareerLift AI

An AI career guidance and resume agent for job seekers in Tier-2/3 cities. Built for the IBM SkillsBuild Masterclass 5 project (SDG 8: Decent Work and Economic Growth).

## What it does
1. Takes a user's profile (skills, interests, city, education, experience).
2. Normalises the skills and matches them against a role-skill dataset (`roles.json`) to rank the best-fit entry-level roles with a fit %.
3. Shows the missing skills for each role and builds a prioritised learning plan (`courses.json`) with a link to IBM SkillsBuild.
4. Generates an ATS-friendly resume PDF for any chosen role.

## Run it
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Project structure
- `app.py`: Flask routes
- `matcher.py`: skill normalisation, role matching, learning plan
- `resume.py`: resume PDF generator (reportlab)
- `roles.json`, `courses.json`: editable datasets
- `templates/`, `static/`: UI
- `test_smoke.py`: quick end-to-end test (`python test_smoke.py`)

## Roadmap
LLM-powered chat coaching, regional-language support, a WhatsApp/Telegram bot, live job data, and college partnerships.

## Notes
The role and skill dataset is a small sample for the MVP. Extend `roles.json` to cover more roles.
