from pydantic import BaseModel, Field
from typing import List

class ExtractionResult(BaseModel):
    skills: List[str] = Field(description="All skills found")
    experience_bullets: List[str] = Field(
        description="Experience bullet points (resume only)",
        default_factory=list
    )

class RewrittenBullet(BaseModel):
    missing_skill: str
    original_bullet: str
    rewritten_bullet: str

class GapReport(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    rewritten_bullets: List[RewrittenBullet]
    match_score_semantic: float
    match_score_ats: float

    def overall_score(self):
        return round(self.match_score_semantic * 0.7 + self.match_score_ats * 0.3, 1)