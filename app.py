from flask import Flask, jsonify

app = Flask(__name__)

# ── Resume Data ───────────────────────────────────────────────────────────────

RESUME = {
    "name": "Alex Johnson",
    "title": "Senior Software Engineer",
    "email": "alex.johnson@email.com",
    "phone": "+1 (555) 123-4567",
    "location": "San Francisco, CA",
    "github": "github.com/alexjohnson",
    "linkedin": "linkedin.com/in/alexjohnson",
    "summary": "Software engineer with 7+ years building scalable web applications and distributed systems. Experienced in leading teams, designing APIs, and shipping production-grade code.",
    "experience": [
        {
            "company": "TechCorp Inc.",
            "role": "Senior Software Engineer",
            "period": "2021 – Present",
            "location": "San Francisco, CA",
            "highlights": [
                "Led migration from monolith to microservices, cutting deploy time by 60%",
                "Built real-time data pipeline processing 2M events/day with Kafka and Python",
                "Mentored 5 engineers and established code-review standards",
            ],
        },
        {
            "company": "StartupXYZ",
            "role": "Software Engineer",
            "period": "2018 – 2021",
            "location": "Remote",
            "highlights": [
                "Designed REST and GraphQL APIs serving 50k+ daily active users",
                "Reduced page load time by 45% through caching and CDN optimisation",
                "Built React dashboard from scratch in 3 months",
            ],
        },
        {
            "company": "WebAgency Co.",
            "role": "Junior Developer",
            "period": "2016 – 2018",
            "location": "New York, NY",
            "highlights": [
                "Delivered 20+ client websites using Django and WordPress",
                "Automated deployment pipeline saving 4 hours per project per week",
            ],
        },
    ],
    "skills": {
        "Languages":  ["Python", "JavaScript", "TypeScript", "Go", "SQL"],
        "Frameworks": ["Flask", "FastAPI", "React", "Django", "Node.js"],
        "Databases":  ["PostgreSQL", "MongoDB", "Redis"],
        "DevOps":     ["Docker", "Kubernetes", "AWS", "GitHub Actions"],
    },
    "education": [
        {
            "institution": "University of California, Berkeley",
            "degree": "B.S. Computer Science",
            "year": "2016",
            "gpa": "3.8 / 4.0",
        }
    ],
    "certifications": [
        {"name": "AWS Certified Solutions Architect – Associate", "year": "2022"},
        {"name": "Certified Kubernetes Administrator (CKA)",      "year": "2021"},
    ],
}

# ── Shared styles & nav ───────────────────────────────────────────────────────

CSS = """
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:Arial,sans-serif;background:#f5f5f0;color:#222;line-height:1.7}
  nav{background:#222;padding:12px 40px;display:flex;gap:4px;flex-wrap:wrap}
  nav a{color:#ccc;text-decoration:none;padding:6px 14px;border-radius:3px;font-size:.85rem;transition:background .2s}
  nav a:hover,nav a.active{background:#444;color:#fff}
  .page{max-width:820px;margin:36px auto;background:#fff;padding:48px;box-shadow:0 2px 12px rgba(0,0,0,.08);border-radius:4px}
  h1{font-size:2rem;font-family:Georgia,serif}
  h2{font-size:1rem;text-transform:uppercase;letter-spacing:.15em;border-bottom:2px solid #222;padding-bottom:6px;margin:32px 0 16px}
  .subtitle{color:#555;margin-top:4px}
  .contact{margin-top:14px;display:flex;flex-wrap:wrap;gap:14px;font-size:.88rem;color:#555}
  .summary{color:#444;line-height:1.85}
  .job{margin-bottom:24px}
  .row{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px}
  .job h3,.edu h3{font-size:1rem;font-family:Georgia,serif}
  .meta{font-size:.85rem;color:#666;margin-top:2px}
  .period{font-size:.85rem;color:#888;white-space:nowrap}
  ul{padding-left:18px;margin-top:8px}
  li{font-size:.92rem;color:#444;margin-bottom:3px}
  .skills-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:16px}
  .sg h4{font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;color:#888;margin-bottom:8px}
  .tags{display:flex;flex-wrap:wrap;gap:6px}
  .tag{padding:3px 10px;background:#f0f0eb;border:1px solid #ddd;font-size:.78rem;color:#444;border-radius:2px}
  .cert-item{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #eee;font-size:.92rem}
  .cert-item:last-child{border-bottom:none}
  .ep-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:8px}
  .ep{background:#f9f9f6;border:1px solid #e0e0d8;padding:14px 18px;border-radius:3px}
  .ep a{text-decoration:none;color:#1a6bb5;font-family:monospace;font-size:.88rem}
  .ep p{font-size:.8rem;color:#888;margin-top:4px}
  .badge{display:inline-block;background:#222;color:#fff;font-size:.68rem;padding:2px 7px;border-radius:2px;margin-right:6px;vertical-align:middle;font-family:monospace}
"""

