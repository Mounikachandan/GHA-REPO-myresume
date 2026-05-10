from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ── Resume Data ──────────────────────────────────────────────────────────────
RESUME = {
    "personal": {
        "name": "Alex Johnson",
        "title": "Senior Software Engineer",
        "email": "alex.johnson@email.com",
        "phone": "+1 (555) 123-4567",
        "location": "San Francisco, CA",
        "linkedin": "linkedin.com/in/alexjohnson",
        "github": "github.com/alexjohnson",
        "summary": (
            "Passionate software engineer with 7+ years building scalable "
            "web applications and distributed systems. I love clean code, "
            "great developer experience, and mentoring junior engineers."
        ),
    },
    "experience": [
        {
            "company": "TechCorp Inc.",
            "role": "Senior Software Engineer",
            "period": "2021 – Present",
            "location": "San Francisco, CA",
            "highlights": [
                "Led migration of monolith to microservices, reducing deploy time by 60%",
                "Mentored a team of 5 engineers; introduced code-review culture",
                "Built real-time data pipeline processing 2M events/day with Kafka & Python",
            ],
        },
        {
            "company": "StartupXYZ",
            "role": "Software Engineer",
            "period": "2018 – 2021",
            "location": "Remote",
            "highlights": [
                "Designed REST & GraphQL APIs consumed by 50k+ daily active users",
                "Reduced page load time by 45% through caching & CDN optimisation",
                "Shipped mobile-responsive React dashboard from scratch in 3 months",
            ],
        },
        {
            "company": "WebAgency Co.",
            "role": "Junior Developer",
            "period": "2016 – 2018",
            "location": "New York, NY",
            "highlights": [
                "Delivered 20+ client websites using Django and WordPress",
                "Automated deployment pipeline saving 4 hours/week per project",
            ],
        },
    ],
    "education": [
        {
            "institution": "University of California, Berkeley",
            "degree": "B.S. Computer Science",
            "year": "2016",
            "gpa": "3.8 / 4.0",
        }
    ],
    "skills": {
        "Languages": ["Python", "JavaScript", "TypeScript", "Go", "SQL"],
        "Frameworks": ["Flask", "FastAPI", "React", "Node.js", "Django"],
        "Databases": ["PostgreSQL", "MongoDB", "Redis", "Elasticsearch"],
        "DevOps": ["Docker", "Kubernetes", "GitHub Actions", "Terraform", "AWS"],
        "Other": ["Kafka", "gRPC", "GraphQL", "REST", "Agile / Scrum"],
    },
    "projects": [
        {
            "name": "OpenMetrics Dashboard",
            "description": "Open-source real-time monitoring dashboard with 1.2k GitHub stars.",
            "tech": ["React", "FastAPI", "InfluxDB"],
            "url": "github.com/alexjohnson/openmetrics",
        },
        {
            "name": "PyScheduler",
            "description": "Lightweight distributed task scheduler for Python — 400k PyPI downloads.",
            "tech": ["Python", "Redis", "Docker"],
            "url": "github.com/alexjohnson/pyscheduler",
        },
    ],
    "certifications": [
        {"name": "AWS Certified Solutions Architect – Associate", "year": "2022"},
        {"name": "Certified Kubernetes Administrator (CKA)", "year": "2021"},
    ],
}

