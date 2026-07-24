from dotenv import load_dotenv
load_dotenv()

from pipeline.orchestrator import analyze_gap

FAKE_RESUME = """
Software Engineer with 3 years of experience.
- Built REST APIs using Django and deployed on AWS EC2
- Helped automate reports using Excel macros and some scripting
- Worked in Agile team with daily standups and sprint planning
- Used Git for version control across multiple projects
"""

FAKE_JD = """
We are looking for a Python Developer with:
- Strong Python and FastAPI skills
- Experience with CI/CD pipelines (GitHub Actions or Jenkins)
- Docker and Kubernetes for containerization
- PostgreSQL database experience
- REST API design and development
- Good communication and teamwork skills
"""

result = analyze_gap(FAKE_RESUME, FAKE_JD)

print(f"\n=== RESULTS ===")
print(f"Semantic Score: {result.match_score_semantic}%")
print(f"ATS Score:      {result.match_score_ats}%")
print(f"Overall Score:  {result.overall_score()}%")
print(f"\nMatched: {result.matched_skills}")
print(f"Missing: {result.missing_skills}")
for rb in result.rewritten_bullets:
    print(f"\n--- Missing: {rb.missing_skill}")
    print(f"Original:  {rb.original_bullet}")
    print(f"Rewritten: {rb.rewritten_bullet}")