def nav(active=""):
    links = [
        ("/",               "Home"),
        ("/about",          "About"),
        ("/experience",     "Experience"),
        ("/skills",         "Skills"),
        ("/education",      "Education"),
        ("/certifications", "Certifications"),
        ("/api/resume",     "JSON API"),
    ]
    items = ""
    for href, label in links:
        cls = ' class="active"' if href == active else ""
        items += f'<a href="{href}"{cls}>{label}</a>'
    return f"<nav>{items}</nav>"

def page(active, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Resume – {RESUME['name']}</title>
<style>{CSS}</style>
</head>
<body>
{nav(active)}
<div class="page">{body}</div>
</body>
</html>"""

# ── HTML Routes ───────────────────────────────────────────────────────────────

@app.route("/")
def home():
    r = RESUME
    endpoints = [
        ("/about",          "About",          "Personal info & summary"),
        ("/experience",     "Experience",     "Work history"),
        ("/skills",         "Skills",         "Tech stack"),
        ("/education",      "Education",      "Academic background"),
        ("/certifications", "Certifications", "Professional certs"),
        ("/api/resume",     "Full JSON",      "Entire resume as JSON"),
        ("/api/experience", "Experience JSON","Work history as JSON"),
        ("/api/skills",     "Skills JSON",    "Skills as JSON"),
    ]
    cards = "".join(
        f'<div class="ep"><span class="badge">GET</span>'
        f'<a href="{url}">{url}</a><p>{desc}</p></div>'
        for url, _, desc in endpoints
    )
    body = f"""
      <h1>{r['name']}</h1>
      <div class="subtitle">{r['title']}</div>
      <div class="contact">
        <span>📧 {r['email']}</span>
        <span>📞 {r['phone']}</span>
        <span>📍 {r['location']}</span>
        <span>🔗 {r['linkedin']}</span>
        <span>🐙 {r['github']}</span>
      </div>
      <h2>Endpoints</h2>
      <div class="ep-grid">{cards}</div>
    """
    return page("/", body)


@app.route("/about")
def about():
    r = RESUME
    body = f"""
      <h1>{r['name']}</h1>
      <div class="subtitle">{r['title']}</div>
      <div class="contact">
        <span>📧 {r['email']}</span>
        <span>📞 {r['phone']}</span>
        <span>📍 {r['location']}</span>
        <span>🔗 {r['linkedin']}</span>
        <span>🐙 {r['github']}</span>
      </div>
      <h2>Summary</h2>
      <p class="summary">{r['summary']}</p>
    """
    return page("/about", body)


@app.route("/experience")
def experience():
    jobs = ""
    for j in RESUME["experience"]:
        items = "".join(f"<li>{h}</li>" for h in j["highlights"])
        jobs += f"""
          <div class="job">
            <div class="row">
              <h3>{j['company']}</h3>
              <span class="period">{j['period']}</span>
            </div>
            <div class="meta">{j['role']} &nbsp;·&nbsp; {j['location']}</div>
            <ul>{items}</ul>
          </div>"""
    return page("/experience", f"<h2>Experience</h2>{jobs}")


@app.route("/skills")
def skills():
    cards = ""
    for category, items in RESUME["skills"].items():
        tags = "".join(f'<span class="tag">{s}</span>' for s in items)
        cards += f'<div class="sg"><h4>{category}</h4><div class="tags">{tags}</div></div>'
    return page("/skills", f'<h2>Skills</h2><div class="skills-grid">{cards}</div>')


@app.route("/education")
def education():
    rows = ""
    for e in RESUME["education"]:
        rows += f"""
          <div class="edu">
            <div class="row">
              <h3>{e['institution']}</h3>
              <span class="period">{e['year']}</span>
            </div>
            <div class="meta">{e['degree']} &nbsp;·&nbsp; GPA {e['gpa']}</div>
          </div>"""
    return page("/education", f"<h2>Education</h2>{rows}")


@app.route("/certifications")
def certifications():
    rows = ""
    for c in RESUME["certifications"]:
        rows += f'<div class="cert-item"><span>{c["name"]}</span><span>{c["year"]}</span></div>'
    return page("/certifications", f"<h2>Certifications</h2>{rows}")


# ── JSON API Routes ───────────────────────────────────────────────────────────

@app.route("/api/resume")
def api_resume():
    return jsonify(RESUME)

@app.route("/api/about")
def api_about():
    keys = ["name", "title", "email", "phone", "location", "github", "linkedin", "summary"]
    return jsonify({k: RESUME[k] for k in keys})

@app.route("/api/experience")
def api_experience():
    return jsonify(RESUME["experience"])

@app.route("/api/skills")
def api_skills():
    return jsonify(RESUME["skills"])

@app.route("/api/education")
def api_education():
    return jsonify(RESUME["education"])

@app.route("/api/certifications")
def api_certifications():
    return jsonify(RESUME["certifications"])


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚀  Resume app running at http://127.0.0.1:5000\n")
    print("  HTML pages:")
    for ep in ["/", "/about", "/experience", "/skills", "/education", "/certifications"]:
        print(f"    GET  {ep}")
    print("\n  JSON API:")
    for ep in ["/api/resume", "/api/about", "/api/experience",
               "/api/skills", "/api/education", "/api/certifications"]:
        print(f"    GET  {ep}")
    print()
    app.run(host="0.0.0.0", port=5000, debug=True)