# ── HTML Template ─────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{{ title }}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #0d0d0d;
    --surface: #141414;
    --border: #2a2a2a;
    --accent: #c8f542;
    --accent2: #42d4f4;
    --text: #e8e8e8;
    --muted: #6b6b6b;
    --card: #1a1a1a;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--text);font-family:'IBM Plex Sans',sans-serif;min-height:100vh}

  /* ── NAV ── */
  nav{position:sticky;top:0;z-index:99;background:rgba(13,13,13,.92);backdrop-filter:blur(12px);
      border-bottom:1px solid var(--border);display:flex;gap:0;overflow-x:auto}
  nav a{padding:14px 22px;color:var(--muted);text-decoration:none;font-family:'IBM Plex Mono',monospace;
        font-size:.78rem;letter-spacing:.08em;white-space:nowrap;border-right:1px solid var(--border);
        transition:all .2s}
  nav a:hover,nav a.active{color:var(--accent);background:rgba(200,245,66,.07)}
  nav a span{opacity:.45;margin-right:6px}

  /* ── MAIN ── */
  main{max-width:900px;margin:0 auto;padding:48px 24px 80px}

  /* ── HERO (home) ── */
  .hero{padding:64px 0 40px}
  .hero-tag{font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--accent);
            letter-spacing:.15em;text-transform:uppercase;margin-bottom:16px}
  .hero h1{font-family:'Playfair Display',serif;font-size:clamp(2.8rem,8vw,5.5rem);
           font-weight:900;line-height:1;letter-spacing:-.02em}
  .hero h1 em{color:var(--accent);font-style:normal}
  .hero-title{margin-top:12px;font-size:1.05rem;color:var(--accent2);
              font-family:'IBM Plex Mono',monospace;letter-spacing:.04em}
  .hero-summary{margin-top:28px;font-size:1.05rem;color:#b0b0b0;line-height:1.8;max-width:600px}
  .hero-contacts{margin-top:36px;display:flex;flex-wrap:wrap;gap:12px}
  .chip{padding:8px 16px;border:1px solid var(--border);border-radius:2px;
        font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--muted);
        transition:all .2s}
  .chip:hover{border-color:var(--accent);color:var(--accent)}
  .endpoint-grid{margin-top:64px;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
  .ep-card{border:1px solid var(--border);padding:20px;background:var(--card);
           transition:all .25s;cursor:pointer;text-decoration:none;display:block}
  .ep-card:hover{border-color:var(--accent);transform:translateY(-2px)}
  .ep-card .method{font-family:'IBM Plex Mono',monospace;font-size:.65rem;
                   color:var(--accent);letter-spacing:.1em;margin-bottom:8px}
  .ep-card .path{font-family:'IBM Plex Mono',monospace;font-size:.85rem;color:var(--text)}
  .ep-card .desc{margin-top:6px;font-size:.78rem;color:var(--muted);line-height:1.5}

  /* ── SECTION HEADER ── */
  .sec-header{margin-bottom:40px;padding-bottom:16px;border-bottom:1px solid var(--border)}
  .sec-header h2{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:700}
  .sec-header p{margin-top:8px;color:var(--muted);font-size:.9rem;font-family:'IBM Plex Mono',monospace}

  /* ── CARDS ── */
  .card{background:var(--card);border:1px solid var(--border);padding:28px;margin-bottom:16px;
        transition:border-color .2s}
  .card:hover{border-color:var(--border)}
  .card-header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
  .card h3{font-family:'Playfair Display',serif;font-size:1.25rem}
  .badge{font-family:'IBM Plex Mono',monospace;font-size:.68rem;padding:4px 10px;
         border:1px solid var(--accent);color:var(--accent);white-space:nowrap}
  .card-sub{margin-top:4px;font-size:.82rem;color:var(--accent2);
            font-family:'IBM Plex Mono',monospace}
  .card ul{margin-top:16px;padding-left:0;list-style:none}
  .card ul li{padding:6px 0;padding-left:20px;position:relative;color:#b0b0b0;
              font-size:.92rem;line-height:1.6}
  .card ul li::before{content:"▸";position:absolute;left:0;color:var(--accent);font-size:.75rem;top:8px}

  /* ── SKILLS ── */
  .skill-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
  .skill-card{background:var(--card);border:1px solid var(--border);padding:24px}
  .skill-card h3{font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--accent);
                 letter-spacing:.12em;text-transform:uppercase;margin-bottom:16px}
  .tags{display:flex;flex-wrap:wrap;gap:8px}
  .tag{padding:5px 12px;background:rgba(255,255,255,.04);border:1px solid var(--border);
       font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:var(--text)}

  /* ── PROJECTS ── */
  .proj-card{background:var(--card);border:1px solid var(--border);padding:28px;margin-bottom:16px}
  .proj-card h3{font-family:'Playfair Display',serif;font-size:1.2rem}
  .proj-card p{margin-top:10px;color:#b0b0b0;line-height:1.7;font-size:.92rem}
  .proj-url{display:inline-block;margin-top:14px;font-family:'IBM Plex Mono',monospace;
            font-size:.72rem;color:var(--accent2)}

  /* ── CERTS ── */
  .cert-card{background:var(--card);border:1px solid var(--border);padding:20px 28px;
             margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
  .cert-card h3{font-size:.98rem}
  .cert-year{font-family:'IBM Plex Mono',monospace;font-size:.78rem;color:var(--accent)}

  /* ── JSON VIEW ── */
  .json-wrap{background:var(--card);border:1px solid var(--border);padding:28px;overflow-x:auto}
  pre{font-family:'IBM Plex Mono',monospace;font-size:.82rem;line-height:1.7;color:#b0b0b0}
  .jk{color:var(--accent2)}.jv{color:var(--accent)}.js{color:#f4a142}

  /* ── FOOTER ── */
  footer{text-align:center;padding:24px;border-top:1px solid var(--border);
         font-family:'IBM Plex Mono',monospace;font-size:.7rem;color:var(--muted)}
  footer em{color:var(--accent)}
</style>
</head>
<body>

<nav>
  <a href="/" {% if active=='home' %}class="active"{% endif %}><span>/</span>Home</a>
  <a href="/about" {% if active=='about' %}class="active"{% endif %}><span>01</span>About</a>
  <a href="/experience" {% if active=='experience' %}class="active"{% endif %}><span>02</span>Experience</a>
  <a href="/skills" {% if active=='skills' %}class="active"{% endif %}><span>03</span>Skills</a>
  <a href="/projects" {% if active=='projects' %}class="active"{% endif %}><span>04</span>Projects</a>
  <a href="/education" {% if active=='education' %}class="active"{% endif %}><span>05</span>Education</a>
  <a href="/certifications" {% if active=='certs' %}class="active"{% endif %}><span>06</span>Certs</a>
  <a href="/api/resume" {% if active=='api' %}class="active"{% endif %}><span>⚡</span>JSON API</a>
</nav>

<main>{{ content }}</main>

<footer>Built with <em>Flask</em> · {{ year }} · <em>{{ name }}</em></footer>
</body>
</html>"""

def render(active, content, extra=""):
    return render_template_string(
        HTML,
        active=active,
        content=content,
        title=f"{RESUME['personal']['name']} — Resume",
        year=datetime.now().year,
        name=RESUME["personal"]["name"],
    )

# ── ROUTES ───────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    p = RESUME["personal"]
    eps = [
        ("/about",          "About",          "Personal info & summary"),
        ("/experience",     "Experience",     "Work history"),
        ("/skills",         "Skills",         "Tech stack"),
        ("/projects",       "Projects",       "Side projects"),
        ("/education",      "Education",      "Academic background"),
        ("/certifications", "Certifications", "Professional certs"),
        ("/api/resume",     "Full JSON",      "Raw API response"),
        ("/api/experience", "Exp JSON",       "Experience as JSON"),
        ("/api/skills",     "Skills JSON",    "Skills as JSON"),
    ]
    cards = "".join(
        f'<a class="ep-card" href="{url}">'
        f'<div class="method">GET</div>'
        f'<div class="path">{url}</div>'
        f'<div class="desc">{desc}</div>'
        f'</a>'
        for url, _, desc in eps
    )
    body = f"""
    <div class="hero">
      <div class="hero-tag">// resume · portfolio</div>
      <h1>{p['name'].split()[0]}<br><em>{p['name'].split()[-1]}</em></h1>
      <div class="hero-title">{p['title']}</div>
      <p class="hero-summary">{p['summary']}</p>
      <div class="hero-contacts">
        <span class="chip">📧 {p['email']}</span>
        <span class="chip">📞 {p['phone']}</span>
        <span class="chip">📍 {p['location']}</span>
        <span class="chip">🔗 {p['linkedin']}</span>
        <span class="chip">🐙 {p['github']}</span>
      </div>
    </div>
    <div class="sec-header">
      <h2>Endpoints</h2>
      <p>// navigate to any section below</p>
    </div>
    <div class="endpoint-grid">{cards}</div>
    """
    return render("home", body)


@app.route("/about")
def about():
    p = RESUME["personal"]
    body = f"""
    <div class="sec-header">
      <h2>About</h2>
      <p>// personal info & summary</p>
    </div>
    <div class="card">
      <div class="card-header">
        <div>
          <h3>{p['name']}</h3>
          <div class="card-sub">{p['title']}</div>
        </div>
        <span class="badge">OPEN TO WORK</span>
      </div>
      <ul>
        <li>📧 {p['email']}</li>
        <li>📞 {p['phone']}</li>
        <li>📍 {p['location']}</li>
        <li>🔗 {p['linkedin']}</li>
        <li>🐙 {p['github']}</li>
      </ul>
    </div>
    <div class="card"><p style="line-height:1.9;color:#b0b0b0">{p['summary']}</p></div>
    """
    return render("about", body)


@app.route("/experience")
def experience():
    cards = ""
    for job in RESUME["experience"]:
        highlights = "".join(f"<li>{h}</li>" for h in job["highlights"])
        cards += f"""
        <div class="card">
          <div class="card-header">
            <div>
              <h3>{job['company']}</h3>
              <div class="card-sub">{job['role']} · {job['location']}</div>
            </div>
            <span class="badge">{job['period']}</span>
          </div>
          <ul>{highlights}</ul>
        </div>"""
    body = f'<div class="sec-header"><h2>Experience</h2><p>// work history</p></div>{cards}'
    return render("experience", body)


@app.route("/skills")
def skills():
    cards = ""
    for category, items in RESUME["skills"].items():
        tags = "".join(f'<span class="tag">{s}</span>' for s in items)
        cards += f'<div class="skill-card"><h3>{category}</h3><div class="tags">{tags}</div></div>'
    body = f'<div class="sec-header"><h2>Skills</h2><p>// tech stack</p></div><div class="skill-grid">{cards}</div>'
    return render("skills", body)


@app.route("/projects")
def projects():
    cards = ""
    for proj in RESUME["projects"]:
        tags = "".join(f'<span class="tag">{t}</span>' for t in proj["tech"])
        cards += f"""
        <div class="proj-card">
          <div class="card-header">
            <h3>{proj['name']}</h3>
          </div>
          <p>{proj['description']}</p>
          <div class="tags" style="margin-top:14px">{tags}</div>
          <div class="proj-url">→ {proj['url']}</div>
        </div>"""
    body = f'<div class="sec-header"><h2>Projects</h2><p>// side projects & open source</p></div>{cards}'
    return render("projects", body)


@app.route("/education")
def education():
    cards = ""
    for edu in RESUME["education"]:
        cards += f"""
        <div class="card">
          <div class="card-header">
            <div>
              <h3>{edu['institution']}</h3>
              <div class="card-sub">{edu['degree']}</div>
            </div>
            <span class="badge">{edu['year']}</span>
          </div>
          <ul><li>GPA: {edu['gpa']}</li></ul>
        </div>"""
    body = f'<div class="sec-header"><h2>Education</h2><p>// academic background</p></div>{cards}'
    return render("education", body)


@app.route("/certifications")
def certifications():
    cards = ""
    for cert in RESUME["certifications"]:
        cards += f"""
        <div class="cert-card">
          <h3>{cert['name']}</h3>
          <span class="cert-year">{cert['year']}</span>
        </div>"""
    body = f'<div class="sec-header"><h2>Certifications</h2><p>// professional credentials</p></div>{cards}'
    return render("certs", body)


# ── JSON API ENDPOINTS ────────────────────────────────────────────────────────

@app.route("/api/resume")
def api_resume():
    return jsonify(RESUME)

@app.route("/api/experience")
def api_experience():
    return jsonify(RESUME["experience"])

@app.route("/api/skills")
def api_skills():
    return jsonify(RESUME["skills"])

@app.route("/api/projects")
def api_projects():
    return jsonify(RESUME["projects"])

@app.route("/api/education")
def api_education():
    return jsonify(RESUME["education"])

@app.route("/api/certifications")
def api_certifications():
    return jsonify(RESUME["certifications"])

@app.route("/api/about")
def api_about():
    return jsonify(RESUME["personal"])


if __name__ == "__main__":
    print("\n🚀  Resume app running at http://127.0.0.1:5000\n")
    print("  HTML endpoints:")
    for ep in ["/", "/about", "/experience", "/skills", "/projects", "/education", "/certifications"]:
        print(f"    GET {ep}")
    print("\n  JSON API endpoints:")
    for ep in ["/api/resume", "/api/about", "/api/experience", "/api/skills",
               "/api/projects", "/api/education", "/api/certifications"]:
        print(f"    GET {ep}")
    print()
    app.run(debug=True)
