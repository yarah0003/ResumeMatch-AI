from .extractor    import extract_skills
from .rag_setup    import build_taxonomy_store, build_bullets_store
from .matcher      import match_skills, ats_score
from .rewriter     import find_closest_bullet, rewrite_bullet
from .output_schema import GapReport, RewrittenBullet

def analyze_gap(resume_text, jd_text):
    print("[1/5] Loading vector stores...")
    taxonomy_store = build_taxonomy_store()
    bullets_store  = build_bullets_store()

    print("[2/5] Extracting skills from resume...")
    resume_data = extract_skills(resume_text, "Resume")

    print("[3/5] Extracting skills from job description...")
    jd_data = extract_skills(jd_text, "Job Description")

    print("[4/5] Matching skills...")
    matched, missing = match_skills(resume_data.skills, jd_data.skills)

    sem_score = round(len(matched) / len(jd_data.skills) * 100, 1) if jd_data.skills else 0
    at_score  = ats_score(resume_data.skills, jd_data.skills)

    print("[5/5] Rewriting bullets for missing skills...")
    rewrites = []
    for skill in missing[:3]:
        closest = find_closest_bullet(skill, resume_data.experience_bullets)
        if closest:
            rewrites.append(RewrittenBullet(
                missing_skill=skill,
                original_bullet=closest,
                rewritten_bullet=rewrite_bullet(skill, closest, bullets_store)
            ))

    return GapReport(
        matched_skills=matched, missing_skills=missing,
        rewritten_bullets=rewrites,
        match_score_semantic=sem_score, match_score_ats=at_score
    )